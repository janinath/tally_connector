from django.db import models

# Create your models here.
class Ledger(models.Model):
    name = models.CharField(max_length=255)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=12, decimal_places=2)
    parent = models.CharField(max_length=255, null=True, blank=True)
    def _str_(self):
        return self.name