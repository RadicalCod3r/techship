from django.urls import path
from ..views import user_views as views

urlpatterns = [
    path('', views.getUsers, name='users'),  
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.registerUser, name='register_user'),
    path('profile/', views.getUserProfile, name='user_profile'),
    path('profile/update/', views.updateUserProfile, name='user_profile_update'),  
    path('<str:pk>/', views.getUserById, name='single_user'),
    path('update/<str:pk>/', views.updateUser, name='user_update'),
    path('delete/<str:pk>/', views.deleteUser, name='user_delete')
]