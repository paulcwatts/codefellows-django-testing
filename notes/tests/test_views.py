from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import formats

from notes.models import Note


class ViewsTest(TestCase):
    def test_empty_list(self):
        "Viewing an empty list shows the list empty hint text with the add note link"
        response = self.client.get(reverse('note-list'))
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertContains(response, 'You have no notes.')
        self.assertContains(response,
                            '<a href="{0}">Add note</a>'.format(reverse('note-add')),
                            html=True)

    def test_note_list(self):
        "Viewing a list with a note contains the note."
        Note.objects.create(note='TEST NOTE')  # Automatically cleaned up each test
        response = self.client.get(reverse('note-list'))
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertNotContains(response, 'You have no notes.')
        self.assertContains(response, 'TEST NOTE')

    def test_note_detail(self):
        "Viewing the note detail shows the note and updated time."
        note = Note.objects.create(note='TEST NOTE')  # Automatically cleaned up each test
        response = self.client.get(note.get_absolute_url())
        self.assertTemplateUsed(response, 'notes/note_detail.html')
        self.assertContains(response, 'TEST NOTE')
        self.assertContains(response, formats.date_format(note.timestamp))

    def test_note_add(self):
        "Viewing the add form show the appropriate version of the form."
        response = self.client.get(reverse('note-add'))
        self.assertTemplateUsed(response, 'notes/note_form.html')

        # One way of testing the context data
        self.assertEqual('Add note', response.context['title'])
        self.assertEqual('Add', response.context['submit_text'])

        # Another way of testing the context data and template
        self.assertContains(response, '<h1>Add note</h1>')
        self.assertContains(response, '<button type="submit">Add</button>', html=True)

    def test_note_add_post_success(self):
        "Submitting the form creates a new note and redirects to the note-list screen."

        # client.post will replicate submitting the form from the browser.
        response = self.client.post(reverse('note-add'), {
            'note': 'Remember to write unit tests.'
        })
        self.assertRedirects(response, reverse('note-list'))
        self.assertEqual(1, Note.objects.count())
        self.assertEqual('Remember to write unit tests.', Note.objects.all()[0].note)

    def test_note_add_post_error(self):
        "The note value is required."
        response = self.client.post(reverse('note-add'), {
            'note': ''
        })
        self.assertTemplateUsed(response, 'notes/note_form.html')
        self.assertFormError(response, 'form', 'note', ['This field is required.'])

    def test_note_update(self):
        "Editing a note displays the note form with the value preset."
        note = Note.objects.create(note='Remember to write unit tests.')
        response = self.client.get(reverse('note-update', kwargs={'pk': note.pk}))
        self.assertTemplateUsed(response, 'notes/note_form.html')

        # One way of testing the context data
        self.assertEqual('Edit note', response.context['title'])
        self.assertEqual('Save', response.context['submit_text'])

        # Another way of testing the context data and template
        self.assertContains(response, '<h1>Edit note</h1>')
        self.assertContains(response, '<button type="submit">Save</button>', html=True)
        self.assertContains(response, """
            <textarea cols="40" id="id_note" name="note" rows="10">
                Remember to write unit tests.
            </textarea>""", html=True)

    def test_note_update_success(self):
        "Updating a note redirects you back to the detail page."
        note = Note.objects.create(note='Remember to write unit tests.')
        url = reverse('note-update', kwargs={'pk': note.pk})
        response = self.client.post(url, {
            'note': 'Unit tests are great.'
        })
        self.assertRedirects(response, note.get_absolute_url())

        # Since model instances are cached, we need to re-get the object to test
        note = Note.objects.get(pk=note.pk)
        self.assertEqual('Unit tests are great.', note.note)

    def test_note_update_error(self):
        "You can't update to an empty note. (Basically tests the same code as add, but why not?)"
        note = Note.objects.create(note='Remember to write unit tests.')
        url = reverse('note-update', kwargs={'pk': note.pk})
        response = self.client.post(url, {
            'note': ''
        })
        self.assertTemplateUsed(response, 'notes/note_form.html')
        self.assertFormError(response, 'form', 'note', ['This field is required.'])

    def test_delete_confirm(self):
        "Deleting a note prompts you and contains the note."
        note = Note.objects.create(note='Remember to write unit tests.')
        response = self.client.get(reverse('note-delete', kwargs={'pk': note.pk}))

        self.assertTemplateUsed(response, 'notes/note_confirm_delete.html')
        self.assertContains(response, 'Remember to write unit tests.')

    def test_delete_confirm_success(self):
        "Deleting a note redirects you to the note list. The note is deleted."
        note = Note.objects.create(note='Delete this note.')
        response = self.client.post(reverse('note-delete', kwargs={'pk': note.pk}))
        self.assertRedirects(response, reverse('note-list'))

        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(pk=note.pk)

        # The view is longer accessible
        response = self.client.get(note.get_absolute_url())
        self.assertEqual(404, response.status_code)
