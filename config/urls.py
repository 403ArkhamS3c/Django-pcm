"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("profil/", views.profil_organisasi, name="profil"),
    path("pimpinan/", views.daftar_pimpinan, name="pimpinan"),
    path("ranting/", views.daftar_ranting, name="ranting"),
    path("amal-usaha/", views.daftar_amal_usaha, name="amal_usaha"),
    path("berita/", views.daftar_berita, name="berita"),
    path("agenda/", views.daftar_agenda, name="agenda"),
    path("dokumen/", views.daftar_dokumen, name="dokumen"),
    path("berita/<slug:slug>/", views.detail_berita, name="detail_berita"),
    path("agenda/<int:pk>/", views.detail_agenda, name="detail_agenda"),
    path("pesan-masuk/", views.pesan_masuk, name="pesan_masuk"),
    path("tautan/", views.daftar_tautan, name="tautan"),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

