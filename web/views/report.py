from django.shortcuts import render


def report_pdf(request):
    return render(request, 'report_pdf.html')
