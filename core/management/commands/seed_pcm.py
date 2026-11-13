from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.db import transaction
from django.utils.text import slugify
from datetime import datetime
from django.utils import timezone

from core.models import (
    ProfilOrganisasi,
    Pimpinan,
    Ranting,
    AmalUsaha,
    Berita,
    Agenda,
    Dokumen,
    TautanTerkait,
    SambutanKetua,
    GaleriKegiatan,
)


PROFIL = None
PROFIL = {
    "nama": "Pimpinan Cabang Muhammadiyah Grogol",
    "nama_singkat": "PCM Grogol",
    "tagline": "Ranting Penting, Cabang Berkembang, Masjid Makmur Memakmurkan",
    "tentang": (
        "Pimpinan Cabang Muhammadiyah (PCM) Grogol merupakan organisasi "
        "persyarikatan Muhammadiyah yang bergerak dalam bidang dakwah Islam, "
        "pendidikan, sosial, dan pemberdayaan masyarakat di wilayah Kecamatan "
        "Grogol, Kabupaten Sukoharjo. PCM Grogol berperan dalam mengoordinasikan "
        "dan membina Pimpinan Ranting Muhammadiyah serta mengembangkan berbagai "
        "amal usaha sebagai wujud nyata pengabdian kepada masyarakat. Melalui "
        "kegiatan keagamaan, pendidikan, sosial, dan penguatan organisasi, PCM "
        "Grogol berupaya mewujudkan masyarakat Islam yang sebenar-benarnya "
        "serta menghadirkan manfaat bagi umat dan lingkungan sekitar."
    ),
    "sejarah":( 
                "Perjalanan Muhammadiyah di wilayah Grogol telah dimulai sejak sekitar tahun 1960-an. Pada awal berdirinya, Muhammadiyah Grogol masih berbentuk Pimpinan Ranting Muhammadiyah Grogol yang berada di bawah koordinasi Cabang Muhammadiyah Solo Selatan, dalam wilayah Pimpinan Daerah Muhammadiyah Kotamadya Surakarta.\n"
                "Pada masa awal tersebut, kepemimpinan Muhammadiyah Grogol dipimpin oleh Bapak H. Syatibi, yang saat itu bekerja sebagai pegawai Departemen Agama Surakarta. Kepemimpinan kemudian dilanjutkan oleh Bapak Dirjo yang menjabat sebagai Penghulu Kantor Urusan Agama (KUA) Kecamatan Grogol. Setelah itu, kepemimpinan diteruskan oleh Bapak M. Sadzali, seorang pegawai KUA sekaligus mubalig.\n"
                "Selanjutnya, kepemimpinan Muhammadiyah Grogol dilanjutkan oleh Bapak Dwijo Wiryono sebagai ketua dengan Bapak H. Katibi sebagai sekretaris.\n"
                "Pada tahun 1970, terjadi perubahan kedudukan organisasi seiring dengan penyesuaian wilayah administratif. Secara geografis, Kecamatan Grogol merupakan bagian dari Kabupaten Sukoharjo. Oleh karena itu, Muhammadiyah Grogol kemudian berdiri sebagai Pimpinan Cabang Muhammadiyah (PCM) Grogol yang berada di bawah koordinasi Pimpinan Daerah Muhammadiyah Kabupaten Sukoharjo.\n"
                "Dalam perjalanan selanjutnya, PCM Grogol terus mengalami pergantian kepemimpinan. Pada periode berikutnya, organisasi dipimpin oleh Bapak Drs. M. Qisti dengan Bapak H. Katibi sebagai sekretaris. Kepemimpinan kemudian dilanjutkan oleh Bapak Ahmad Husen, disusul Bapak Muhyidin, yang keduanya didampingi oleh Bapak H. Katibi sebagai sekretaris.\n"
                "Pada periode selanjutnya, PCM Grogol dipimpin oleh Bapak Rachmadi Raharjo dengan Bapak Supomo sebagai sekretaris.\n"
                "Memasuki perkembangan organisasi pada masa yang lebih modern, PCM Grogol dipimpin oleh Bapak Dr. Sri Lahir, M.Pd. pada periode 2015–2022 dengan Bapak M. Safrudin sebagai sekretaris.\n"
                "Selanjutnya, berdasarkan hasil Musyawarah Cabang Muhammadiyah dalam rangkaian Muktamar Muhammadiyah ke-48, kepemimpinan PCM Grogol periode 2022–2027 dipercayakan kepada Bapak Agus Komarudin sebagai ketua dengan Bapak M. Safrudin sebagai sekretaris.\n"
                "Perjalanan panjang tersebut menjadi bagian dari sejarah perkembangan Muhammadiyah di Kecamatan Grogol. Dari sebuah ranting yang tumbuh pada tahun 1960-an hingga menjadi Pimpinan Cabang Muhammadiyah yang berdiri sendiri, PCM Grogol terus berupaya melanjutkan dakwah dan gerakan persyarikatan melalui berbagai bidang kehidupan masyarakat.\n"
               ),
    "visi": "Sebagai Gerakan Islam yang berlandaskan pada Al-Qur’an dan As-Sunnah dengan watak tajdid yang dimilikinya senantiasa istiqamah dan aktif dalam melaksanakan Dakwah Islam Amar Ma’ruf  Nahi Munkar di segala bidang sehingga menjadi rahmatan li al-’alamin bagi umat, bangsa, dan dunia kemanusiaan menuju terciptanya Masyarakat Utama yang diridhai Allah Subhanahu Wata’ala dalam kehidupan di dunia ini.",
    "misi": (
            "Menegakkan keyakinan tauhid yang murni sesuai dengan ajaran Allah SWT, yang dibawa oleh Rasul Allah yang disyariatkan sejak Nabi Nuh AS hingga Nabi Muhammad SAW.\n"
            "Memahami agama dengan menggunakan akal pikiran sesuai dengan jiwa ajaran Islam untuk menjawab dan menyelesaikan persoalan-persoalan kehidupan yang bersifat duniawi.\n"
            "Menyebarluaskan ajaran Islam yang bersumber kepada Al-Qur’an sebagai kitab Allah yang terakhir untuk umat manusia dan Sunnah Rasul.\n"
            "Mewujudkan amalan-amalan Islam dalam kehidupan pribadi, keluarga, dan masyarakat.\n"),
    "alamat_sekretariat": "Jl. Raya Solo Baru No. 62 A Madegondo, Grogol, Sukoharjo, Jawa Tengah",
    "telepon": "0811 2634 335 (Safruddin)",
    "email": None,
    "jumlah_anggota_ktam": 27,
    "gambar_utama": "profile/pcm.png",
}


