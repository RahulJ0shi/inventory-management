from django.db import models

# Create your models here.
class product(models.Model):
	name=models.CharField(max_length=50,blank=False,unique=True)
	category=models.CharField(max_length=50,blank=False)
	price=models.IntegerField()
	expire_date=models.DateField()
	units=models.IntegerField()

	class Meta:
		ordering=['-expire_date']

	def __str__(self):
		return self.name

class cat(models.Model):
	p_category=models.CharField(max_length=100,blank=False,unique=True)
	capacity=models.IntegerField()

	def __str__(self):
		return self.category

