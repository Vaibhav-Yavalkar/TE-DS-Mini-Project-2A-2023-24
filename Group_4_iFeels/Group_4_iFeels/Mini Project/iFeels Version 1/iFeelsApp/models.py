from django.db import models

# makemigrations(meaning) => create changes and store in a file
# migrate(meaning) => apply the pending chamges created by makemigrations

# Create your models here.
class Contact(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class Sign_up(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    username = models.CharField(max_length=50)
    security_question = models.CharField(max_length=100)
    security_question_answer = models.CharField(max_length=255)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name