PIMPINAN = [
    # 1. PIMPINAN CABANG

    # Ketua
    {
        "nama": "Agus Komarudin",
        "jabatan": "Ketua",
        "periode": "Periode ke-48",
        "foto": "pimpinan/agus.png",
        "urutan_tampil": 1,
    },

    # Wakil Ketua
    {
        "nama": "Sodiq, S.Psi., S.Pd.I.",
        "jabatan": "Wakil Ketua 1",
        "periode": "Periode ke-48",
        "foto": "pimpinan/sodiq.png",
        "urutan_tampil": 2,
    },
    {
        "nama": "Drs. Asyhuri, M.Ag.",
        "jabatan": "Wakil Ketua 2",
        "periode": "Periode ke-48",
        "foto": "pimpinan/asyhuri.png",
        "urutan_tampil": 3,
    },
    {
        "nama": "Dr. Edy Muslimin, S.Ag., M.Si.",
        "jabatan": "Wakil Ketua 3",
        "periode": "Periode ke-48",
        "foto": "pimpinan/edy_muslimin.png",
        "urutan_tampil": 4,
    },
    {
        "nama": "Ngadiyono, S.Pd",
        "jabatan": "Wakil Ketua 4",
        "periode": "Periode ke-48",
        "foto": "pimpinan/ngadiyono.png",
        "urutan_tampil": 5,
    },
    {
        "nama": "Tumirah, S.Pd.I",
        "jabatan": "Wakil Ketua 5",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 6,
    },

    # Sekretaris
    {
        "nama": "Muhamad Safrudin",
        "jabatan": "Sekretaris",
        "periode": "Periode ke-48",
        "foto": "pimpinan/safrudin.png",
        "urutan_tampil": 7,
    },

    # Wakil Sekretaris
    {
        "nama": "Slamet Untoro, S.Pd.I",
        "jabatan": "Wakil Sekretaris",
        "periode": "Periode ke-48",
        "foto": "pimpinan/slamet_untoro.png",
        "urutan_tampil": 8,
    },

    # Bendahara
    {
        "nama": "Sukemi Budi Utomo",
        "jabatan": "Bendahara",
        "periode": "Periode ke-48",
        "foto": "pimpinan/sukemi.png",
        "urutan_tampil": 9,
    },

    # Wakil Bendahara
    {
        "nama": "Drs. Ahmad Haris Munandar",
        "jabatan": "Wakil Bendahara",
        "periode": "Periode ke-48",
        "foto": "pimpinan/ahmad_haris.png",
        "urutan_tampil": 10,
    },

    # Penasehat
    {
        "nama": "H. Katibi, S.Pd",
        "jabatan": "Penasehat",
        "periode": "Periode ke-48",
        "foto": "pimpinan/katibi.png",
        "urutan_tampil": 11,
    },
    {
        "nama": "Muhyiddin, S.Ag",
        "jabatan": "Penasehat",
        "periode": "Periode ke-48",
        "foto": "pimpinan/muhyiddin.png",
        "urutan_tampil": 12,
    },
    {
        "nama": "H. Ahmad Djazim Djuwairi, BA",
        "jabatan": "Penasehat",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 13,
    },
    {
        "nama": "H. Rahmadi Raharjo",
        "jabatan": "Penasehat",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 14,
    },
    {
        "nama": "H. Dr. Sri Lahir, M.Pd",
        "jabatan": "Penasehat",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 15,
    },
    # 2. MAJELIS TARJIH DAN TAJDID
    {
        "nama": "Suhaji, S.Pd.I.",
        "jabatan": "Ketua (Majelis Tarjih dan Tajdid)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/suhaji.png",
        "urutan_tampil": 16,
    },
    {
        "nama": "Drs. Muis Lidinillah",
        "jabatan": "Sekretaris (Majelis Tarjih dan Tajdid)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/muis.png",
        "urutan_tampil": 17,
    },
    {
        "nama": "Syamsudin",
        "jabatan": "Anggota Majelis Tarjih dan Tajdid",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 18,
    },
    {
        "nama": "Fatkhurohman, S.Pd.",
        "jabatan": "Anggota Majelis Tarjih dan Tajdid",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 19,
    },
    {
        "nama": "Saubari, S.Pd.",
        "jabatan": "Anggota Majelis Tarjih dan Tajdid",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 20,
    },
    # 3. MAJELIS TABLIGH
    {
        "nama": "Muh. Fatahillah Suparman, Spdi, MPsi",
        "jabatan": "Ketua (Majelis Tabligh)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/fatahillah.png",
        "urutan_tampil": 21,
    },
    {
        "nama": "Dr. Mulyanto Abdullah Khoir, M.Ag.",
        "jabatan": "Sekretaris Majelis Tabligh",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 22,
    },
    {
        "nama": "Drs. Joko Dwi Haryanto",
        "jabatan": "Anggota Majelis Tabligh",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 23,
    },
    {
        "nama": "Eko Wicaksono, S.Pd.",
        "jabatan": "Anggota Majelis Tabligh",
        "periode": "Periode ke-48",
        "foto": "pimpinan/wicaksono.png",
        "urutan_tampil": 24,
    },
    {
        "nama": "Muh. Fadly, S.Pd",
        "jabatan": "Anggota (Majelis Tabligh)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/faldy.png",
        "urutan_tampil": 25,
    },
    {
        "nama": "Supomo, S.Ag.",
        "jabatan": "Anggota (Majelis Tabligh)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/supomo.png",
        "urutan_tampil": 26,
    },
    # 4. MAJELIS PKU DAN MPKS
    {
        "nama": "Joko Rumiarso, S.Pd.",
        "jabatan": "Ketua (Majelis PKU & MPKS)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/joko_rumiarso.png",
        "urutan_tampil": 27,
    },
    {
        "nama": "Abdullah Maknawi",
        "jabatan": "Sekretaris Majelis PKU dan MPKS",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 28,
    },
    {
        "nama": "Murjanto",
        "jabatan": "Anggota Majelis PKU dan MPKS",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 29,
    },
    {
        "nama": "Ihvan Syakur",
        "jabatan": "Anggota Majelis PKU dan MPKS",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 30,
    },
    # 5. MAJELIS DIKDASMEN
    {
        "nama": "Muhammad Islam, S.Ag., M.Pd.",
        "jabatan": "Ketua Majelis Dikdasmen",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 31,
    },
    {
        "nama": "Miftah Farid, S.Pd., M.Pd.",
        "jabatan": "Sekretaris Majelis Dikdasmen",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 32,
    },
    {
        "nama": "Amat Sabar. S.Pd. Eng.",
        "jabatan": "Anggota (Majelis Dikdasmen)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/amat_sabar.png",
        "urutan_tampil": 33,
    },
    {
        "nama": "Widayat, S.Pd.",
        "jabatan": "Anggota Majelis Dikdasmen",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 34,
    },
    {
        "nama": "Supardi, S.Pd., M.Si.",
        "jabatan": "Anggota Majelis Dikdasmen",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 35,
    },
    {
        "nama": "Almuntaqo Zain, M.Pd.",
        "jabatan": "Anggota Majelis Dikdasmen",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 36,
    },
    {
        "nama": "Muhammad Toyib, M.Pd.",
        "jabatan": "Anggota Majelis Dikdasmen",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 37,
    },
    # 6. MAJELIS PENDIDIKAN KADER DAN PEMBERDAYAAN RANTING
    {
        "nama": "Supriyadi",
        "jabatan": "Ketua (Majelis Pend. Kader & Pemberdayaan Ranting)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/supriyadi.png",
        "urutan_tampil": 38,
    },
    {
        "nama": "Alim Saleh STh.I MPd",
        "jabatan": "Sekretaris (Majelis Pend. Kader & Pemberdayaan Ranting)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/alim_saleh.png",
        "urutan_tampil": 39,
    },
    {
        "nama": "Tohari",
        "jabatan": "Anggota Majelis Pendidikan Kader dan Pemberdayaan Ranting",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 40,
    },
    {
        "nama": "Damsuki",
        "jabatan": "Anggota Majelis Pendidikan Kader dan Pemberdayaan Ranting",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 41,
    },
    {
        "nama": "Fajar Nur Ihsan",
        "jabatan": "Anggota Majelis Pendidikan Kader dan Pemberdayaan Ranting",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 42,
    },
    # 7. MAJELIS PI DAN SENI BUDAYA
    {
        "nama": "Winarto, S.Kom.",
        "jabatan": "Ketua (Majelis PI & Seni Budaya)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/winarto.png",
        "urutan_tampil": 43,
    },
    {
        "nama": "Uut Prihonggo, S.Pd.",
        "jabatan": "Sekretaris Majelis PI dan Seni Budaya",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 44,
    },
    {
        "nama": "Bowo Yudha Prasetyo, S.Pd.",
        "jabatan": "Anggota Majelis PI dan Seni Budaya",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 45,
    },
    {
        "nama": "Heri Susanto",
        "jabatan": "Anggota Majelis PI dan Seni Budaya",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 46,
    },
    {
        "nama": "Kasto",
        "jabatan": "Anggota Majelis PI dan Seni Budaya",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 47,
    },
    {
        "nama": "Wahyu Tri S.",
        "jabatan": "Anggota Majelis PI dan Seni Budaya",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 48,
    },
    {
        "nama": "Mi'roj Zaeni Isymaya, S.Pd.I.",
        "jabatan": "Anggota (Majelis PI & Seni Budaya)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/zaini_ismaya.png",
        "urutan_tampil": 49,
    },
    # 8. MAJELIS EKONOMI
    {
        "nama": "Santoso",
        "jabatan": "Ketua Majelis Ekonomi",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 50,
    },
    {
        "nama": "Muh. Imam Wicaksono, M.Ling.",
        "jabatan": "Sekretaris (Majelis Ekonomi)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 51,
    },
    {
        "nama": "Sambodo, SE.",
        "jabatan": "Anggota Majelis Ekonomi",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 52,
    },
    {
        "nama": "Muhammad Sodri",
        "jabatan": "Anggota Majelis Ekonomi",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 53,
    },
    {
        "nama": "Budi Suprayitna",
        "jabatan": "Anggota Majelis Ekonomi",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 54,
    },
    {
        "nama": "Mukimin Mursyid",
        "jabatan": "Anggota Majelis Ekonomi",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 55,
    },
    # 9. MAJELIS WAKAF DAN KEBENDAHARAAN
    {
        "nama": "Muh. Taufik Darmawan, S.HI.",
        "jabatan": "Ketua (Majelis Wakaf & Kebendaharaan)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/taufik.png",
        "urutan_tampil": 56,
    },
    # 10. LEMBAGA PEMBINAAN DAN PENGAWASAN KEUANGAN
    {
        "nama": "Ir. Djarwo Sukarno, MM",
        "jabatan": "Ketua Lembaga Pembinaan dan Pengawasan Keuangan",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 57,
    },
    {
        "nama": "Jamil Kasiman, SE., M.Si.",
        "jabatan": "Sekretaris (Lembaga Pembinaan & Pengawasan Keuangan)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/jamil_kasiman.png",
        "urutan_tampil": 58,
    },
    {
        "nama": "Marjono, BA.",
        "jabatan": "Anggota Lembaga Pembinaan dan Pengawasan Keuangan",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 59,
    },
    {
        "nama": "Ir. Ifwan Noerdin Chaniago",
        "jabatan": "Anggota Lembaga Pembinaan dan Pengawasan Keuangan",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 60,
    },
    {
        "nama": "Rasyid Ari Nugroho, SE., M.Ak.",
        "jabatan": "Anggota Lembaga Pembinaan dan Pengawasan Keuangan",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 61,
    },
    # 11. LEMBAGA LAZISMU
    {
        "nama": "M. Abduh Suryo H.",
        "jabatan": "Ketua Lembaga LAZISMU",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 62,
    },
    {
        "nama": "Supriyono, S.Pd.",
        "jabatan": "Sekretaris (Lembaga LAZISMU)",
        "periode": "Periode ke-48",
        "foto": "pimpinan/supriyono.png",
        "urutan_tampil": 63,
    },
    {
        "nama": "Joko Yuwono",
        "jabatan": "Anggota Lembaga LAZISMU",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 64,
    },
    {
        "nama": "Cahyo Murdiono",
        "jabatan": "Anggota Lembaga LAZISMU",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 65,
    },
    {
        "nama": "Wahyu Saputra",
        "jabatan": "Anggota Lembaga LAZISMU",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 66,
    },
    # 12. LEMBAGA LPB
    {
        "nama": "Suhardi",
        "jabatan": "Ketua Lembaga LPB",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 67,
    },
    {
        "nama": "Budi Prihanto",
        "jabatan": "Sekretaris Lembaga LPB",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 68,
    },
    {
        "nama": "Jarno",
        "jabatan": "Anggota Lembaga LPB",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 69,
    },
    {
        "nama": "Margiyanto",
        "jabatan": "Anggota Lembaga LPB",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 70,
    },
    {
        "nama": "Aminuddin",
        "jabatan": "Anggota Lembaga LPB",
        "periode": "Periode ke-48",
        "foto": "pimpinan/defaul.png",
        "urutan_tampil": 71,
    },
    # 13. JABATAN BELUM DIKETAHUI
    {
        "nama": "Arkanudin Rizki Permono.",
        "jabatan": "-",
        "periode": "-",
        "foto": "pimpinan/rizki_permono.png",
        "urutan_tampil": 72,
    },
]

