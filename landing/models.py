from django.db import models

from django.db import models

class Contestant(models.Model):
    name_or_group_name = models.CharField(max_length=100)
    email = models.EmailField()
    talent_description = models.TextField()
    is_group = models.BooleanField(default=False)
    group_size = models.PositiveIntegerField(null=True, blank=True)
    video_submission = models.FileField(upload_to='videos/', null=True, blank=True)

    
    def __str__(self):
        return self.name_or_group_name