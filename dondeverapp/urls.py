from django.contrib import admin
from django.urls import path, include
from catalog import views_admin

urlpatterns = [
    # trigger import endpoint before admin so it doesn't conflict
    path('admin/trigger-import/', views_admin.trigger_import, name='trigger_import'),
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
]
