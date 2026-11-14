from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    ProfilOrganisasi,
    Pimpinan,
    Ranting,
    AmalUsaha,
    Berita,
    Agenda,
    Dokumen,
    PesanMasuk,
    TautanTerkait,
    SambutanKetua,
    GaleriKegiatan,
)


@admin.register(ProfilOrganisasi)
class ProfilOrganisasiAdmin(ModelAdmin):
    def has_add_permission(self, request):
        # Hanya izinkan penambahan jika profil belum ada.
        return not ProfilOrganisasi.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Profil organisasi tidak boleh dihapus melalui admin.
        return False

@admin.register(Pimpinan)
class PimpinanAdmin(ModelAdmin):
    list_display = ("nama", "jabatan", "periode", "urutan_tampil")
    search_fields = ("nama", "jabatan", "periode")
    list_filter = ("periode",)
    ordering = ("urutan_tampil", "nama")


@admin.register(Ranting)
class RantingAdmin(ModelAdmin):
    list_display = ("nama_ranting", "ketua", "telepon")
    search_fields = ("nama_ranting", "ketua", "alamat")
    ordering = ("nama_ranting",)


@admin.register(AmalUsaha)
class AmalUsahaAdmin(ModelAdmin):
    list_display = ("nama", "bidang")
    search_fields = ("nama", "alamat")
    list_filter = ("bidang",)


@admin.register(Berita)
class BeritaAdmin(ModelAdmin):
    list_display = ("judul", "status", "tanggal_terbit")
    search_fields = ("judul", "slug", "isi")
    list_filter = ("status", "tanggal_terbit")
    prepopulated_fields = {"slug": ("judul",)}


@admin.register(Agenda)
class AgendaAdmin(ModelAdmin):
    list_display = ("nama_kegiatan", "waktu_mulai", "tempat")
    search_fields = ("nama_kegiatan", "tempat", "keterangan")
    list_filter = ("waktu_mulai",)


@admin.register(Dokumen)
class DokumenAdmin(ModelAdmin):
    list_display = ("judul", "tanggal_unggah")
    search_fields = ("judul", "keterangan")
    list_filter = ("tanggal_unggah",)


@admin.register(PesanMasuk)
class PesanMasukAdmin(ModelAdmin):
    list_display = (
        "nama", "email", "subjek", "sudah_dibaca", "waktu_kirim"
    )
    search_fields = ("nama", "email", "subjek", "pesan")
    list_filter = ("sudah_dibaca", "waktu_kirim")
    readonly_fields = ("waktu_kirim",)


@admin.register(TautanTerkait)
class TautanTerkaitAdmin(ModelAdmin):
    list_display = ("nama", "url", "urutan")
    search_fields = ("nama",)
    ordering = ("urutan", "nama")

@admin.register(SambutanKetua)
class SambutanKetuaAdmin(ModelAdmin):
    list_display = ("nama",)

    def has_add_permission(self, request):
        return not SambutanKetua.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(GaleriKegiatan)
class GaleriKegiatanAdmin(ModelAdmin):
    list_display = ("judul",)
    search_fields = ("judul",)