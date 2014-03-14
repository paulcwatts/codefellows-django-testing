from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)
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

    def get_context_data(self, **kwargs):
        context = super(NoteCreate, self).get_context_data(**kwargs)
        context['title'] = 'Add note'
        context['submit_text'] = 'Add'
        return context


class NoteUpdate(UpdateView):
    model = Note
    form_class = NoteForm

    def get_context_data(self, **kwargs):
        context = super(NoteUpdate, self).get_context_data(**kwargs)
        context['title'] = 'Edit note'
        context['submit_text'] = 'Save'
        return context


class NoteDelete(DeleteView):
    model = Note
    success_url = reverse_lazy('note-list')
