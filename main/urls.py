from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('',views.index),
    path('home/',views.index,name='home'),
    path('sign-up/',views.signup,name='signup'),
    path('nums/', views.nums, name='nums'),
    path('addnum/',views.addnum,name='addnum'),
    path('setup/<str:username>',views.setup,name='setup'),
    path('profile/<str:username>',views.profile,name='profile'),
    path('<str:mode>/<str:username>/edit/add/<str:property>',views.edit_deatails,name='edit'),
    path('edit/remove/<str:property>/<int:id>',views.del_deatails,name='del'),
    path('edit/basic/', views.edit_basic_info, name='edit_basic_info'),
    path('edit/contact/', views.edit_contact_info, name='edit_contact_info'),
    path('edit/identity/', views.edit_identity_info, name='edit_identity_info'),
    path('edit/privacy/',views.edit_privacy,name='edit_privacy'),
    path('edit/user/',views.edit_user_info,name='edit_user_info'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('recover/',views.account_recover,name='recover')
]