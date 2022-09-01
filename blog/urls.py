from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import AuthorProfile, PostCreateView, PostDelete, PostDetailView, PostUpdate, PostsView, \
    about_page, contact_form, post_by_auth, post_comment


app_name = 'blog'

urlpatterns = [
    path('', PostsView.as_view(), name='posts'),
    path('contact/', contact_form, name='contact'),
    path('about/', about_page, name='about'),
    path('<slug>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/add/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('posts/<int:pk>', post_by_auth, name='post_by_auth'),
    path('<int:post_id>/comment/', post_comment, name='post_comment'),
    path('author/<int:pk>/', AuthorProfile.as_view(), name='author_profile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
