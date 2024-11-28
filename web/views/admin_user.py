from django.shortcuts import render, redirect, HttpResponse

from web import models


def user_list(request):
    # 根据需求筛选数据库数据
    queryset = models.Preference.objects.all()

    context = {
        "queryset": queryset,
    }
    return render(request, "user_list.html", context)
