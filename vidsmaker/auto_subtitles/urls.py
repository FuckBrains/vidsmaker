from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', views.profile, name='profile'),
    path('upload', views.model_form_upload, name='upload'),
    path('generate/<int:document_id>/download', views.download, name='download'),
    path('generate/<int:document_id>/save', views.save_video, name='save'),
    path('generate/<int:document_id>', views.generate_video, name='generate'),
    path('videos/', views.videos, name='videos'),
    path('videos/<int:document_id>/delete', views.videos, name='delete_video'),
    path('translate/<int:document_id>', views.translate_video, name='translate'),
]