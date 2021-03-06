from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea(attrs={'autofocus': ''}))

    class Meta:
        model = Note
        fields = ('note',)
