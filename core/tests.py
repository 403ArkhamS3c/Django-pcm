from datetime import date, datetime, time
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Agenda


class AgendaPageTests(TestCase):
    def test_agendas_are_separated_and_page_renders(self):
        today = date(2026, 11, 12)
        tz = timezone.get_current_timezone()

        terlaksana = Agenda.objects.create(
            nama_kegiatan="Kegiatan yang sudah lewat",
            waktu_mulai=timezone.make_aware(
                datetime.combine(date(2026, 11, 11), time(10)),
                tz,
            ),
            tempat="Grogol",
        )
        agenda_hari_ini = Agenda.objects.create(
            nama_kegiatan="Kegiatan hari ini",
            waktu_mulai=timezone.make_aware(
                datetime.combine(today, time(10)),
                tz,
            ),
            tempat="Grogol",
        )
        agenda_mendatang = Agenda.objects.create(
            nama_kegiatan="Kegiatan mendatang",
            waktu_mulai=timezone.make_aware(
                datetime.combine(date(2026, 11, 13), time(10)),
                tz,
            ),
            tempat="Grogol",
        )

        with patch("core.views.timezone.localdate", return_value=today):
            response = self.client.get(reverse("agenda"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Agenda Akan Datang")
        self.assertContains(response, "Agenda Terlaksana")
        self.assertContains(response, "Kegiatan hari ini")
        self.assertContains(response, "Kegiatan mendatang")
        self.assertContains(response, "Kegiatan yang sudah lewat")

        upcoming_section = response.content.decode().split(
            'id="agenda-terlaksana"', 1
        )[0]
        completed_section = response.content.decode().split(
            'id="agenda-terlaksana"', 1
        )[1]
        self.assertIn(agenda_hari_ini.nama_kegiatan, upcoming_section)
        self.assertIn(agenda_mendatang.nama_kegiatan, upcoming_section)
        self.assertNotIn(terlaksana.nama_kegiatan, upcoming_section)
        self.assertIn(terlaksana.nama_kegiatan, completed_section)
        self.assertNotIn(agenda_hari_ini.nama_kegiatan, completed_section)