RANTING = [
    {
        "nama_ranting": "Ranting Pondok",
        "ketua": "Drs. Joko Dwi Haryanto",
        "alamat": "Balai Desa Pondok, Jl. Raya Temulus, Desa Pondok, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah 57552",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Cemani",
        "ketua": "Jamil Kasiman, S.E., M.Si.",
        "alamat": "Balai Desa Cemani, Jl. Batik Keris, Desa Cemani, Kec. Grogol, Kab. Sukoharjo",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Waringinrejo",
        "ketua": "-",
        "alamat": "-",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Madegondo",
        "ketua": "Almuntaqo Zainuddin, M.Pd.",
        "alamat": "Balai Desa Madegondo, Jl. Raya Grogol No. 58, Dusun II, Madegondo, Grogol, Sukoharjo, 57552",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Telukan",
        "ketua": "-",
        "alamat": "Kantor Desa Telukan, Jl. Raya Telukan No. 60, Telukan, Grogol, Sukoharjo",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Grogol",
        "ketua": "-",
        "alamat": "Balai Desa Grogol, Jl. Grogol No. 134, Kec. Grogol, Sukoharjo",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Kadokan",
        "ketua": "-",
        "alamat": "Balai Desa Kadokan, Jl. Raya Kadokan No. 01, RT 01/RW 03, Kadokan, Grogol, Sukoharjo",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Parangjoro",
        "ketua": "-",
        "alamat": "Jl. Telukan-Cuplik Km 2,5, Dukuh Singkil RT 003/RW 008, Desa Parangjoro, Grogol, Sukoharjo",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Sanggrahan",
        "ketua": "Dr. Mulyanto Abdullah Khoir",
        "alamat": "Balai Desa Sanggrahan, Jl. Palagan Tentara Pelajar, Sanggrahan, Grogol, Sukoharjo",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Banaran",
        "ketua": "-",
        "alamat": "Balai Desa Banaran, Jl. Merapi No. 29, Banaran, Grogol, Sukoharjo, 57552",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Langenharjo",
        "ketua": "-",
        "alamat": "Balai Desa Langenharjo, Jl. Suwarno Honggopati No. 2, Dusun I, Langenharjo, Grogol, Sukoharjo, 57552",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Gedangan",
        "ketua": "-",
        "alamat": "Balai Desa Gedangan, Jl. Duren No. 18, Gedangan, Grogol, Sukoharjo",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Pandeyan",
        "ketua": "-",
        "alamat": "Balai Desa Pandeyan, Dukuh Pandeyan RT 04/RW 03, Desa Pandeyan, Grogol, Sukoharjo",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Manang",
        "ketua": "-",
        "alamat": "Balai Desa Manang, Jl. Raya Manang-Baki No. 01, Manang, Grogol, Sukoharjo, 57552",
        "telepon": "-",
    },
    {
        "nama_ranting": "Ranting Kwarasan",
        "ketua": "-",
        "alamat": "Balai Desa Kwarasan, Jl. Lempuyang 1, Munyung, Kwarasan, Grogol, Sukoharjo",
        "telepon": "-",
    },
]
AMAL_USAHA = [
    {
        "nama": "Panti Asuhan Yatim Muhammadiyah Grogol",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "deskripsi": "Lembaga Kesejahteraan Sosial Anak milik Muhammadiyah yang berdiri pada tahun 1995. Panti ini bergerak dalam bidang sosial dan keagamaan melalui kegiatan pengasuhan, pendidikan, pembinaan keislaman, serta pengembangan kemandirian anak yatim dan dhuafa. Lembaga ini secara khusus menerima anak asuh laki-laki.",
        "alamat": "Telukan RT 02/RW 01, Desa Telukan, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/panti1.png",
    },
    {
        "nama": "Panti Asuhan Yatim Putri Aisyiyah",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "deskripsi": "Lembaga Kesejahteraan Sosial Anak yang dikelola oleh Aisyiyah dan bergerak dalam pelayanan sosial serta pengasuhan anak yatim putri. Panti Asuhan Yatim Putri Aisyiyah Grogol tercatat berdiri pada 1 Juli 1999 sebagai bagian dari kiprah Aisyiyah dalam bidang sosial dan kemanusiaan.",
        "alamat": "Jl. Nusa Indah/Panirejo RT 02/RW 03, Grogol, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/panti2.png",
    },
    {
        "nama": "Madrasah Ibtidaiyah Muhammadiyah Grogol",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "deskripsi": "Lembaga pendidikan dasar Islam di bawah naungan Yayasan Pimpinan Daerah Muhammadiyah Kabupaten Sukoharjo. Madrasah ini menyelenggarakan pendidikan pada jenjang ibtidaiyah dengan mengintegrasikan pembelajaran umum dan pendidikan agama Islam. Dalam data resmi Kemendikdasmen, lembaga ini tercatat dengan nama MI Muhammadiyah Dimoro dan memiliki akreditasi A.",
        "alamat": "Sudimoro RT 03/RW 10, Desa Parangjoro, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/madrasah1.png",
    },
    {
        "nama": "Madrasah Tsanawiyah Muhammadiyah Grogol",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "deskripsi": "Lembaga pendidikan Islam tingkat menengah pertama yang berada di bawah naungan Yayasan Pimpinan Daerah Muhammadiyah Kabupaten Sukoharjo. Madrasah ini menyelenggarakan pendidikan jenjang tsanawiyah dengan perpaduan pembelajaran umum dan pendidikan agama Islam. MTs Muhammadiyah Grogol tercatat berdiri pada tahun 1985 dan memiliki akreditasi B.",
        "alamat": "Dimoro RT 03/RW 10, Desa Parangjoro, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/madrasah2.png",
    },
    {
        "nama": "TK/BA AISYIYAH 1 Grogol",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "deskripsi": "Lembaga pendidikan anak usia dini yang dikelola oleh Aisyiyah melalui satuan pendidikan Bustanul Athfal. Lembaga ini memberikan layanan pendidikan dasar bagi anak usia dini sebagai tahap awal pengembangan kemampuan, pembentukan karakter, serta pengenalan nilai-nilai keislaman.",
        "alamat": "Jl. Maya, Dukuh Sanggrahan RT 04/RW 01, Desa Grogol, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/defaul.png",
    },
    {
        "nama": "TK/BA AISYIYAH 2 Grogol",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "deskripsi": "Satuan pendidikan Bustanul Athfal yang dikelola oleh Aisyiyah untuk memberikan pendidikan anak usia dini. Kegiatan pendidikannya ditujukan untuk membantu perkembangan anak melalui pembelajaran dasar, pembiasaan perilaku positif, serta pengenalan nilai-nilai agama Islam.",
        "alamat": "Soko RT 02/RW 03, Desa Madegondo, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/aisyiyah2.png",
    },
    {
        "nama": "TK/BA AISYIYAH 3 Grogol",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "deskripsi": "Lembaga pendidikan anak usia dini berbentuk Bustanul Athfal yang berada di lingkungan Aisyiyah. Lembaga ini menyelenggarakan pendidikan awal untuk mendukung perkembangan kemampuan dasar, pembentukan karakter, dan penanaman nilai-nilai keislaman pada anak.",
        "alamat": "Sudimoro RT 01/RW 10, Desa Parangjoro, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/aisyiyah3.png",
    },
    {
        "nama": "TK/BA AISYIYAH 4 Grogol",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "deskripsi": "Satuan pendidikan anak usia dini yang dikelola oleh Aisyiyah melalui pendidikan Bustanul Athfal. Lembaga ini berperan dalam memberikan pendidikan dasar bagi anak usia dini melalui pengembangan kemampuan awal, pembiasaan akhlak yang baik, dan pengenalan ajaran Islam.",
        "alamat": "Gatak RT 02/RW 05, Desa Madegondo, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/aisyiyah4.png",
    },
    {
        "nama": "TK/BA AISYIYAH 5 Grogol",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "deskripsi": "Lembaga pendidikan anak usia dini berbentuk Bustanul Athfal di bawah pengelolaan Aisyiyah. Lembaga ini memberikan layanan pendidikan awal untuk membantu perkembangan anak, membangun kebiasaan positif, serta mengenalkan nilai-nilai keagamaan sejak usia dini.",
        "alamat": "Mupusan RT 03/RW 05, Desa Pondok, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/aisyiyah5.png",
    },
    {
        "nama": "TK/BA AISYIYAH 6 Grogol",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "deskripsi": "Satuan pendidikan Bustanul Athfal yang dikelola oleh Aisyiyah dan melayani pendidikan anak usia dini. Pendidikan diarahkan pada pengembangan kemampuan dasar, pembentukan perilaku positif, serta pengenalan nilai-nilai keislaman sebagai bekal perkembangan anak.",
        "alamat": "Manggaran RT 02/RW 06, Desa Pondok, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/aisyiyah6.png",
    },
    {
        "nama": "TK/BA AISYIYAH 7 Grogol",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "deskripsi": "Lembaga pendidikan anak usia dini berbentuk Bustanul Athfal di lingkungan Aisyiyah. Lembaga ini menyelenggarakan pendidikan awal yang mendukung perkembangan anak melalui pembelajaran dasar, pembiasaan akhlak, dan pengenalan nilai-nilai agama Islam.",
        "alamat": "Ngrantan RT 01/RW 01, Desa Kadokan, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/aisyiyah7.png",
    },
    {
        "nama": "TK/BA AISYIYAH 8 Grogol",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "deskripsi": "Satuan pendidikan Bustanul Athfal yang dikelola oleh Aisyiyah sebagai bagian dari pelayanan pendidikan anak usia dini. Lembaga ini berperan dalam memberikan pendidikan awal, mengembangkan kemampuan dasar anak, serta membiasakan perilaku dan nilai-nilai keislaman.",
        "alamat": "Mantung RT 04/RW 05, Desa Sanggrahan, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/defaul.png",
    },
    {
        "nama": "TK/BA AISYIYAH 9 Grogol",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "deskripsi": "Lembaga pendidikan anak usia dini berbentuk Bustanul Athfal yang berada di bawah pengelolaan Aisyiyah. Lembaga ini memberikan layanan pendidikan awal untuk mendukung perkembangan kemampuan dasar, pembentukan karakter, dan penanaman nilai-nilai agama Islam.",
        "alamat": "Tegalsari RT 04/RW 05, Desa Langenharjo, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/defaul.png",
    },
    {
        "nama": "TK/BA AISYIYAH Qurrata A'yun Grogol",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "deskripsi": "Lembaga pendidikan anak usia dini yang dikelola dalam lingkungan pendidikan Muhammadiyah dan Aisyiyah. TK Aisyiyah Qurrata A'yun memberikan layanan pendidikan bagi anak usia dini untuk mendukung perkembangan kemampuan dasar, pembentukan karakter, dan pengenalan nilai-nilai keislaman. Lembaga ini tercatat memiliki izin operasional sejak tahun 2018.",
        "alamat": "Temulus RT 003/RW 003, Desa Pondok, Kec. Grogol, Kab. Sukoharjo, Jawa Tengah",
        "gambar": "amal_usaha/qurata.png",
    },
]



