# Django PCM Grogol

Dokumentasi implementasi dan pengembangan website Pimpinan Cabang Muhammadiyah (PCM) Grogol menggunakan Django.

---

# 1. Implementasi Context Processor untuk Footer

## 1.1 Deskripsi

Context Processor digunakan untuk menyediakan data tautan persyarikatan (`TautanTerkait`) dari database ke seluruh template Django secara otomatis.

Dengan menggunakan Context Processor, data tautan tidak perlu diambil dan dikirim secara berulang melalui setiap fungsi View. Hal ini membuat pengelolaan kode lebih efisien dan memudahkan pemeliharaan aplikasi.

## 1.2 Struktur File

Tambahkan file `context_processors.py` di dalam direktori aplikasi `core`.

```text
core/
├── context_processors.py
├── models.py
├── views.py
└── templates/
```

## 1.3 Pembuatan Context Processor

Buat fungsi `tautan_footer` pada file `core/context_processors.py`.

```python
from .models import TautanTerkait

def tautan_footer(request):
    return {
        "tautan_terkait": TautanTerkait.objects.all()
    }
```

**Keterangan:**

- `TautanTerkait`: Model yang digunakan untuk mengambil data tautan dari database.
- `request`: Parameter request yang diberikan Django kepada Context Processor.
- `tautan_terkait`: Nama variabel yang dapat dipanggil langsung dari template.
- `objects.all()`: Mengambil seluruh data tautan yang tersimpan di database.

## 1.4 Konfigurasi pada settings.py

Daftarkan Context Processor pada bagian `TEMPLATES`, tepatnya di dalam konfigurasi `context_processors`.

```python
'context_processors': [
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'core.context_processors.tautan_footer',
],
```

Pendaftaran ini memungkinkan Django menjalankan fungsi `tautan_footer` ketika memproses template menggunakan konfigurasi tersebut.

## 1.5 Penerapan pada Template Footer

Gunakan variabel `tautan_terkait` untuk menampilkan daftar tautan persyarikatan pada footer.

```django
<ul class="list-unstyled footer-links">
    {% for tautan in tautan_terkait %}
        <li class="mb-2">
            <a href="{{ tautan.url }}"
               target="_blank"
               rel="noopener noreferrer">
                {{ tautan.nama }}
            </a>
        </li>
    {% empty %}
        <li class="footer-muted">
            Belum ada tautan tersedia.
        </li>
    {% endfor %}
</ul>
```

**Keterangan:**

- `tautan.nama`: Menampilkan nama tautan.
- `tautan.url`: Menampilkan alamat tujuan tautan.
- `target="_blank"`: Membuka tautan pada tab baru.
- `{% empty %}`: Menampilkan keterangan apabila belum terdapat data tautan.

## 1.6 Keuntungan Penggunaan Context Processor

1. **Efisiensi kode:** Tidak perlu mengambil data tautan secara berulang pada setiap View.
2. **Konsistensi data:** Seluruh halaman dapat menampilkan daftar tautan yang sama.
3. **Kemudahan pemeliharaan:** Perubahan data cukup dilakukan melalui pengelolaan database.
4. **Penggunaan ulang (reusability):** Data dapat digunakan pada berbagai template selama diproses menggunakan konfigurasi Context Processor tersebut.

## 1.7 Hasil Implementasi

Data tautan persyarikatan yang tersimpan di database dapat ditampilkan secara otomatis pada footer di seluruh halaman website yang menggunakan template footer tersebut, tanpa perlu menambahkan pengambilan data secara manual pada setiap fungsi View.

---

# 2. Implementasi Django Template: Extends dan Include

## 2.1 Tujuan

Penggunaan `extends` dan `include` bertujuan untuk menghindari penulisan kode HTML yang berulang pada setiap halaman website PCM Grogol.

Dengan penerapan ini, bagian yang memiliki struktur sama dapat digunakan kembali sehingga pengelolaan template menjadi lebih mudah dan konsisten.

## 2.2 Struktur Template

Komponen template disusun seperti berikut:

```text
core/
└── templates/
    └── core/
        ├── components/
        │   ├── base.html
        │   ├── topbar.html
        │   ├── navbar.html
        │   ├── hero.html
        │   └── footer.html
        │
        ├── home.html
        ├── pimpinan.html
        └── ranting.html
```

**Keterangan:**

- `base.html`: Template utama yang menjadi kerangka dasar halaman.
- `topbar.html`: Komponen bagian informasi atas website.
- `navbar.html`: Komponen navigasi website.
- `hero.html`: Komponen banner atau bagian pengenalan halaman.
- `footer.html`: Komponen bagian bawah website.
- Template halaman seperti `home.html`, `pimpinan.html`, dan `ranting.html` berisi konten khusus masing-masing halaman.

## 2.3 Penggunaan Extends

`extends` digunakan untuk mewarisi struktur HTML dari template utama (`base.html`).

Contoh penerapan pada `pimpinan.html`:

```django
{% extends 'core/components/base.html' %}

{% block title %}Pimpinan PCM{% endblock %}

{% block hero %}
    ...
{% endblock %}

{% block content %}
    ...
{% endblock %}
```

