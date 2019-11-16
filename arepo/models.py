from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Achievement(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField
    image = models.ImageField(default=None)


class Employee(models.Model, User):
    achievements = models.ManyToManyField(Achievement)


class Dish(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField
    price = models.DecimalField(max_digits=5, decimal_places=2)


class Order(models.Model):
    table = models.IntegerField
    employee = models.ForeignKey(Employee, on_delete=CASCADE)
    tip = models.IntegerField
    dishes = models.ManyToManyField(Dish)
