from django.db import models
from django.contrib.auth.models import User

class Site_User(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    FACULTY = 'FC'
    STUDENT = 'ST'

    TYPE_OF_USER_CHOICES = [
        (FACULTY, 'Faculty'),
        (STUDENT, 'Student'),
    ]

    type = models.CharField(
        max_length=2,
        choices=TYPE_OF_USER_CHOICES,
        default=STUDENT,
    )

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
