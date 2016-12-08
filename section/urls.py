from django.contrib import admin
from django.conf.urls import include,url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import settings
from .views import properties
from .models import Sell
from . import views

  

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^properties/', properties.as_view(), name='properties'),
	url(r'^map-search/', views.map, name='map'),
	url(r'^map/get-properties/', views.get_properties, name='get_properties'),
	url(r'^map/properties/filter', views.properties_filter, name='properties_filter'),
	url(r'^login/',views.login_view, name='login'),
	url(r'^logout/',views.logout_view, name='logout'),
	url(r'^register/',views.register_view, name='register'),
	
	
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




