from django.shortcuts import render


def home(request):
    return render(request, 'accounts/main.html')