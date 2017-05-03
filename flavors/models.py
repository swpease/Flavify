from django.db import models

# Create your models here.

class Ingredient(models.Model):
    base_item = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50, blank=True)
    tastes = models.ManyToManyField('Taste')

    def __str__(self):
        return '{} {}'.format(self.base_item, self.subcategory)

class Taste(models.Model):
    TONGUE_MAP = (
        ('Sweet', 'Sweet'),
        ('Salty', 'Salty'),
        ('Sour', 'Sour'),
        ('Bitter', 'Bitter'),
        ('Umami', 'Umami'),
        ('Spicy', 'Spicy'),  # mustard
        ('Numbing', 'Numbing'),  # Szechuan peppercorns
        ('Cooling', 'Cooling'),  # mint
    )

    mouth_taste = models.CharField(max_length=20, choices=TONGUE_MAP)

    def __str__(self):
        return self.mouth_taste
