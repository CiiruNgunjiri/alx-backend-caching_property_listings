from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # Keep view-level cache for 15 minutes to cache full response
def property_list(request):
    properties = get_all_properties()  # Use cached queryset (or fetch if expired)
    data = [{'id': p.id, 'title': p.title, 'location': p.location, 'price': p.price} for p in properties]
    return JsonResponse({'data': data})
    
    # you can also return as below
    # return render(request, 'properties/property_list.html', {'properties': properties})
