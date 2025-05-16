from django.http import HttpResponse

def homepage(request):
    return HttpResponse("Hello?")

def about(request):
    return HttpResponse("My abt page")

