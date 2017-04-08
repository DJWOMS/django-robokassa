from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#Модель пополнения	
class Popoln(models.Model):
	class Meta():
		db_table = 'popoln'
		verbose_name = "Пополнение"
		verbose_name_plural = "Пополнения"
		
	user = models.ForeignKey(User)
	sum = models.FloatField("Сумма", default = 50.00)
	date = models.DateTimeField("Дата покупки", default=timezone.now)
	odobren = models.BooleanField("Успех пополнения", default=False)
	
	def __str__(self):
		return self.user.username
