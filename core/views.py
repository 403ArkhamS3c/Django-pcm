from django.shortcuts import render
from .models import ProfilOrganisasi, Pimpinan, Ranting, AmalUsaha, Berita, Agenda, Dokumen, TautanTerkait, SambutanKetua, GaleriKegiatan
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PesanMasuk
from .forms import PesanMasukForm
from django.utils import timezone
from django.db.models import ImageField, FileField


FIELD_PUBLIK = {
    ProfilOrganisasi: ["nama", "nama_singkat", "tagline", "tentang", "sejarah", "visi", "misi", "alamat_sekretariat", "telepon", "email", "jumlah_anggota_ktam", "gambar_utama"],
    Pimpinan: ["nama", "jabatan", "periode", "foto", "urutan_tampil"],
    Ranting: ["nama_ranting", "ketua", "alamat", "telepon"],
    AmalUsaha: ["nama", "bidang", "deskripsi", "alamat", "gambar"],
    Berita: ["judul", "slug", "ringkasan", "isi", "gambar_sampul", "tanggal_terbit", "status"],
    Agenda: ["nama_kegiatan", "waktu_mulai", "tempat", "keterangan"],
    Dokumen: ["judul", "keterangan", "berkas", "tanggal_unggah"],
}

KONFIGURASI_PUBLIKASI = {
    Berita: {
        "field_status": "status",
        "nilai_terbit": "terbit",
    },
    Agenda: {
        "field_status": None,
        "nilai_terbit": None,
    },
}

def home(request):
    profil = ProfilOrganisasi.objects.first()

    detail_profil = (
        data_tampilan(profil)
        if profil is not None
        else []
    )
    berita_terbaru = Berita.objects.terbit()[:3]
    ketua = SambutanKetua.objects.first()
    galeri = GaleriKegiatan.objects.all()
    agenda_list = Agenda.objects.all()[:6]
    pimpinan_list = Pimpinan.objects.all()

    return render(
        request,
        "core/home.html",
        {
            "profil": profil,
            "detail_profil": detail_profil,
            "berita_terbaru": berita_terbaru,
            "ketua": ketua,
            "galeri": galeri,
            "agenda_list":agenda_list,
            "pimpinan_list": pimpinan_list,  
        },
    )



def daftar_pimpinan(request):
    semua_pimpinan = Pimpinan.objects.all().order_by("urutan_tampil")

    per_halaman = 2
    total_data = semua_pimpinan.count()
    total_halaman = (total_data + per_halaman - 1) // per_halaman

    try:
        halaman = int(request.GET.get("page", 1))
    except ValueError:
        halaman = 1

    halaman = max(1, min(halaman, total_halaman or 1))

    mulai = (halaman - 1) * per_halaman
    selesai = mulai + per_halaman

    pimpinan = semua_pimpinan[mulai:selesai]

    daftar = [
        {
            "objek": item,
            "detail": data_tampilan(item)
        }
        for item in pimpinan
    ]

    return render(request, "core/pimpinan.html", {
        "daftar": daftar,
        "halaman": halaman,
        "ada_next": halaman < total_halaman,
        "ada_previous": halaman > 1,
    })


def daftar_ranting(request):
    halaman = int(request.GET.get("page", 1))
    per_halaman = 10

    mulai = (halaman - 1) * per_halaman
    selesai = mulai + per_halaman

    semua_ranting = Ranting.objects.all().order_by("nama_ranting")
    ranting = semua_ranting[mulai:selesai]

    return render(
        request,
        "core/ranting.html",
        {
            "ranting": ranting,
            "halaman": halaman,
            "mulai": mulai,
            "ada_next": semua_ranting.count() > selesai,
            "ada_previous": halaman > 1,
        },
    )


