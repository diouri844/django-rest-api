from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=150, name="name")
    bio = models.CharField(max_length=500, name="bio")
    createdAt = models.DateTimeField('created_at')
    updatedAt = models.DateTimeField('updated_at')

    def __str__(self):
        return f"hey i m {self.name} and here is my bio : {self.bio} thanks "