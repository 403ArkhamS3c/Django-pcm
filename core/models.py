from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# 1. Profil organisasi
class ProfilOrganisasi(models.Model):
    nama = models.CharField(max_length=200)
    nama_singkat = models.CharField(max_length=100)
    tagline = models.CharField(max_length=255)
    tentang = models.TextField()
    sejarah = models.TextField()
    visi = models.TextField()
    misi = models.TextField(
        help_text="Tuliskan satu misi pada setiap baris."
    )
    alamat_sekretariat = models.TextField()
    telepon = models.CharField(max_length=30)
    email = models.EmailField()
    jumlah_anggota_ktam = models.PositiveIntegerField(default=0)
    gambar_utama = models.ImageField(upload_to="profil/")

    class Meta:
        verbose_name = "Profil Organisasi"
        verbose_name_plural = "Profil Organisasi"

    def save(self, *args, **kwargs):
        if not self.pk and ProfilOrganisasi.objects.exists():
            raise ValidationError(
                "Profil organisasi hanya boleh memiliki satu baris."
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError(
            "Profil organisasi tidak boleh dihapus."
        )

    def __str__(self):
        return self.nama_singkat


# 2. Pimpinan
class Pimpinan(models.Model):
    nama = models.CharField(max_length=150)
    jabatan = models.CharField(max_length=150)
    periode = models.CharField(
        max_length=30,
        help_text="Contoh: 2022–2027"
    )
    foto = models.ImageField(upload_to="pimpinan/")
    urutan_tampil = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["urutan_tampil", "nama"]
        verbose_name = "Pimpinan"
        verbose_name_plural = "Pimpinan"

    def __str__(self):
        return f"{self.nama} - {self.jabatan}"


# 3. Ranting
class Ranting(models.Model):
    nama_ranting = models.CharField(max_length=200)
    ketua = models.CharField(max_length=150)
    alamat = models.TextField()
    telepon = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["nama_ranting"]
        verbose_name = "Ranting"
        verbose_name_plural = "Ranting"

    def __str__(self):
        return self.nama_ranting


# 4. Amal usaha
class AmalUsaha(models.Model):
    class Bidang(models.TextChoices):
        PENDIDIKAN = "pendidikan", "Pendidikan"
        KESEHATAN = "kesehatan", "Kesehatan"
        SOSIAL = "sosial", "Sosial"
        EKONOMI = "ekonomi", "Ekonomi"

    nama = models.CharField(max_length=200)
    bidang = models.CharField(
        max_length=20,
        choices=Bidang.choices
    )
    deskripsi = models.TextField()
    alamat = models.TextField()
    gambar = models.ImageField(upload_to="amal_usaha/")

    class Meta:
        ordering = ["bidang", "nama"]
        verbose_name = "Amal Usaha"
        verbose_name_plural = "Amal Usaha"

    def __str__(self):
        return self.nama


# 5. Berita
class BeritaQuerySet(models.QuerySet):
    def terbit(self):
        sekarang = timezone.now()
        return self.filter(
            status=self.model.Status.TERBIT,
            tanggal_terbit__lte=sekarang
        )


class Berita(models.Model):
    class Status(models.TextChoices):
        DRAF = "draf", "Draf"
        TERBIT = "terbit", "Terbit"

    judul = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True
    )
    ringkasan = models.TextField()
    isi = models.TextField()
    gambar_sampul = models.ImageField(
        upload_to="berita/",
        blank=True
    )
    tanggal_terbit = models.DateTimeField(
        default=timezone.now
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAF
    )

    objects = BeritaQuerySet.as_manager()

    class Meta:
        ordering = ["-tanggal_terbit"]
        verbose_name = "Berita"
        verbose_name_plural = "Berita"


    def save(self, *args, **kwargs):
        dasar_slug = slugify(self.slug or self.judul) or "berita"
        slug_baru = dasar_slug
        nomor = 2

        while Berita.objects.filter(
            slug=slug_baru
        ).exclude(pk=self.pk).exists():
            slug_baru = f"{dasar_slug}-{nomor}"
            nomor += 1

        self.slug = slug_baru
        
        super().save(*args, **kwargs)


    def __str__(self):
        return self.judul


# 6. Agenda
class Agenda(models.Model):
    nama_kegiatan = models.CharField(max_length=200)
    waktu_mulai = models.DateTimeField()
    tempat = models.CharField(max_length=250)
    keterangan = models.TextField(blank=True)

    class Meta:
        ordering = ["waktu_mulai"]
        verbose_name = "Agenda"
        verbose_name_plural = "Agenda"

    def __str__(self):
        return self.nama_kegiatan


# 7. Dokumen
class Dokumen(models.Model):
    judul = models.CharField(max_length=200)
    keterangan = models.TextField(blank=True)
    berkas = models.FileField(upload_to="dokumen/")
    tanggal_unggah = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-tanggal_unggah"]
        verbose_name = "Dokumen"
        verbose_name_plural = "Dokumen"

    def __str__(self):
        return self.judul


# 8. Pesan masuk
class PesanMasuk(models.Model):
    nama = models.CharField(max_length=150)
    email = models.EmailField()
    subjek = models.CharField(max_length=200)
    pesan = models.TextField()
    waktu_kirim = models.DateTimeField(auto_now_add=True)
    sudah_dibaca = models.BooleanField(default=False)

    class Meta:
        ordering = ["-waktu_kirim"]
        verbose_name = "Pesan Masuk"
        verbose_name_plural = "Pesan Masuk"

    def __str__(self):
        return f"{self.subjek} - {self.nama}"


# 9. Tautan terkait
class TautanTerkait(models.Model):
    nama = models.CharField(max_length=150)
    url = models.URLField()
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["urutan", "nama"]
        verbose_name = "Tautan Terkait"
        verbose_name_plural = "Tautan Terkait"

    def __str__(self):
        return self.nama
