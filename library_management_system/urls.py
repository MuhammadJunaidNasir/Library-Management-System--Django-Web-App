from django.contrib import admin
from django.urls import path, include
from library.views import logout_view  # <-- import custom logout view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),

    path('login/', auth_views.LoginView.as_view(
        template_name='library/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    path('logout/', logout_view, name='logout'), 
]
