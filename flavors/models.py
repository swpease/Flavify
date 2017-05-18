from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

"""Current logic for all ingredients / names: keep plurality as singular (e.g. "mushroom", not "mushrooms").

   Notes on order of creation:
     - Must create an Ingredient instance before a dependent AltName instance.
     - Must create an Ingredient instance without any tastes before tastes can be assigned.
       Tastes must be derived from the existing Tastes:
         x = Ingredient.objects.create(listed_name="x", umbrella_cat="")
         tastes = Taste.objects.all()
         x.tastes.add(tastes[0], tastes[3])
       To view x's tastes, use x.tastes.all()
"""
class Ingredient(models.Model):
    """
    RELATIONSHIPS: Taste - many-to-many, "forward"
                   AltName - one-to-many, "backward"
                   Combination – many-to-many, "backward"
    listed_name: Case-insensitive, and must be written in normal words (e.g: "morel mushroom", NOT "morel_mushroom").
                 Represents the title of a given ingredients page.
    umbrella_cat: Same restrictions as listed_name, PLUS it must itself be a listed_name.
                  If an ingredient makes sense as a "parent", it goes here.
                    Example 1: listed_name = "Morel mushroom", umbrella_cat = "Mushroom"
                    Example 2: listed_name = "Szechuan peppercorn", umbrella_cat = ""
    """
    listed_name = models.CharField(max_length=50, unique=True)
    umbrella_cat = models.CharField(max_length=30, blank=True)
    tastes = models.ManyToManyField('Taste', blank=True)  # Do I want to be able to list a relative magnitude somehow?

    def save(self, *args, **kwargs):
        """Auto-creates the reflexive AltName object."""
        super(Ingredient, self).save(*args, **kwargs)
        try:
            AltName.objects.get(name=self.listed_name)
        except ObjectDoesNotExist:
            AltName.objects.create(name=self.listed_name, ingredient=self)

    def __str__(self):
        # umb = ", under " + self.umbrella_cat if self.umbrella_cat else ". No umbrella category."
        return self.listed_name

    class Meta:
        ordering = ['listed_name']


class AltName(models.Model):
    """
    name: Case-insensitive, and must be written in normal words.
          Represents a valid name for an ingredient. (e.g.: "filbert" : "hazelnut" and "hazelnut" : "hazelnut")
    """
    name = models.CharField(max_length=50)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: Listed as {}'.format(self.name, self.ingredient)


class Taste(models.Model):
    """
    RELATIONSHIPS: Ingredient – many-to-many, "backward"
    mouth_taste: A collection of words that one can use to describe flavor.
    """
    TONGUE_MAP = (
        ('sweet', 'sweet'),
        ('salty', 'salty'),
        ('sour', 'sour'),
        ('bitter', 'bitter'),
        ('umami', 'umami'),
        ('spicy', 'spicy'),  # mustard
        ('numbing', 'numbing'),  # Szechuan peppercorns
        ('cooling', 'cooling'),  # mint
    )

    mouth_taste = models.CharField(max_length=20, choices=TONGUE_MAP)

    def __str__(self):
        return self.mouth_taste


class Combination(models.Model):
    """
    RELATIONSHIPS: Ingredient – many-to-many, "forward"
    tries: Number of users who have confirmed that they tried the combination
    datetime_submitted: auto-generated upon Combination creation
    submittor: user who submitted the Combination
    """
    tries = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    datetime_submitted = models.DateTimeField(auto_now_add=True)
    submittor = models.CharField(max_length=100, default="admin")
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        ingreds = [i.listed_name for i in self.ingredients.all()]
        return " ".join(ingreds)