Dengan menggunakan `extends`, halaman `pimpinan.html` tidak perlu menuliskan ulang struktur HTML utama seperti `<html>`, `<head>`, `<body>`, dan komponen umum lainnya.

### Penggunaan Block

`block` digunakan untuk menentukan bagian template yang dapat diisi atau diganti oleh template turunan.

Block yang digunakan antara lain:

| Block | Fungsi |
|---|---|
| `title` | Mengatur judul halaman pada tab browser. |
| `topbar` | Menyediakan bagian topbar. |
| `navbar` | Menyediakan bagian navigasi. |
| `hero` | Menampilkan banner atau pengenalan halaman. |
| `content` | Menampilkan konten utama halaman. |

Contoh pada `base.html`:

```django
<title>{% block title %}PCM Grogol{% endblock %}</title>

{% block hero %}{% endblock %}

{% block content %}{% endblock %}
```

Template turunan dapat mengisi block tersebut sesuai kebutuhan masing-masing halaman.

## 2.4 Penggunaan Include

`include` digunakan untuk memasukkan komponen template lain ke dalam template yang sedang digunakan.

Contoh penerapan pada `base.html`:

```django
{% include 'core/components/topbar.html' %}
{% include 'core/components/navbar.html' %}

{% block hero %}{% endblock %}

{% block content %}{% endblock %}

{% include 'core/components/footer.html' %}
```

Dengan demikian, komponen topbar, navbar, dan footer cukup dibuat satu kali dan dapat digunakan kembali pada berbagai halaman.

### Include dengan Parameter

Komponen Hero memiliki struktur yang sama, tetapi isi teksnya berbeda pada setiap halaman. Oleh karena itu, digunakan `include` dengan parameter `with`.

Contoh penerapan pada `pimpinan.html`:

```django
{% block hero %}
    {% include 'core/components/hero.html' with
        hero_label="STRUKTUR ORGANISASI"
        hero_title="Pimpinan PCM"
        hero_description="Kenali jajaran pimpinan dan periode kepengurusan Pimpinan Cabang Muhammadiyah."
    %}
{% endblock %}
```

Parameter tersebut digunakan untuk mengirimkan informasi ke `hero.html`.

Contoh isi `hero.html`:

```django
<header class="hero text-center">
    <div class="container">
        <span class="hero-label">{{ hero_label }}</span>
        <h1>{{ hero_title }}</h1>
        <p>{{ hero_description }}</p>
    </div>
</header>
```

Dengan cara ini, struktur Hero tetap sama, sedangkan teksnya dapat disesuaikan untuk setiap halaman.

## 2.5 Pembagian Tanggung Jawab Template

Penerapan `extends` dan `include` membagi tanggung jawab template sebagai berikut:

- `base.html` mengatur kerangka utama halaman, pemanggilan komponen umum, file CSS, dan JavaScript.
- `topbar.html`, `navbar.html`, `hero.html`, dan `footer.html` menyimpan komponen yang dapat digunakan kembali.
- Template turunan seperti `pimpinan.html` dan `ranting.html` mengatur konten yang bersifat khusus untuk halaman tersebut.

Sebagai contoh, pada `pimpinan.html`, bagian daftar pimpinan, foto, informasi identitas, kondisi data kosong, dan pagination tetap berada di dalam block `content`.

## 2.6 Perbedaan Extends dan Include

| Aspek | Extends | Include |
|---|---|---|
| Fungsi | Mewarisi template utama. | Memasukkan komponen template lain. |
| Penggunaan | Hubungan template induk dan turunan. | Menggunakan kembali potongan template. |
| Contoh | `base.html` ke `pimpinan.html`. | `navbar.html` ke `base.html`. |
| Tujuan | Menghindari pengulangan kerangka halaman. | Menghindari pengulangan komponen HTML. |

## 2.7 Catatan Penting

1. Penggunaan `extends` harus ditempatkan di bagian paling atas template turunan.
2. Nama block pada template turunan harus sesuai dengan nama block yang tersedia pada template utama.
3. Komponen yang selalu digunakan pada semua halaman sebaiknya dipanggil langsung dari `base.html`.
4. Komponen yang memiliki struktur sama tetapi isi berbeda dapat menggunakan `include` dengan parameter `with`.
5. Jika sebuah file template menggunakan `{% static %}`, tambahkan `{% load static %}` pada file tersebut.
6. Jangan menuliskan ulang footer, navbar, Bootstrap JavaScript, dan file JavaScript utama di template turunan apabila sudah ditangani oleh `base.html`.

## 2.8 Kesimpulan

Penggunaan `extends` dan `include` membuat struktur template website PCM Grogol menjadi lebih terorganisasi dan mengurangi duplikasi kode HTML.

`extends` digunakan untuk mewarisi kerangka halaman, sedangkan `include` digunakan untuk menggunakan kembali komponen tertentu. Dengan penerapan ini, perubahan pada komponen umum dapat dilakukan cukup dari satu file tanpa harus mengubah setiap halaman secara terpisah.