BERITA = [
    {
        "judul": "LKSA Panti Asuhan Yatim Putri 'Aisyiyah Kukuhkan Pengurus dan Susun Program Kerja",
        "ringkasan": (
            "LKSA Panti Asuhan Yatim Putri 'Aisyiyah Grogol "
            "menggelar pengukuhan pengurus dan rapat kerja "
            "periode 2026–2031 untuk memperkuat tata kelola "
            "dan meningkatkan kualitas pelayanan kepada anak asuh."
        ),
        "isi": """
        Lembaga Kesejahteraan Sosial Anak (LKSA) Panti Asuhan
        Yatim Putri 'Aisyiyah Grogol menyelenggarakan kegiatan
        pengukuhan dan rapat kerja pengurus pada Ahad,
        13 September 2026. Kegiatan berlangsung di Aula
        LKSA Panti Asuhan Yatim Putri 'Aisyiyah Grogol.

        Kegiatan ini menjadi momentum untuk memperkuat
        kepengurusan sekaligus menyusun program kerja
        periode 2026–2031. Acara dihadiri oleh jajaran
        Pimpinan 'Aisyiyah, pengurus panti, pembina,
        pengasuh, serta unsur yang terlibat dalam
        pengelolaan lembaga.

        Ketua PCM Grogol, Agus Qomarudin, yang hadir
        sebagai penasihat, mengingatkan pentingnya
        menjalankan amanah organisasi sesuai aturan
        persyarikatan dengan penuh keikhlasan dan
        profesionalitas.

        Ketua pengurus, Sri Suwarni, S.Pd., juga
        menekankan bahwa anak asuh merupakan amanah
        yang harus dibimbing dan didampingi dengan
        ketulusan serta keteladanan.

        Rapat kerja membahas sejumlah program, meliputi
        pengasuhan, pendidikan, keagamaan, kesehatan,
        kemandirian anak, pengembangan sumber daya manusia,
        administrasi, serta pengelolaan sumber dana.

        Melalui kepengurusan dan program kerja yang
        terarah, LKSA berharap dapat terus meningkatkan
        kualitas pelayanan dan pembinaan anak asuh.
        """,
        "gambar_sampul": "berita/panti1.png",
        "tanggal_terbit": timezone.make_aware(
            datetime(2026, 9, 13, 9, 0)
        ),
        "status": "terbit",
    },
    {
            "judul": "LKSA PAYPA Grogol Gelar Temu Anak dan Orang Tua, Perkuat Komunikasi Keluarga",
            "ringkasan": (
                "LKSA Panti Asuhan Yatim Putri 'Aisyiyah Grogol "
                "mengadakan temu penguatan kapasitas anak dan "
                "keluarga yang diikuti sekitar 120 peserta. "
                "Kegiatan ini membahas pentingnya komunikasi "
                "efektif antara anak, orang tua, dan pengasuh."
            ),
            "isi": """
            LKSA Panti Asuhan Yatim Putri 'Aisyiyah (PAYPA)
            Grogol, Sukoharjo, menyelenggarakan kegiatan
            Temu Penguatan Kapasitas Anak dan Keluarga pada
            Ahad, 21 Juni 2026. Kegiatan berlangsung di Aula
            LKSA PAYPA Grogol.
    
            Mengangkat tema Komunikasi Efektif antara Anak,
            Orang Tua, dan Pengasuh: Kunci Kedekatan dan
            Kepercayaan, kegiatan ini diikuti sekitar
            120 peserta yang terdiri dari anak asuh,
            calon anak asuh, orang tua, pengurus, dan
            tamu undangan.
    
            Ketua LKSA PAYPA, Sri Suwarni, menyampaikan
            pentingnya membangun komunikasi yang baik
            antara anak dan orang tua. Komunikasi yang
            terbuka diharapkan dapat memperkuat hubungan
            keluarga dan mencegah konflik dalam pengasuhan.
    
            Kegiatan dirangkai dengan wisuda Tahfidzul
            Qur'an, pelepasan penerima manfaat, serta
            penerimaan santriwati baru. Sebanyak enam
            santriwati memperoleh apresiasi atas capaian
            hafalan Al-Qur'an mulai dari satu hingga
            lima juz.
    
            Dalam sesi seminar, peserta memperoleh
            pemahaman mengenai pentingnya kerja sama
            antara keluarga dan lembaga pengasuhan
            dalam mendampingi perkembangan anak.
    
            Melalui kegiatan ini, LKSA PAYPA berharap
            hubungan antara anak, orang tua, dan
            pengasuh semakin erat sehingga tercipta
            lingkungan pengasuhan yang positif.
            """,
            "gambar_sampul": "berita/panti2",
            "tanggal_terbit": timezone.make_aware(
                datetime(2026, 6, 24, 9, 0)
            ),
            "status": "terbit",
        },
        {
            "judul": "PDPM Sukoharjo Bekali Anak Muda Jadi Dai yang Nasihatnya Sampai ke Hati",
            "ringkasan": (
            "Bidang Dakwah Pimpinan Daerah Pemuda Muhammadiyah (PDPM) Kabupaten Sukoharjo menyelenggarakan Diklat Dai Ramadhan Jilid #2 di MCC LKSA Yatim Putra Muhammadiyah Telukan. Kegiatan digelar Ahad (8/2/2026) dan diikuti oleh puluhan peserta muda baik putra maupun putri yang ingin mengasah kemampuan dakwah mereka."
            ),
            "isi": """
            Diklat kali ini mengusung tema “Jago Ngomong dari Hati ke Hati” dan menghadirkan dua pembicara ahli: Akhen Amalageng, Pembina Imtaq Shighor PK Isykarima, serta KH. Bimawan Syamsudin, S.P., Pembina Majelis Tabligh Pimpinan Daerah Muhammadiyah (PDM) Sukoharjo.

            Dalam sambutannya, Ketua PDPM Sukoharjo, H. Yusuf Aziz Rahma, S.Pd, M.M, memotivasi peserta dengan potongan hadis Nabi Muhammad saw: “Ballighu ‘anni walau ayah” (Sampaikan dariku walau hanya satu ayat).

            “Semoga semakin banyak anak-anak muda kita yang terjun menjadi dai, penyeru kebenaran Al-Qur’an dan Sunnah,” harap Aziz.

            Sementara itu, Ketua Bidang Dakwah PDPM Sukoharjo, Sodiq, S.Pd.I., S.Psi, menjelaskan bahwa program ini merupakan kolaborasi antara bidang dakwah yang ia pimpin dengan PCPM Grogol.

            “Kami hadir untuk memfasilitasi saudara/i semua agar menjadi dai yang nasihatnya sampai ke hati,” pungkas Sodiq.

            Kegiatan diklat ini diharapkan dapat mencetak generasi muda Muhammadiyah yang tidak hanya piawai dalam berbicara, tetapi juga mampu menyampaikan dakwah dengan ketulusan hati dan pengaruh positif bagi masyarakat.
            """,
            "gambar_sampul": "berita/diklat.png",
            "tanggal_terbit": timezone.make_aware(
                datetime(2026, 8, 2, 9, 0)
            ),
            "status": "terbit",
        },
        {
                "judul": "Kelola 8 SPPG, Mendag Budi Santoso Apresiasi Muhammadiyah Sukoharjo",
                "ringkasan": (
                    "Pimpinan Daerah Muhammadiyah (PDM) Kabupaten Sukoharjo menggelar Rapat Kerja Pimpinan (Rakerpim) di SM Tower Malioboro, Yogyakarta, Sabtu–Ahad (3–4 Januari 2026). Forum ini menjadi momentum strategis untuk memperkuat arah gerakan Muhammadiyah dalam memajukan dan menyejahterakan masyarakat Sukoharjo."
                ),
                "isi": """
                Rakerpim dibuka oleh Ketua Pimpinan Wilayah Muhammadiyah (PWM) Jawa Tengah, Kyai Tafsir. Ia menegaskan bahwa Muhammadiyah dituntut terus menghadirkan solusi nyata atas persoalan umat, salah satunya melalui penguatan ketahanan pangan yang berkelanjutan.

                Dengan mengusung tema “Memajukan dan Mensejahterakan Sukoharjo Melalui Ketahanan Pangan”, Rakerpim ini menempatkan sektor pangan sebagai pintu masuk pembangunan ekonomi dan sosial masyarakat.

                Kegiatan ini menghadirkan Menteri Perdagangan RI, Budi Santoso, sebagai narasumber melalui sambungan Zoom. Dalam pemaparannya yang bertajuk “Peran Muhammadiyah Bidang Perdagangan dalam Menyukseskan Pembangunan Bangsa”, Menteri Budi menilai Muhammadiyah memiliki jejaring kuat yang mampu menjadi motor penggerak ekonomi umat.

                Menteri Perdagangan mengapresiasi langkah PDM Sukoharjo yang telah mengelola delapan Satuan Pelayanan Pemenuhan Gizi (SPPG). Menurutnya, inisiatif tersebut merupakan contoh konkret kontribusi organisasi kemasyarakatan dalam memperkuat ketahanan pangan nasional.

                “Pengelolaan SPPG ini merupakan kontribusi konkret Muhammadiyah dalam memperkuat ketahanan pangan sekaligus ekonomi masyarakat,” ujar Menteri Budi.

                Delapan SPPG tersebut tersebar di berbagai unit Muhammadiyah, yakni SPPG PDA 1, SPPG PDA 2, SPPG Nguter, SPPG LKSA Grogol, SPPG PCM Baki, SPPG Imam Syuhodo, SPPG UMS Pabelan, serta SPPG RS PKU Muhammadiyah.

                Keberadaan SPPG tidak hanya berfungsi sebagai pusat pelayanan gizi, tetapi juga mampu menggerakkan ekonomi kerakyatan. SPPG dinilai dapat menjadi wadah penyerapan hasil pertanian lokal, sehingga produk petani memiliki pasar yang jelas dan berkelanjutan.

                Sebagai putra daerah Sukoharjo yang berasal dari Kelurahan Sonorejo, Kecamatan Sukoharjo, Menteri Budi Santoso juga mendorong agar UMKM binaan Muhammadiyah Sukoharjo terus dikembangkan. Ia berharap UMKM tersebut tidak hanya mampu mengisi pasar domestik, tetapi juga berani bersaing di pasar ekspor.

                Melalui Rakerpim ini, PDM Sukoharjo diharapkan mampu merumuskan kebijakan dan program kerja yang berdampak langsung bagi penguatan ekonomi umat serta peningkatan kesejahteraan masyarakat secara luas.
                """,
                "gambar_sampul": "berita/sppg.png",
                "tanggal_terbit": timezone.make_aware(
                    datetime(2026, 1, 3, 9, 0)
                ),
                "status": "terbit",
            },
    
]


