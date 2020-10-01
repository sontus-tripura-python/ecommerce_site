
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from ecommerceapp import views as user_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
     path('', include('ecommerceapp.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
