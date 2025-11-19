from .models import SuperCategory


def supercategories_processor(request):
    return {'menu_supercategories': SuperCategory.objects.all().order_by('order', 'name')}
