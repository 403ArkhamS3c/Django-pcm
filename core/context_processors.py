from .models import TautanTerkait, ProfilOrganisasi

def tautan_footer(request):
    return {
        "tautan_terkait": TautanTerkait.objects.all(),
        "profil": ProfilOrganisasi.objects.first(),
    }