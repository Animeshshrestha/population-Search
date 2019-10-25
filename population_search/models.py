import uuid

from django.db import models

class TimeStampedUUID(models.Model):

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

	name = models.CharField(
		max_length=255,
		unique=True
	)

	def __str__(self):

		return self.name

class CityOrState(TimeStampedUUID):

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

	def __str__(self):

		return ('{} , {}'.format(self.country.name,self.city_or_state))

class PopulationSearch(TimeStampedUUID):

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
	city_or_state = models.CharField(max_length=255)
	no_of_male = models.PositiveIntegerField()
	no_of_female = models.PositiveIntegerField()

	def __str__(self):

		return ('{} , {}'.format(self.country,self.group))



