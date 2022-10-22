from django.db import models

# Create your models here.


class Property(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)


class Component(models.Model):
    component_no = models.CharField(max_length=100, unique=True, primary_key=True)
    properties = models.ManyToManyField(to=Property, blank=True, default=None)


class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)


class Order(models.Model):
    order_no = models.IntegerField(unique=True, primary_key=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    component = models.ForeignKey(Component, null=True, on_delete=models.SET_NULL)



