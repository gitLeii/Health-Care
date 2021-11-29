from django.db import models

# Create your models here.



class Symptom(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    
    def __str__(self):
        return self.name 


class Disease(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    description = models.TextField(null=True, blank=True)
    disease_symptom = models.ManyToManyField(Symptom, blank=True)
    prevention = models.TextField(default="")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]