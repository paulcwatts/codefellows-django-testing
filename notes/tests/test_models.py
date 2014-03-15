from datetime import datetime, timedelta

from django.test import TestCase

from notes.models import Note


class ModelsTest(TestCase):
    def test_ordering(self):
        "Notes are ordered most recent first."
        now = datetime.utcnow()

        # We want to be deliberate about the timestamps, so we're not
        # at the mercy of the test timing.
        note1 = Note.objects.create(note='Older note', timestamp=now - timedelta(days=1))
        note2 = Note.objects.create(note='Newer note', timestamp=now)
        self.assertQuerysetEqual(Note.objects.all(), [note2.pk, note1.pk],
                                 transform=lambda note: note.pk)
