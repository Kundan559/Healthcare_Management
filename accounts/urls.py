from django.urls import path
from . import views 

urlpatterns = [
    path('register/',
         views.register_view,
         name='register'
         ),
    
    path(
        '',
        views.login_view,
        name='accounts_home'
    ),
    
    path(
        'login/',
        views.login_view,
        name='login'
        ),
    
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
    
    
]
