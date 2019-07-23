from django.db import models


class CyclparkPointManager(models.Manager):

    def create_object(self, data: dict):
        point = CyclparkPoint.objects.filter(global_id=data['global_id'])
        if not point.exists():
            new_point = self.create(
                global_id=data['global_id'],
                name=data['name'],
                admarea=data['admarea'],
                district=data['district'],
                address=data['address'],
                capacity=data['capacity'],
                departamentalaffiliation=data['departamentalaffiliation'],
                objectoperorgname=data['objectoperorgname'],
                longitude_WGS84=data['longitude_WGS84'],
                latitude_WGS84=data['latitude_WGS84']

            )
            return new_point
        else:
            point = CyclparkPoint.objects.filter(global_id=data['global_id'])
            point.name = data['name']
            point.admarea = data['admarea']
            point.district = data['district']
            point.address = data['address']
            point.capacity = data['capacity']
            point.departamentalaffiliation = data['departamentalaffiliation']
            point.objectoperorgname = data['objectoperorgname']
            point.longitude_WGS84 = data['longitude_WGS84']
            point.latitude_WGS84 = data['latitude_WGS84']
            return point


class CyclparkPoint(models.Model):
    global_id = models.IntegerField(verbose_name='global_id', unique=True, default=None)
    name = models.CharField(verbose_name='Name', max_length=200, default=None)
    admarea = models.CharField(verbose_name='Adm. area', max_length=200, default=None)
    district = models.CharField(verbose_name='District', max_length=200, default=None)
    address = models.CharField(verbose_name='Address', max_length=200, default=None)
    capacity = models.IntegerField(verbose_name='Capacity', default=None)
    departamentalaffiliation = models.CharField(verbose_name='Departament Affiliation', max_length=200, default=None)
    objectoperorgname = models.CharField(verbose_name='Object organisation name', max_length=200, default=None)
    longitude_WGS84 = models.FloatField(verbose_name='Langitude', default=None)
    latitude_WGS84 = models.FloatField(verbose_name='Latitude', default=None)

    def __str__(self):
        return self.name

    objects = CyclparkPointManager()


class ApiInfo(models.Model):
    version = models.IntegerField(name='versionNumber')
    release = models.IntegerField(name='releaseNumber')

    def __str__(self):
        return f'Version: {self.versionNumber}, release: {self.releaseNumber}'
