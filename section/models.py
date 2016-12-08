from __future__ import unicode_literals
from django.db import models
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
 






class Sell(models.Model):
	sale_rent_choices = (
		('Sale', 'Sale'),
		('Rent', 'Rent'),
	)

	beds_choices = (
	(1, '1'),
	(2, '2'),
	(3, '3'),
	(4, '4'),
	(5, '5'),
	(6, '6'),
	(7, '7'),
	
	)

	baths_choices = (
	(1, '1'),
	(2, '2'),
	(3, '3'),
	(4, '4'),
	(5, '5'),
	(6, '6'),
	(7, '7'),
	
	)

	house_type_choices = (
		('HOUSE', 'House'),
		('APARTMENT_FLAT', 'Apartment/Flat'),
		('TOWNHOUSE', 'Town House'),
		('DUPLEX','Duplex'),
	)


	model_pic = models.ImageField(upload_to = 'media', blank=True, null=True)
	firstname = models.CharField(max_length=20)
	lastname = models.CharField(max_length=20)
	email = models.EmailField(max_length=70)
	phone = models.IntegerField()
	price = models.IntegerField()
	sale_rent = models.CharField(max_length=10, choices=sale_rent_choices)
	house_type = models.CharField(max_length=20, choices=house_type_choices)
	beds = models.IntegerField(choices=beds_choices)
	baths = models.IntegerField(choices=baths_choices)
	description = models.TextField()
	geom = models.PointField(srid=4326)
	objects = models.GeoManager()

	def __unicode__(self):
		return self.sale_rent

	class Meta:
		verbose_name_plural = "Residential Real Estate"










