from django.db import models
from django.contrib.auth.models import User

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
    listed_name = models.CharField(max_length=50, unique=True)  # Do I want this to be the PK?

    def save(self, *args, **kwargs):
        """Auto-creates the reflexive AltName object."""
        super(Ingredient, self).save(*args, **kwargs)
        # Does not protect against manually entering the same altName multiple times
        AltName.objects.get_or_create(name=self.listed_name, ingredient=self)

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
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)

    def __str__(self):
        if self.ingredient.listed_name == self.name:
            return self.name
        else:
            return self.name + " (as " + self.ingredient.listed_name + ")"


class Combination(models.Model):
    """
    RELATIONSHIPS: Ingredient – many-to-many, "forward"
    tries: Number of users who have confirmed that they tried the combination
    datetime_submitted: auto-generated upon Combination creation
    submittor: user who submitted the Combination
    """
    ingredients = models.ManyToManyField(Ingredient)
    # Backwards, but avoids needing to customize the User model or create an unnecessary UserProfile model.
    users = models.ManyToManyField(User, through='UserComboData')

    tries = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    datetime_submitted = models.DateTimeField(auto_now_add=True)
    submittor = models.CharField(max_length=100, default="admin")

    # Might want to modify this if I am interested in likes/(likes + dislikes) vs likes/tries
    # TODO... some people could have notes on stuff they haven't tried yet.
    def calc_percent_likes(self):
        """
        Percent likes taken to be likes/tries.
        :return: percentage
        """
        all_opinions = UserComboData.objects.filter(combination=self).count()
        likes = UserComboData.objects.filter(combination=self, like=True).count()
        if all_opinions == 0:
            return 0  # Do I want to return 0 here, or what?
        else:
            return int((likes / all_opinions) * 100)

    def get_num_tried(self):
        """
        Number of tries should just be the number of instances of UserComboData with this Combination
        :return: non-negative int.
        """
        return UserComboData.objects.filter(combination=self).count()

    def __str__(self):
        ings = [i.listed_name for i in self.ingredients.all()]
        return " ".join(ings)


class IngredientSubmission(models.Model):
    """
    Standalone table that houses user-submitted ingredients (currently not in Ingredients table)
    for manual review.
    """
    submission = models.CharField(max_length=100,
                                  verbose_name='New Ingredient Submission',
                                  help_text='Submit a new ingredient to be able to pick for new flavor combinations.')
    datetime_submitted = models.DateTimeField(auto_now_add=True)
    submittor = models.CharField(max_length=100)  # Do I want to set editable=False?

    def __str__(self):
        return self.submission


class UserComboData(models.Model):
    """
    Extra fields for the User-Combo M2M relationship.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    combination = models.ForeignKey(Combination, on_delete=models.CASCADE)

    # Might want to change the widget from a checkbox to allow keyboard navigation
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    note = models.CharField(max_length=500, blank=True)
    # cooking_method = models.CharField(max_length=20, choices="TBD")
    # cuisine = models.CharField(max_length=50, choices="TBD")
