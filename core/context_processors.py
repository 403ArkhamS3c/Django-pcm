from .models import TautanTerkait

def tautan_footer(request):
    return {
        "tautan_terkait": TautanTerkait.objects.all()
    }