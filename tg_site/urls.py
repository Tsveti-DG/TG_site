from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # само начална страница и статични текстове
    path('', include('core.urls')),
    path('news/', include('news.urls')),
    path('gallery/', include('gallery.urls')),
    path('documents/', include('documents.urls')),
    path('newspaper/', include('newspaper.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