AGENDA = [
    {
        "nama_kegiatan": "Pengajian Rutin Pimpinan Cabang dan Ranting Muhammadiyah Grogol setiap Senin malam Selasa.",
        "waktu_mulai": datetime(2026, 11, 9, 19, 30),
        "tempat": "-",
        "keterangan": "Kegiatan pengajian rutin yang diikuti oleh Pimpinan Cabang dan Pimpinan Ranting Muhammadiyah Grogol sebagai sarana pembinaan keagamaan, peningkatan pemahaman Islam, serta mempererat silaturahmi antaranggota persyarikatan.",
    },
    {
        "nama_kegiatan": "Pengajian Rutin Pimpinan Cabang dan Ranting Muhammadiyah dan Ortom beserta Guru dan Karyawan se-Kecamatan Grogol setiap Sabtu.",
        "waktu_mulai": datetime(2026, 11, 14, 19, 30),
        "tempat": "-",
        "keterangan": "Kegiatan pengajian rutin yang melibatkan unsur Pimpinan Cabang, Pimpinan Ranting, Organisasi Otonom Muhammadiyah, serta guru dan karyawan se-Kecamatan Grogol sebagai bentuk pembinaan keislaman dan penguatan ukhuwah di lingkungan persyarikatan.",
    },
    {
        "nama_kegiatan": "Pengajian Rutin setiap Ahad pagi jam 06.00–07.00 di Aula Panti Asuhan Yatim Muhammadiyah Telukan Grogol.",
        "waktu_mulai": datetime(2026, 11, 8, 6, 0),
        "tempat": "Aula Panti Asuhan Yatim Muhammadiyah, Telukan, Grogol, Sukoharjo",
        "keterangan": "Pengajian rutin setiap Ahad pagi yang dilaksanakan selama satu jam, mulai pukul 06.00 hingga 07.00 WIB. Kegiatan ini menjadi sarana pembinaan spiritual dan peningkatan pemahaman keagamaan bagi peserta pengajian.",
    },
    {
        "nama_kegiatan": "Pengajian Rutin setiap Ahad pagi jam 06.00–07.00 di Aula Panti Asuhan Yatim Putri 'Aisyiyah Grogol.",
        "waktu_mulai": datetime(2026, 11, 15, 6, 0),
        "tempat": "Aula Panti Asuhan Yatim Putri 'Aisyiyah, Grogol, Sukoharjo",
        "keterangan": "Pengajian rutin yang diselenggarakan setiap Ahad pagi pukul 06.00–07.00 WIB di aula panti asuhan. Kegiatan ini merupakan bagian dari aktivitas pembinaan keagamaan dan penguatan nilai-nilai Islam.",
    },
    {
        "nama_kegiatan": "Mengadakan Tarawih Keliling setiap Bulan Ramadan bersama Pimpinan Cabang Pemuda Muhammadiyah Grogol.",
        "waktu_mulai": datetime(2027, 2, 8, 19, 30),
        "tempat": "-",
        "keterangan": "Kegiatan ibadah Tarawih Keliling yang diselenggarakan setiap bulan Ramadan bersama Pimpinan Cabang Pemuda Muhammadiyah Grogol. Kegiatan ini bertujuan mempererat silaturahmi, meningkatkan kebersamaan, serta memperkuat ukhuwah Islamiyah di lingkungan Muhammadiyah.",
    },
]


