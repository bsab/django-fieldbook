#!/usr/bin/env python
# coding: utf-8
import json
import requests

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView, View, ListView, DeleteView, DetailView
from django.contrib.auth.models import User
from django.views.generic.base import ContextMixin, TemplateResponseMixin

from fieldbook.operators import FieldbookClient
from fieldbook.models import FieldBookUser


class FieldbookException(Exception):
    def __init__(self, status_code, message):
        #override public fields
        self.status_code = status_code
        self.message = message

class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        """
        Convert the context dictionary into a JSON object.
        """
        try:
            del context['view'] #to avoid no JSON serializable exception
        except:
            pass

        return json.dumps(context)


class FieldBookSheetMixin(ContextMixin):
    """Mixing for fieldbook sheets views.

        :keyword sheet_name: A string with the sheet from the book, ex 'assignments'
        :keyword record_id: Row number to retrieve, if not positive real no row assumed, ex 1
        :keyword list_include: List of fields to include
        :keyword list_exclude: List of fields to exclude
    """
    record_id = None
    sheet_name = None
    ordering = None
    list_include = None
    list_exclude = None

    def get_context_data(self, **kwargs):
        """Update view context"""

        if 'sheet_name' in self.kwargs:
            self.sheet_name = self.kwargs['sheet_name']
        print 'sheet_name', self.sheet_name

        if 'record_id' in self.kwargs:
            self.record_id = self.kwargs['record_id']
        print 'record_id', self.record_id

        context = super(FieldBookSheetMixin, self).get_context_data(**kwargs)

        userprofile = self.get_fieldbook_user()
        context.update({
            'book_id': userprofile.fieldbook_book,
            'record_id': self.record_id,
            'sheet_name': self.sheet_name,
            'list_include': self.list_include,
            'list_exclude': self.list_exclude
        })
        return context

    def get_client(self):
        print "get_client"
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
            up = FieldBookUser.objects.get(user=u)
        except:
            pass
        return up;


class FieldbookSheetIndexView(FieldBookSheetMixin, TemplateView):
    """View suitable to work with Fieldbook Sheet List.
       Returns the list of sheet names on the book.

       The view responsive for handling GET/POST requests from the browser
       and AJAX from the datatable.
    """
    def get_context_data(self, **kwargs):
        context = super(FieldbookSheetIndexView, self).get_context_data(**kwargs)
        context['message'] ='Please search a sheet within the book specified'
        return context



class FieldbookSheetListView(FieldBookSheetMixin, TemplateView):
    """View suitable to work with Fieldbook Sheet List.
       Returns the list of sheet names on the book.

       The view responsive for handling GET/POST requests from the browser
       and AJAX from the datatable.
    """
    list_sheets = None

    def get_context_data(self, **kwargs):
        context = super(FieldbookSheetListView, self).get_context_data(**kwargs)
        self.list_sheets = self.get_sheets();

        context.update({
            'list_sheets': self.list_sheets,
        })
        return context

    def get_sheets(self):
        """Returns a list of sheets within the book specified at instantiation."""
        fb = self.get_client()
        rows = fb.get_all_rows(self.sheet_name)
        print rows
        if not rows:
            return []
        return rows

    #def render_to_response(self, context, **response_kwargs):
    #    return self.render_to_json_response(context)

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
        """Returns an array of records from a particular sheet. """
        fb = self.get_client()
        print "self.sheet_name-->", self.sheet_name
        print "self.record_id-->", self.record_id
        item = fb.get_row(self.sheet_name,
                          self.record_id,
                          self.list_include,
                          self.list_exclude)
        print item
        return item

    #@method_decorator(login_required)
    #def dispatch(self, request, *args, **kwargs):
    #    return super(FieldbookSheetEntryView, self).dispatch(request, *args, **kwargs)

