from django.views.generic import CreateView, DetailView, ListView
from django.core.urlresolvers import reverse_lazy

from .forms import NoteForm
from .models import Note


class NoteList(ListView):
    model = Note
    context_object_name = 'notes'


class NoteDetail(DetailView):
    model = Note
    context_object_name = 'note'


class NoteCreate(CreateView):
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy('note-list')
