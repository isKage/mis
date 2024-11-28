from django.shortcuts import render


def help_doc_zh(request):
    return render(request, 'help_doc_zh.html')

def help_doc_en(request):
    return render(request, 'help_doc_en.html')