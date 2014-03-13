from django.conf.urls import patterns, url

from .views import NoteList, NoteDetail


urlpatterns = patterns('notes.views',
    url(r'^$', NoteList.as_view(), name='note-list'),
    url(r'^(?P<pk>\d+)/$', NoteDetail.as_view(), name='note-detail')
)
