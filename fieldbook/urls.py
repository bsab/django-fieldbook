from django.conf.urls import url, include

from fieldbook.views.user import FieldBookUserRegistration
from fieldbook.demo import SheetListView, SheetEntryView

urlpatterns = [
    url(r'^user-register/$', FieldBookUserRegistration.as_view(), name="fieldbook_registration"),

    #list sheets
    url(r'^sheet-list/book_name=(?P<book_name>[-\w]+)/$', SheetListView.as_view(), name='fieldbooksheet_list'),
    #single sheet by id
    url(r'^sheet-entry-(?P<record_id>\w+)/book_name=(?P<book_name>[-\w]+)/$', SheetEntryView.as_view(), name='fieldbooksheet_entry'),

]