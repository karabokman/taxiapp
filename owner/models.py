from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Owner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='o_img', default='placeholder.jpeg')

    def __str__(self):
        return self.user.last_name


class Transactions(models.Model):
    ride_no = models.CharField(max_length=255, unique=True)
    driver_no = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=150, decimal_places=2)
    category = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering:['-date']



class ToDoList(models.Model):
    task = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default="Not Done")

    def __str__(self):
        return self.task
