import requests

from django.conf import settings
from django.views.generic import TemplateView, View, ListView, DeleteView, DetailView
from django.contrib.auth.models import User
from django.views.generic.base import ContextMixin, TemplateResponseMixin

from fieldbook.operators import FieldbookClient
from fieldbook.models import UserProfile, FieldBookSheet


class FieldbookException(Exception):
    def __init__(self, status_code, message):
        #override public fields
        self.status_code = status_code
        self.message = message


class FieldBookSheetMixin(ContextMixin):
    """Mixing for fieldbook sheets views.

        :keyword list_include: List of fields to include
        :keyword list_exclude: List of fields to exclude
    """
    record_id = None
    book_name = None
    ordering = None
    list_include = ('__str__',)
    list_exclude = ('__str__',)

    def get_context_data(self, **kwargs):
        """Update view context"""

        if 'book_name' in self.kwargs:
            self.book_name = self.kwargs['book_name']
        print 'book_name', self.book_name

        if 'record_id' in self.kwargs:
            self.record_id = self.kwargs['record_id']
        print 'record_id', self.record_id

        context = super(FieldBookSheetMixin, self).get_context_data(**kwargs)
        context.update({
            'record_id': self.record_id,
            'book_name': self.book_name,
            'list_include': self.list_include,
            'list_exclude': self.list_exclude
        })
        return context

    def get_client(self):
        """Get Fieldbook client."""

        userprofile = self.get_fieldbook_user()

        fieldbook_url = settings.FIELDBOOK_BASE_URL + \
                        settings.FIELDBOOK_VERSION + \
                        '/' + \
                        userprofile.fieldbook_book;

        print "connecting to ", fieldbook_url, " ...."
        print userprofile.fieldbook_api_key
        print userprofile.fieldbook_api_secret

        #check connection
        print "checking connection"
        try:
            request = requests.get(fieldbook_url,
                                   auth=(userprofile.fieldbook_api_key,
                                         userprofile.fieldbook_api_secret),
                                   params ={})
            # raise an exception for error codes (4xx or 5xx)
            request.raise_for_status()

            # ok connection
            fb = FieldbookClient(userprofile.fieldbook_api_key,
                                 userprofile.fieldbook_api_secret,
                                 fieldbook_url)
            return fb;

        except requests.ConnectionError as e:
            raise FieldbookException(status_code=request.status_code,
                                     message='Cannot connect to Fieldbook API ' + str(e))

        except requests.HTTPError as e2:
            raise FieldbookException(status_code=request.status_code,
                                     message='Error while connect to Fieldbook API ' + str(e2))

    def get_fieldbook_user(self):
        """Return current fieldbookuser profile."""

        u = User.objects.get(username=self.request.user)
        up = None;
        try:
            up = UserProfile.objects.get(user=u)
        except:
            pass
        return up;


class FieldbookSheetListView(FieldBookSheetMixin, TemplateView):
    """View suitable to work with Fieldbook Sheet List.
       Returns the list of sheet names on the book.

       The view responsive for handling GET/POST requests from the browser
       and AJAX from the datatable.
    """

    def get_context_data(self, **kwargs):
        context = super(FieldbookSheetListView, self).get_context_data(**kwargs)
        context.update({
            'list_sheets': self.get_sheets(),
        })
        return context

    def get_sheets(self):
        #try:
        fb = self.get_client()
        rows = fb.get_all_rows(self.book_name)
        print "rows---------->", rows
        print "type---------->", type(rows)
        if not rows:
            return []
        return rows
        #except FieldbookException as fbe:
        #    print "FieldbookException ", str(fbe.message)
        #    return []

    #@method_decorator(login_required)
    #def dispatch(self, request, *args, **kwargs):
    #    return super(FieldbookSheetListView, self).dispatch(request, *args, **kwargs)


class FieldbookSheetEntryView(FieldBookSheetMixin, TemplateView):
    """View suitable to work with Fieldbook Sheet record.
       Return a specific record in a sheet. OPTIONS can
       include/exclude options just as list() can.

       The view responsive for handling GET/POST requests from the browser
       and AJAX from the datatable.
    """

    def get_context_data(self, **kwargs):
        context = super(FieldbookSheetEntryView, self).get_context_data(**kwargs)
        context.update({
            'sheet_entry': self.get_sheet_entry(),
        })
        return context

    def get_sheet_entry(self):
        fb = self.get_client()
        item = fb.get_row(self.book_name,
                          self.record_id,
                          self.list_include,
                          self.list_exclude)
        return item

    #@method_decorator(login_required)
    #def dispatch(self, request, *args, **kwargs):
    #    return super(FieldbookSheetEntryView, self).dispatch(request, *args, **kwargs)
