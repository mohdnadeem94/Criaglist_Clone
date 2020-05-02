from django.shortcuts import render

def HomePage(request):
    return render(request,'index.html')

def ThanksPage(request):
    return render(request,'thanks.html')
