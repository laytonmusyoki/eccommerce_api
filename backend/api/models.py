from django.db import models

# Create your models here.


class Product(models.Model):
    Categories=(
        ('Desktop','Desktop'),
        ('Laptop','Laptop'),
        ('Phone','Phone'),
        ('Accessories','Accessories')
    )
    categories=models.CharField(max_length=100,choices=Categories,default=False,null=True,blank=True)
    name = models.CharField(max_length=200, null=True)
    description=models.CharField(max_length=300, null=True,blank=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(blank=True, null=True,upload_to='static/images')

    def __str__(self):
        return self.name

    # fixing error when there's no image for a given product
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