DOKUMEN = [
{
    "judul": "SK Pendirian dan SK Kepengurusan",
    "keterangan": "Dokumen resmi yang memuat surat keputusan tentang pendirian organisasi Pimpinan Cabang Muhammadiyah Grogol serta penetapan susunan kepengurusan dan masa jabatannya.",
    "berkas": "dokumen/SK_PENDIRIAN_DAN_SK_KEPENGURUSAN.pdf",
}
]

TAUTAN_TERKAIT = [
    {
        "nama": "Muhammadiyah",
        "url": "https://muhammadiyah.or.id/",
        "urutan": 1,
    },
    {
        "nama": "PWM Jateng",
        "url": "https://pwmjateng.com/",
        "urutan": 2,
    },
    {
        "nama": "PDM Sukoharjo",
        "url": "https://pdmsukoharjo.or.id/",
        "urutan": 3,
    },
    {
        "nama": "Suara Muhammadiyah",
        "url": "https://suaramuhammadiyah.id/",
        "urutan": 4,
    },
    {
        "nama": "Lazismu",
        "url": "https://lazismu.org/",
        "urutan": 5,
    },
]

SAMBUTAN = {
    "nama": "Agus Komarudin",
    "foto": "sambutan_ketua/agus.png",
    "sambutan": (
        "Assalamu’alaikum warahmatullahi wabarakatuh.\n\n"
        "Puji syukur ke hadirat Allah SWT atas segala rahmat dan karunia-Nya. "
        "Shalawat serta salam semoga tercurah kepada Nabi Muhammad SAW.\n\n"
        "Selamat datang di website Pimpinan Cabang Muhammadiyah Grogol. "
        "Website ini diharapkan menjadi sarana informasi, komunikasi, dan "
        "publikasi berbagai kegiatan serta program persyarikatan. Kami "
        "berkomitmen untuk terus mengembangkan dakwah Islam berkemajuan, "
        "meningkatkan kualitas pendidikan, sosial, dan pelayanan masyarakat.\n\n"
        "Wassalamu’alaikum warahmatullahi wabarakatuh."
    ),
}

