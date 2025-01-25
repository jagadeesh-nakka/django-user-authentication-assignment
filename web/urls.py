'''from django.contrib import admin
from django.urls import path
from webapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('upload/', views.upload, name='upload'),
    path('open_camera/', views.open_camera, name='open_camera'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)'''

from django.urls import path
from webapp import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('signout/', LogoutView.as_view(), name='logout'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('change_password/', views.change_password, name='change-password'),
    path('profile/', views.profile, name='profile'),
    path('open-camera/', views.open_camera, name='open_camera'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset/<uidb64>/<token>/', views.reset_password, name='reset_password'),
]

# Serve static files during development (in DEBUG mode)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
