from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