GALERI = [
{
    "judul": "Pelatihan Mubaligh Mubalighat tingkat Cabang",
    "gambar": "galeri_kegiatan/pelatihan.png",
},
{
    "judul": "Kajian Aisyiyah",
    "gambar": "galeri_kegiatan/kajian_aisyiyah.png",
},
{
    "judul": "Kajian Rutin Masjid",
    "gambar": "galeri_kegiatan/kajian.png",
},
{
    "judul": "Melaksanakan kaderisasi dan penambahan jumlah anggota baru",
    "gambar": "galeri_kegiatan/pengkaderan.png",
},
{
    "judul": "Kunjungan Kesehatan",
    "gambar": "galeri_kegiatan/kesehatan.png",
},
{
    "judul": "SOSIALISASI DAN BIMTEK E KTAM",
    "gambar": "galeri_kegiatan/acara.png",
}
]


class Command(BaseCommand):
    help = "Memasukkan data asli PCM Grogol ke database. Tidak membuat data atau file dummy."

    def add_arguments(self, parser):
        parser.add_argument(
            "--update",
            action="store_true",
            help="Perbarui data yang sudah ada berdasarkan kunci pencariannya.",
        )

    def handle(self, *args, **options):
        self.created = 0
        self.updated = 0
        self.skipped = 0
        self.failed = 0
        self.update_existing = options["update"]

        self.stdout.write(self.style.SUCCESS("=== SEED DATA ASLI PCM GROGOL ==="))
        if not self.update_existing:
            self.stdout.write(
                self.style.WARNING(
                    "Mode aman: data yang sudah ada tidak akan ditimpa. "
                    "Gunakan --update jika memang ingin memperbaruinya."
                )
            )

        with transaction.atomic():
            self.seed_singleton(ProfilOrganisasi, PROFIL, "Profil Organisasi", "gambar_utama")
            self.seed_many(Pimpinan, PIMPINAN, "Pimpinan", "nama", required_files=("foto",))
            self.seed_many(Ranting, RANTING, "Ranting", "nama_ranting")
            self.seed_many(AmalUsaha, AMAL_USAHA, "Amal Usaha", "nama", required_files=("gambar",))
            self.seed_berita()
            self.seed_agenda()
            self.seed_many(Dokumen, DOKUMEN, "Dokumen", "judul", required_files=("berkas",))
            self.seed_many(TautanTerkait, TAUTAN_TERKAIT, "Tautan Terkait", "url")
            self.seed_singleton(SambutanKetua, SAMBUTAN, "Sambutan Ketua", "foto")
            self.seed_many(GaleriKegiatan, GALERI, "Galeri Kegiatan", "judul", required_files=("gambar",))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=== SELESAI ==="))
        self.stdout.write(f"Data dibuat       : {self.created}")
        self.stdout.write(f"Data diperbarui   : {self.updated}")
        self.stdout.write(f"Data dilewati     : {self.skipped}")
        self.stdout.write(f"Data gagal        : {self.failed}")
        self.stdout.write(
            self.style.WARNING(
                "PesanMasuk tidak di-seed karena berisi pesan yang dikirim pengunjung website."
            )
        )

    def asset_exists(self, path, model_label, field_name):
        if not path:
            self.stdout.write(
                self.style.WARNING(
                    f"[DILEWATI] {model_label}: file pada field '{field_name}' belum diisi."
                )
            )
            self.skipped += 1
            return False

        if not default_storage.exists(path):
            self.stdout.write(
                self.style.WARNING(
                    f"[DILEWATI] {model_label}: file '{path}' tidak ditemukan di MEDIA_ROOT/storage."
                )
            )
            self.skipped += 1
            return False
        return True

    def prepare_defaults(self, model, data, label, required_files=()):
        defaults = {key: value for key, value in data.items() if value is not None}
        for field_name in required_files:
            if not self.asset_exists(defaults.get(field_name), label, field_name):
                return None

        # File opsional boleh kosong, tetapi jika diisi harus tersedia.
        for field_name in ("gambar_sampul",):
            path = defaults.get(field_name)
            if path and not default_storage.exists(path):
                self.stdout.write(
                    self.style.WARNING(
                        f"[DILEWATI] {label}: file opsional '{path}' tidak ditemukan."
                    )
                )
                self.skipped += 1
                return None

        return defaults

    def save_record(self, model, lookup, defaults, label):
        obj = model.objects.filter(**lookup).first()
        if obj:
            if not self.update_existing:
                self.skipped += 1
                self.stdout.write(self.style.WARNING(f"[DILEWATI] {label}: data sudah ada."))
                return

            for field, value in defaults.items():
                setattr(obj, field, value)
            obj.save()
            self.updated += 1
            self.stdout.write(self.style.SUCCESS(f"[DIPERBARUI] {label}"))
            return

        model.objects.create(**lookup, **defaults)
        self.created += 1
        self.stdout.write(self.style.SUCCESS(f"[DIBUAT] {label}"))

    def seed_singleton(self, model, data, label, required_file):
        if not data:
            self.skipped += 1
            self.stdout.write(self.style.WARNING(f"[DILEWATI] {label}: data belum diisi."))
            return

        defaults = self.prepare_defaults(model, data, label, (required_file,))
        if defaults is None:
            return

        existing = model.objects.first()
        if existing:
            if not self.update_existing:
                self.skipped += 1
                self.stdout.write(self.style.WARNING(f"[DILEWATI] {label}: data tunggal sudah ada."))
                return
            for field, value in defaults.items():
                setattr(existing, field, value)
            existing.save()
            self.updated += 1
            self.stdout.write(self.style.SUCCESS(f"[DIPERBARUI] {label}"))
            return

        model.objects.create(**defaults)
        self.created += 1
        self.stdout.write(self.style.SUCCESS(f"[DIBUAT] {label}"))

    def seed_many(self, model, records, label, lookup_field, required_files=()):
        if not records:
            self.stdout.write(self.style.WARNING(f"[INFO] {label}: belum ada data untuk dimasukkan."))
            return

        for index, record in enumerate(records, start=1):
            data = record.copy()
            lookup_value = data.pop(lookup_field, None)
            if not lookup_value:
                self.failed += 1
                self.stdout.write(self.style.ERROR(f"[GAGAL] {label} #{index}: '{lookup_field}' wajib diisi."))
                continue

            defaults = self.prepare_defaults(model, data, f"{label}: {lookup_value}", required_files)
            if defaults is None:
                continue
            self.save_record(model, {lookup_field: lookup_value}, defaults, f"{label}: {lookup_value}")

    def seed_berita(self):
        if not BERITA:
            self.stdout.write(self.style.WARNING("[INFO] Berita: belum ada data untuk dimasukkan."))
            return

        for index, record in enumerate(BERITA, start=1):
            data = record.copy()
            judul = data.get("judul")
            if not judul:
                self.failed += 1
                self.stdout.write(self.style.ERROR(f"[GAGAL] Berita #{index}: judul wajib diisi."))
                continue

            if not data.get("slug"):
                data["slug"] = slugify(judul)

            defaults = self.prepare_defaults(Berita, data, f"Berita: {judul}")
            if defaults is None:
                continue
            slug = defaults.pop("slug")
            self.save_record(Berita, {"slug": slug}, defaults, f"Berita: {judul}")

    
    def seed_agenda(self):
        for record in AGENDA:
            data = record.copy()
            nama = data.get("nama_kegiatan")

            if data.get("waktu_mulai") is None:
                self.stdout.write(
                    f"[DILEWATI] Agenda: {nama} - waktu mulai belum tersedia."
                )
                continue

            # nama_kegiatan sudah digunakan sebagai lookup
            data.pop("nama_kegiatan", None)

            self.save_record(
                Agenda,
                {"nama_kegiatan": nama},
                data,
                f"Agenda: {nama}"
            )
