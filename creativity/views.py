from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import CreativeWork


def creativity_list(request):
    works = CreativeWork.objects.all()

    paginator = Paginator(works, 9)  # като новините
    page_number = request.GET.get("page")
    works_page = paginator.get_page(page_number)

    context = {
        "works_page": works_page,
    }
    return render(request, "creativity/creativity_list.html", context)


def creativity_detail(request, code):
    work = get_object_or_404(CreativeWork, code=code)

    context = {
        "work": work,
    }
    return render(request, "creativity/creativity_detail.html", context)
