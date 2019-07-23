from django.shortcuts import render
from django.http.response import HttpResponse
from .update import update_points
from .models import ApiInfo, CyclparkPoint
import re


def index(request):
    points = CyclparkPoint.objects.all()
    all_points = []
    for point in points:
        address = point.address
        shop_name = re.findall(r'".{0,30}"', point.address)
        if shop_name:
            address = address.replace(shop_name[0], '«{}»'.format(shop_name[0].replace('"', '')))

        all_points.append(
            {
                'y': point.longitude_WGS84,
                'x': point.latitude_WGS84,
                'name': point.name,
                'address': address.replace('\n', '')
            }
        )

    return render(request, 'index.html', context={'points_info': all_points})