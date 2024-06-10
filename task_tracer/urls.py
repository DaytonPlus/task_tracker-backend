"""
URL configuration for task_tracer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


# Disable Admin Authentication
class AccessUser:
    has_module_perms = has_perm = __getattr__ = lambda s,*a,**kw: True
admin.site.has_permission = lambda r: setattr(r, 'user', AccessUser()) or True


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('v1/', include('crud.urls')),
        path('auth/', include('user.urls')),
    ])),
]
