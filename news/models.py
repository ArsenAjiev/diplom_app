from django.db import models

from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255)
    pubDate = models.DateTimeField()
    link = models.URLField()
    image = models.CharField(max_length=255, null=True, blank=True)

    def str(self):
        return self.title
