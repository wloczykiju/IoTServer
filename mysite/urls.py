from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mysite.core import views
from users import views as user_views

# urls for the site            

urlpatterns = [
    path('', views.home, name='home'),
    path('honeypots/', views.deploy_honeypot, name='deploy_honeypot'),
    path('logs/', views.get_logs, name='get_logs'),
    path('guide/', views.guide, name='guide'),
    path('about/', views.about_index, name="about_index"),
    path('about/<int:pk>/', views.about_detail, name="about_detail"),
    path('iot_honeypots/', views.iot_honeypots, name="iot_honeypots"),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name="register"),
    path('profile/', user_views.profile, name="profile"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