def daftar_amal_usaha(request):
    semua_amal_usaha = AmalUsaha.objects.all().order_by("nama")

    per_halaman = 2
    total_data = semua_amal_usaha.count()
    total_halaman = (total_data + per_halaman - 1) // per_halaman

    try:
        halaman = int(request.GET.get("page", 1))
    except ValueError:
        halaman = 1

    halaman = max(1, min(halaman, total_halaman or 1))

    mulai = (halaman - 1) * per_halaman
    selesai = mulai + per_halaman

    amal_usaha = semua_amal_usaha[mulai:selesai]

    daftar = [
        {
            "objek": item,
            "detail": data_tampilan(item)
        }
        for item in amal_usaha
    ]

    return render(request, "core/amal_usaha.html", {
        "daftar": daftar,
        "halaman": halaman,
        "ada_next": halaman < total_halaman,
        "ada_previous": halaman > 1,
    })



def daftar_berita(request):
    berita = konten_publik(Berita)

    daftar = [
        {
            "objek": item,
            "detail": data_tampilan(item),
        }
        for item in berita
    ]

    return render(
        request,
        "core/berita.html",
        {"daftar": daftar},
    )



def daftar_agenda(request):
    agenda = konten_publik(Agenda)

    daftar = [
        {
            "objek": item,
            "detail": data_tampilan(item),
        }
        for item in agenda
    ]

    return render(
        request,
        "core/agenda.html",
        {"daftar": daftar},
    )



def daftar_dokumen(request):
    dokumen = Dokumen.objects.all()

    daftar = [
        {
            "objek": item,
            "detail": data_tampilan(item),
        }
        for item in dokumen
    ]

    return render(
        request,
        "core/dokumen.html",
        {"daftar": daftar},
    )



def detail_berita(request, pk):
    item = get_object_or_404(
        konten_publik(Berita),
        pk=pk,
    )

    detail = data_tampilan(item)

    # Mengambil 5 berita terbaru selain berita yang sedang dibuka
    berita_terbaru = (
        konten_publik(Berita)
        .exclude(pk=item.pk)
        .order_by("-tanggal_terbit")[:5]
    )

    return render(
        request,
        "core/detail_berita.html",
        {
            "item": item,
            "detail": detail,
            "berita_terbaru": berita_terbaru,
        },
    )

def detail_agenda(request, pk):
    item = get_object_or_404(
        konten_publik(Agenda),
        pk=pk,
    )
    detail = data_tampilan(item)
    return render(
        request,
        "core/detail_agenda.html",
        {"item": item, "detail": detail},
    )


def pesan_masuk(request):
    if request.method == "POST":
        form = PesanMasukForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Pesan berhasil dikirim."
            )
            return redirect("pesan_masuk")
    else:
        form = PesanMasukForm()

    return render(
        request,
        "core/pesan_masuk.html",
        {"form": form},
    )


def daftar_tautan(request):
    tautan = TautanTerkait.objects.all()
    return render(
        request,
        "core/tautan.html",
        {"tautan": tautan},
    )


def data_tampilan(objek):
    hasil = []
    field_diizinkan = FIELD_PUBLIK.get(type(objek), [])

    for field in objek._meta.fields:
        if field.name not in field_diizinkan:
            continue

        nilai = getattr(objek, field.name, None)

        if not nilai:
            continue

        if isinstance(field, ImageField):
            jenis = "gambar"
            url_file = nilai.url
        elif isinstance(field, FileField):
            jenis = "file"
            url_file = nilai.url
        else:
            jenis = "teks"
            url_file = None

        hasil.append({
            "label": field.verbose_name,
            "nilai": nilai,
            "jenis": jenis,
            "url_file": url_file,
        })

    return hasil


def konten_publik(model):
    konfigurasi = KONFIGURASI_PUBLIKASI.get(model)

    if not konfigurasi:
        return model.objects.none()

    nama_field = konfigurasi["field_status"]
    nilai_terbit = konfigurasi["nilai_terbit"]

    if nama_field is None and nilai_terbit is None:
        return model.objects.all().order_by("waktu_mulai")

    if not nama_field or nilai_terbit is None:
        return model.objects.none()

    nama_field_valid = {
        field.name
        for field in model._meta.fields
    }

    if nama_field not in nama_field_valid:
        return model.objects.none()

    return model.objects.filter(
        **{nama_field: nilai_terbit}
    )

