
from django import forms
from .models import PesanMasuk


class PesanMasukForm(forms.ModelForm):
    class Meta:
        model = PesanMasuk
        fields = [
            field.name
            for field in PesanMasuk._meta.fields
            if (
                field.editable
                and not field.primary_key
                and field.get_internal_type()
                in ("CharField", "TextField", "EmailField", "URLField")
                and not field.choices
            )
        ]

    def clean_pesan(self):
        pesan = self.cleaned_data["pesan"].strip()
        if len(pesan) < 10:
            raise forms.ValidationError(
                "Pesan harus terdiri dari minimal 10 karakter."
            )
        return pesan
