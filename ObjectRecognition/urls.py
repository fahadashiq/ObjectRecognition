from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views, settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('objectDetection', views.objectDetection, name='objectDetection')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
