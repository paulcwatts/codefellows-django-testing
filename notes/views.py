from django.views.generic import DetailView, ListView

from .models import Note


class NoteList(ListView):
    model = Note
    context_object_name = 'notes'


class NoteDetail(DetailView):
    model = Note
    context_object_name = 'note'
