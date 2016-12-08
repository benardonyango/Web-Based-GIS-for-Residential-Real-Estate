from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from section.models import Sell


class SellAdmin(geoadmin.OSMGeoAdmin):
	default_lon = 36.8219
	default_lat = -1.2921
	default_zoom = 5
	

geoadmin.site.register(Sell,SellAdmin)




    