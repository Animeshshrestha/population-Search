import uuid

from django.db import models
from django.core.exceptions import NON_FIELD_ERRORS

class TimeStampedUUID(models.Model):
	"""
	Abstract Model 
	"""

	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

class Country(TimeStampedUUID):
	"""
	Model that inherits the TimeStampedUUID Model
	Model for adding the Country
	"""

	name = models.CharField(
		max_length=255,
		unique=True
	)

	def __str__(self):

		return self.name

class CityOrState(TimeStampedUUID):
	"""
	Model that inherits the TimeStampedUUID Model
	Model for adding the CityorState for specific 
	country
	"""

	country = models.ForeignKey(
				Country,
				on_delete=models.CASCADE,
				related_name='country_name'
	)
	city_or_state = models.CharField(max_length=255)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['country','city_or_state'],
				 name='unique_country_state')
		]
	
	def save(self, *args,**kwargs):
		"""
		This save method is used to check that 
		the unique validation is not violated.
		"""
		self.validate_unique()
		super(CityOrState,self).save(*args, **kwargs) 

	def __str__(self):

		return ('{} , {}'.format(self.country.name,self.city_or_state))

class PopulationSearch(TimeStampedUUID):
	"""
	Model that inherits the TimeStampedUUID Model
	Model for adding the Population for specific 
	country and city/state of specific age group
	for male and female
	"""

	GROUP_OLD='ol'
	GROUP_YOUNG = 'yo'
	GROUP_CHILD = 'ch'

	GROUP_CHOICES = (
		(GROUP_OLD,'Old'),
		(GROUP_YOUNG,'Young'),
		(GROUP_CHILD,'Child')
	)

	group = models.CharField(
		max_length=2,
		choices=GROUP_CHOICES
	)

	country = models.ForeignKey(Country,
				on_delete=models.CASCADE,
				related_name='country_population')

	city_or_state = models.ForeignKey(CityOrState,
				on_delete=models.CASCADE,
				related_name='country_cityorstate')

	no_of_male = models.PositiveIntegerField()
	no_of_female = models.PositiveIntegerField()

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['group','country','city_or_state'],
				 name='unique_group_age_state')
		]
	
	def save(self, *args,**kwargs):
		"""
		This save method is used to check that 
		the unique validation is not violated.
		"""
		self.validate_unique()
		super(PopulationSearch,self).save(*args, **kwargs) 

	def __str__(self):

		return ('{} , {}'.format(self.country,self.group))


