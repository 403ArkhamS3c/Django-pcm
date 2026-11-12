from core.models import AmalUsaha

S, P = "sosial", "pendidikan"

data = [
    ("Panti Asuhan Yatim Muhammadiyah Grogol", S, "Telukan, Grogol",
     "Panti asuhan yatim di bawah naungan Muhammadiyah Grogol, berlokasi di Telukan."),
    ("Panti Asuhan Yatim Putri Aisyiyah Grogol", S, "Grogol",
     "Panti asuhan yatim putri di bawah naungan Aisyiyah Grogol."),
    ("Madrasah Ibtidaiyah Muhammadiyah Grogol", P, "Sudimoro, Grogol",
     "Madrasah ibtidaiyah Muhammadiyah yang berlokasi di Sudimoro, Grogol."),
    ("Madrasah Tsanawiyah Muhammadiyah Grogol", P, "Sudimoro, Grogol",
     "Madrasah tsanawiyah Muhammadiyah yang berlokasi di Sudimoro, Grogol."),
    ("TK/BA Aisyiyah 1 Grogol", P, "Grogol",
     "Taman kanak-kanak Aisyiyah yang berlokasi di Grogol."),
    ("TK/BA Aisyiyah 2 Grogol", P, "Soko, Grogol",
     "Taman kanak-kanak Aisyiyah yang berlokasi di Soko, Grogol."),
    ("TK/BA Aisyiyah 3 Grogol", P, "Sudimoro, Grogol",
     "Taman kanak-kanak Aisyiyah yang berlokasi di Sudimoro, Grogol."),
    ("TK/BA Aisyiyah 4 Grogol", P, "Madegondo, Grogol",
     "Taman kanak-kanak Aisyiyah yang berlokasi di Madegondo, Grogol."),
    ("TK/BA Aisyiyah 5 Grogol", P, "Pondok, Grogol",
     "Taman kanak-kanak Aisyiyah yang berlokasi di Pondok, Grogol."),
    ("TK/BA Aisyiyah 6 Grogol", P, "Pondok, Grogol",
     "Taman kanak-kanak Aisyiyah yang berlokasi di Pondok, Grogol."),
    ("TK/BA Aisyiyah 7 Grogol", P, "Kadokan, Grogol",
     "Taman kanak-kanak Aisyiyah yang berlokasi di Kadokan, Grogol."),
    ("TK/BA Aisyiyah 8 Grogol", P, "Sanggrahan, Grogol",
     "Taman kanak-kanak Aisyiyah yang berlokasi di Sanggrahan, Grogol."),
    ("TK/BA Aisyiyah 9 Grogol", P, "Langenharjo, Grogol",
    "Taman kanak-kanak Aisyiyah yang berlokasi di Langenharjo, Grogol."),
    ("TK/BA Aisyiyah Qurrata A'yun Grogol", P, "Pondok, Grogol",
    "Taman kanak-kanak Aisyiyah yang berlokasi di Pondok, Grogol."),
]

for nama, bidang, alamat, deskripsi in data:
    obj, dibuat = AmalUsaha.objects.get_or_create(
        nama=nama,
        defaults={"bidang": bidang, "alamat": alamat, "deskripsi": deskripsi},
    )
    print(("Dibuat: " if dibuat else "Sudah ada: ") + nama)