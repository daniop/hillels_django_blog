from django.contrib import messages
from django.contrib.auth import authenticate, login, views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST

from .forms import AuthorCreationForm, CommentForm, ContactForm
from .models import Author, Post
from .tasks import new_comment, send_contact


class PostsView(generic.ListView):
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    queryset = Post.published.select_related('author')


def post_by_auth(request, pk):
    author = get_object_or_404(Author, id=pk)
    if request.user == author:
        objects_list = Post.objects.filter(author=author)
    else:
        objects_list = Post.published.filter(author=author)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, 3)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_by_auth.html', {'page_obj': page_obj, 'author': author})


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        objects_list = self.object.comments.filter(active=True)
        page_num = self.request.GET.get('page', 1)
        paginator = Paginator(objects_list, 3)
        total_comments = objects_list.count()
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['page_obj'] = page_obj
        if self.request.user.is_authenticated:
            context['form'] = CommentForm(
                initial={'email': self.request.user.email, 'name': self.request.user.username}
            )
        else:
            context['form'] = CommentForm()
        context['total_comments'] = total_comments
        return context


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        message = f'Новый комментарий к посту: {post.title} автора {post.author}- {comment.body}'
        new_comment.delay("New comment", message)

    return render(request, 'blog/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'short_description', 'body', 'status', 'post_image']
    template_name_suffix = '_create'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:posts')


class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'short_description', 'body', 'status', 'post_image']
    template_name_suffix = '_update'

    def get_object(self, queryset=None):
        obj = super(PostUpdate, self).get_object(queryset)
        if obj.author != self.request.user:
            raise Http404("Это не ваш пост)")
        return obj


class PostDelete(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:posts')
    template_name_suffix = '_delete'

    def form_valid(self, form):
        messages.success(self.request, "Пост удален.")
        return super(PostDelete, self).form_valid(form)

    def get_object(self, queryset=None):
        obj = super(PostDelete, self).get_object(queryset)
        if obj.author != self.request.user:
            raise Http404("Это не ваш пост)")
        return obj


class SignUpView(generic.CreateView):
    form_class = AuthorCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("blog:posts")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)  # TODO: fix
        return super(SignUpView, self).form_valid(form)


class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class AuthorProfile(generic.DetailView):
    model = Author
    template_name = 'blog/author_profile.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorProfile, self).get_context_data(**kwargs)
        context['total_posts'] = self.object.author.all().count()
        return context


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Author
    fields = ["first_name", "last_name", "email", "username", "description", "profile_photo"]
    template_name = "registration/update_profile.html"
    success_url = reverse_lazy("blog:posts")
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class PasswordsChangeView(views.PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'registration/change_pass_done.html')


def contact(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_contact.delay(name, email, message)
            data['form_is_valid'] = True
            msg = [f"Сообщение от {name} отправлено"]
            data['msg_list'] = render_to_string('blog/message_contact.html', {
                'messages': msg
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
    else:
        form = ContactForm()
    return contact(request, form, 'blog/contact.html')


def about_page(request):
    return render(request, 'blog/about.html')
