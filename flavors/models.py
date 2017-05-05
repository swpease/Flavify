from django.db import models

# Create your models here.

"""Current logic for all ingredients / names: keep plurality as singular (e.g. "mushroom", not "mushrooms")."""
class Ingredient(models.Model):
    """
    RELATIONSHIPS: Taste - many-to-many
                   AltName - one-to-many
    listed_name: Case-insensitive, and must be written in normal words (e.g: "morel mushroom", NOT "morel_mushroom").
                 Represents the title of a given ingredients page.
    umbrella_cat: Same restrictions as listed_name, PLUS it must itself be a listed_name.
                  If an ingredient makes sense as a "parent", it goes here.
                    Example 1: listed_name = "Morel mushroom", umbrella_cat = "Mushroom"
                    Example 2: listed_name = "Szechuan peppercorn", umbrella_cat = ""
    """
    listed_name = models.CharField(max_length=50)
    umbrella_cat = models.CharField(max_length=30, blank=True)
    tastes = models.ManyToManyField('Taste')

    def __str__(self):
        return '{} (also under: {})'.format(self.listed_name, self.umbrella_cat)


class AltName(models.Model):
    """
    name: Case-insensitive, and must be written in normal words.
          Represents a valid name for an ingredient. (e.g.: "filbert" : "hazelnut" and "hazelnut" : "hazelnut")
    """
    name = models.CharField(max_length=50)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return '{} listed as {}'.format(self.name, self.ingredient)


class Taste(models.Model):
    """
    RELATIONSHIPS: many-to-many with Ingredient.
    mouth_taste: A collection of words that one can use to describe flavor.
    """
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
