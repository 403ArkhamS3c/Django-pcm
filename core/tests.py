from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Berita, PesanMasuk


class PencarianBeritaTest(TestCase):
    def setUp(self):
        kemarin = timezone.now() - timedelta(days=1)
        Berita.objects.create(
            judul="Pengajian Akbar", ringkasan="r", isi="i",
            status="terbit", tanggal_terbit=kemarin,
        )
        Berita.objects.create(
            judul="Bakti Sosial", ringkasan="r", isi="i",
            status="terbit", tanggal_terbit=kemarin,
        )
        self.draf = Berita.objects.create(
            judul="Pengajian Draf", ringkasan="r", isi="i",
            status="draf", tanggal_terbit=kemarin,
        )

    def test_pencarian_hanya_berita_terbit_yang_cocok(self):
        res = self.client.get(reverse("core:berita"), {"q": "Pengajian"})
        self.assertContains(res, "Pengajian Akbar")
        self.assertNotContains(res, "Bakti Sosial")
        self.assertNotContains(res, "Pengajian Draf")

    def test_pencarian_tanpa_hasil_form_tetap_ada(self):
        res = self.client.get(reverse("core:berita"), {"q": "zzzxxx"})
        self.assertContains(res, "Berita Tidak Ditemukan")
        self.assertContains(res, 'name="q"')

    def test_detail_berita_draf_404(self):
        res = self.client.get(
            reverse("core:detail_berita", args=[self.draf.slug])
        )
        self.assertEqual(res.status_code, 404)

    def test_detail_berita_masa_depan_404(self):
        besok = Berita.objects.create(
            judul="Besok", ringkasan="r", isi="i", status="terbit",
            tanggal_terbit=timezone.now() + timedelta(days=1),
        )
        res = self.client.get(
            reverse("core:detail_berita", args=[besok.slug])
        )
        self.assertEqual(res.status_code, 404)


class HalamanPublikTest(TestCase):
    def test_semua_halaman_publik_200(self):
        for nama in [
            "home", "profil", "pimpinan", "ranting", "amal_usaha",
            "berita", "agenda", "unduhan", "pesan_masuk",
        ]:
            res = self.client.get(reverse(f"core:{nama}"))
            self.assertEqual(res.status_code, 200, nama)


class FormulirKontakTest(TestCase):
    def test_pesan_tersimpan(self):
        res = self.client.post(reverse("core:pesan_masuk"), {
            "nama": "Budi",
            "email": "budi@example.com",
            "subjek": "Tanya kegiatan",
            "pesan": "Kapan pengajian berikutnya diadakan?",
        })
        self.assertEqual(res.status_code, 302)
        self.assertEqual(PesanMasuk.objects.count(), 1)

    def test_pesan_terlalu_pendek_ditolak(self):
        res = self.client.post(reverse("core:pesan_masuk"), {
            "nama": "Budi",
            "email": "budi@example.com",
            "subjek": "Tes",
            "pesan": "pendek",
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(PesanMasuk.objects.count(), 0)