from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserSearchView.as_view(), name='user_search'),
    path('create/', views.create_user, name='create_user'),
    path('edit/<int:user_id>/<str:role>', views.edit_user, name='edit_user'),
    path('delete/<int:user_id>/<str:role>', views.user_delete_confirmation, name='user_delete_confirmation'),
    path('delete/<int:user_id>/<str:role>/delete/', views.user_delete, name='user_delete'),
    # path('search/<str:username>/', views.UserSearchView.as_view(), name='user_search_with_username'),



]
