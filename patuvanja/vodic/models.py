from django.db import models

# Create your models here.

#Patuvanja imaat mesto, vremetraenje i slika
class Patuvanje(models.Model):
    mesto = models.CharField(max_length = 255)
    datum_pochetok = models.DateTimeField(auto_now=False, auto_now_add=False)
    vremetraenje = models.IntegerField()
    slika = models.ImageField(upload_to='data/')

# Vodachi imaat ime, prezime, telefon, email
# zaedno so relacija do patuvanja (m2m)
class Vodach(models.Model):
    ime = models.CharField(max_length=50)
    prezime = models.CharField(max_length=50)
    telefon = models.IntegerField()
    mail = models.EmailField(max_length=254)
    patuvanja_mtm = models.ManyToManyField(Patuvanje)