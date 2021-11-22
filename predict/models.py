from django.db import models

# Create your models here.

class Disease(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Symptom(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    symptom_disease = models.ManyToManyField(Disease, blank=True, related_name="symptom_disease")
    
    def __str__(self):
        return self.name 

