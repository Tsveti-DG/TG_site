# newspaper/views.py
from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Newspaper


def newspaper_list(request):
    issues = Newspaper.objects.filter(
        published_at__lte=timezone.now()
        # published_at__lte=timezone.localdate()

    ).order_by("-published_at", "-issue_number")

    paginator = Paginator(issues, 10)  # 10 броя на страница
    page = request.GET.get("page")
    issues_page = paginator.get_page(page)

    return render(request, "newspaper/newspaper_list.html", {
        "issues_page": issues_page
    })


# def newspaper_list(request):
#     # issues = Newspaper.objects.all()

#     issues = Newspaper.objects.filter(
#         published_at__lte=timezone.now()
#     )
#     return render(request, "newspaper/newspaper_list.html", {"issues": issues})
