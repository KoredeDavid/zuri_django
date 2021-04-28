from django.urls import path, include
from . import views

# path('', views.project_index, name='project_index'),
# path("<a_title>/", views.project_detail, name="project_detail"),

urlpatterns = [
    path('', views.repo, name='home'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.sign_in, name='sign_in'),
    path('logout/', views.sign_out, name='sign_out'),
    path('articles-factory/', views.articles_factory, name='articles_factory'),
    path('category/<category_slug>/', views.category, name="category"),
    path('post/<post_slug>/', views.post, name="post"),
    path('comment/<post>/', views.comment, name="comment"),
    # path('comment/<user>/<post>/', views.make_comment, name="make_comment"),
]
