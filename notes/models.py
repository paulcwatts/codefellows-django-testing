from django.db import models


class Note(models.Model):
    note = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.note
