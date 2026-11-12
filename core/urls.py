from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("profil/", views.profil_organisasi, name="profil"),
    path("pimpinan/", views.daftar_pimpinan, name="pimpinan"),
    path("ranting/", views.daftar_ranting, name="ranting"),
    path("amal-usaha/", views.daftar_amal_usaha, name="amal_usaha"),
    path("berita/", views.daftar_berita, name="berita"),
    path("berita/<slug:slug>/", views.detail_berita, name="detail_berita"),
    path("agenda/", views.daftar_agenda, name="agenda"),
    path("agenda/<int:pk>/", views.detail_agenda, name="detail_agenda"),
    path("unduhan/", views.daftar_dokumen, name="unduhan"),
    path("kontak/", views.pesan_masuk, name="pesan_masuk"),
    path("tautan/", views.daftar_tautan, name="tautan"),
]