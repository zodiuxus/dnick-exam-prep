from django.db import models
from django.db.models import CheckConstraint, Q, F, Sum
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.

#Patuvanja imaat mesto, vremetraenje i slika
class Patuvanje(models.Model):
    mesto = models.CharField(max_length = 255, unique = True)
    datum_pochetok = models.DateTimeField(auto_now=False, auto_now_add=False)
    vremetraenje = models.IntegerField()
    cena = models.IntegerField(default = 0)
    slika = models.ImageField(upload_to='data/')

# Vodachi imaat ime, prezime, telefon, email
# zaedno so relacija do patuvanja (m2m)
class Vodach(models.Model):

    class Meta:
        constraints: [
            CheckConstraint(
                check = Q(patuvanja_mtm__count__lte=F(5)),
                name = 'check_max_trips'
            )
        ]

    def clean(self):
        if self.pk:
            if self.vkupna_cena > 50000:
                raise ValidationError("Vkupnata cena na patuvanjata koi gi vodi " + self.ime + " e pregolema.")
            if self.patuvanja_mtm.count() > 5:
                raise ValidationError("Vodachot ima premnogu patuvanja! Trgnete dodeka nema maksimum 5 patuvanja i probajte pak.")

    @property
    def vkupna_cena(self):
        return self.patuvanja_mtm.aggregate(total = Sum('cena'))['total']

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    ime = models.CharField(max_length=50)
    prezime = models.CharField(max_length=50)
    telefon = models.IntegerField()
    mail = models.EmailField(max_length=254)
    patuvanja_mtm = models.ManyToManyField(Patuvanje)
    user = models.ForeignKey(User, on_delete = models.CASCADE)