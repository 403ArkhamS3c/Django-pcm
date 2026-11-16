# ⚠️ LAPORAN AUDIT KEAMANAN — Peringatan

> **Tanggal audit:** 16 November 2026
> **Scope:** Seluruh git history (`main`, `perbaikan-agenda`, `revisi-faqih`) + file tree HEAD
> **Status repo:** PUBLIC (dapat diakses siapa pun)
> **Catatan:** Laporan ini dibuat sebagai **peringatan**. History sengaja **tidak** dibersihkan, dan seluruh secret di bawah **wajib dianggap bocor**.

---

## 🔴 RINGKASAN EKSEKUTIF

Terdapat **secret yang bocor ke git history** repository ini. Karena repository bersifat **publik**, siapa pun dapat melihatnya melalui commit lama, meskipun file di HEAD sudah dibersihkan.

| # | Temuan | Severity | Di HEAD? | Di History? |
|---|--------|----------|----------|-------------|
| 1 | `SECRET_KEY` Django hardcoded | 🔴 Tinggi | ❌ Sudah dibersihkan | ✅ Masih ada |
| 2 | Password Postgres plaintext | 🔴 Tinggi | ❌ Sudah dibersihkan | ✅ Masih ada |
| 3 | `.env.production` pernah di-commit | 🟡 Sedang | ❌ Sudah dihapus | ✅ Masih ada |
| 4 | `.gitignore` belum case-insensitive | 🟡 Sedang | ⚠️ Sebagian | — |
| 5 | Bucket storage public tanpa auth | 🟠 Rendah | ⚠️ Ya | — |

---

## 🔴 1. SECRET_KEY Django Hardcoded (Severity: TINGGI)

**Lokasi (history):** commit `ed381d2` ("konfigurasi awal") dan `ad0b2d2` ("buat model data pcm")
**File:** `config/settings.py`

Nilai key (dipotong): `django-insecure-92mn#...`

Kedua commit tersebut adalah **leluhur `origin/main`**, sehingga masih dapat dibuka siapa pun melalui GitHub.

**Dampak:** Dengan `SECRET_KEY` yang bocor, penyerang dapat:
- Memalsukan sesi & cookie (session forgery)
- Menandatangani token CSRF palsu
- Dalam skenario tertentu, mengeksekusi serangan deserialisasi

**Status saat ini:** `config/settings.py` di HEAD sudah benar — membaca dari `os.getenv("SECRET_KEY")` dan melempar error jika kosong saat `DEBUG=False`. ✅

---

## 🔴 2. Password Postgres Plaintext (Severity: TINGGI)

**Lokasi (history):** commit `56e85b1`, `0a094ee`, `6984327`
**File:** `.env.example`

Terdiri dari:
- `POSTGRES_PASSWORD=PCM_Grog...123`
- `DATABASE_URL=postgresql://pcm_user:PCM_Grog...123@db:5432/pcm_db`

**Dampak:** Kredensial database terekspos publik. Password ini **wajib dianggap bocor**.

**Status saat ini:** `.env.example` di HEAD sudah kosong (tidak berisi password). ✅

---

## 🟡 3. `.env.production` Pernah Di-commit (Severity: SEDANG)

**Lokasi (history):**
- Ditambahkan: commit `56e85b1`
- Dihapus: commit `4dcb908`

**Isinya (semua placeholder):** `SECRET_KEY=secret-production`, `AWS_ACCESS_KEY_ID=...`, `DATABASE_URL=postgresql://...`

Tidak ada key AWS asli yang bocor, **tetapi** `secret-production` adalah nilai yang sangat mudah ditebak — **jangan pernah menggunakan nilai tersebut di environment production**.

---

## 🟡 4. `.gitignore` Belum Case-Insensitive (Severity: SEDANG)

`gitignore` bersifat **case-sensitive**. Pola berikut **TIDAK** ter-ignore:

```
.EVT  →  .ENV, .Env
Env/, Venv/
DB.sqlite3
```

Selain itu, `.env.*` baru ditambahkan belakangan. Pola yang sudah benar di HEAD:

```
.env
.env.*
!.env.example
```

**Rekomendasi tambahan:**
```
.ENV
.Env
Env/
Venv/
DB.sqlite3
```

---

## 🟠 5. Storage Public Tanpa Autentikasi (Severity: RENDAH)

Pada `config/settings.py`:
```python
AWS_QUERYSTRING_AUTH = False
# Bucket harus bersifat public untuk konfigurasi ini.
```

Semua file media (gambar, dokumen) dapat diakses tanpa login oleh siapa pun yang tahu URL-nya. Pastikan ini memang disengaja untuk kebutuhan website publik.

---

## ✅ YANG SUDAH AMAN

- Tidak ditemukan AWS key, token GitHub (`ghp_`), API key (`sk-`), atau private key di seluruh history
- `.env.example` di HEAD: seluruh secret dalam keadaan kosong
- `config/settings.py` di HEAD: `SECRET_KEY` dari environment, DEBUG default `False`
- Tidak ada `db.sqlite3` atau `.env` yang ter-commit
- `venv/` ter-ignore, tidak ada file `.env` di working directory
- README tidak membocorkan kredensial admin
- Tidak ada tabrakan nama file case-sensitive

---

## ⚡ REKOMENDASI (WAJIB DILAKUKAN)

### Prioritas 1 — ROTATE (paling urgent, lakukan SEKARANG)
Karena repository **publik**, secret di history sudah bisa dilihat orang lain:

1. **Ganti `SECRET_KEY` Django** di environment Vercel/production
2. **Ganti password Postgres** `PCM_Grog...123` — anggap password lama sudah bocor
3. Jika password yang sama dipakai di layanan lain (Supabase, email, dll) → **ganti juga**

> 🔑 **Menghapus history ≠ secret aman.** Rotasi adalah satu-satunya cara membuat secret lama benar-benar tidak berguna.

### Prioritas 2 — Proteksi GitHub
1. **Settings → Code security and analysis** → aktifkan:
   - ✅ **Secret scanning** (deteksi otomatis)
   - ✅ **Push protection** (push berisi secret otomatis ditolak)
2. Perkuat `.gitignore` dengan pola case variant (lihat butir 4)

### Prioritas 3 — Bersihkan History (OPSIONAL)
Jika ingin history bersih, gunakan `git filter-repo`:

```bash
pip install git-filter-repo
git filter-repo --replace-text <file-pola-secret>
git push --force --all origin
```

**Catatan:**
- Butuh force push ke semua branch
- GitHub menyimpan object "tak terjangkau" untuk beberapa waktu (masih bisa diakses via SHA)
- Fork/clone pihak lain tetap menyimpan salinan lama
- PR lama (`refs/pull/*`) juga membawa history lama

**Karena alasan di atas, ROTATE (Prioritas 1) tetap wajib meskipun history sudah dibersihkan.**

---

## 📋 CHECKLIST

- [ ] Rotate `SECRET_KEY` di production
- [ ] Ganti password Postgres
- [ ] Ganti password layanan lain yang memakai kredensial sama
- [ ] Aktifkan Secret Scanning di GitHub
- [ ] Aktifkan Push Protection di GitHub
- [ ] Perkuat `.gitignore` (pola case variant)
- [ ] (Opsional) Bersihkan history dengan `git filter-repo`
- [ ] (Opsional) Nonaktifkan/arsipkan PR lama yang membawa history bocor

---

*Laporan ini dibuat otomatis dari audit repository. Jangan hapus file ini sampai seluruh checklist di atas terpenuhi.*
