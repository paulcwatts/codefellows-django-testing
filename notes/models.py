from django.core.urlresolvers import reverse
from django.db import models


class Note(models.Model):
    note = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('note-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.note
