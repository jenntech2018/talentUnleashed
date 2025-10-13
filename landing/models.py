from django.db import models

class Contestant(models.Model):
    name_or_group_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    talent_description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_or_group_name