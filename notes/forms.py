from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Note
        fields = ('note',)
