from django.http import HttpResponse

# Create your views here.
def hello(request):
    return HttpResponse("<h2>Aplicacion web de consultas medicas </h2>")

def about(request):
    return HttpResponse('Acerca de ')