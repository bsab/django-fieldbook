#!/usr/bin/env python
# coding: utf-8
import json
import requests

from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.views.generic.base import ContextMixin

from fieldbook_py import FieldbookClient
from fieldbook.models import FieldBookUser


class FieldBookSheetMixin(ContextMixin):
    """Mixing for fieldbook sheets views.

        :keyword sheet_name: A string with the sheet from the book, ex 'assignments'
        :keyword record_id: Row number to retrieve, if not positive real no row assumed, ex 1
        :keyword list_include: List of fields to include
        :keyword list_exclude: List of fields to exclude
        :keyword userprofile:
        :keyword fieldbook_url:

    """
    sheet_list = None
    sheet_name = None
    record_id = None
    list_include = None
    list_exclude = None
    userprofile = None
    fieldbook_url = None

    def get_context_data(self, **kwargs):
        """Update view context"""
        self.userprofile = self.get_fieldbook_user()
        self.fieldbook_url = self.get_fieldbook_url();

        context = super(FieldBookSheetMixin, self).get_context_data(**kwargs)
        context.update({
            'fbuser': self.userprofile,
            'list_include': self.list_include,
            'list_exclude': self.list_exclude
        })
        return context

    def get_fieldbook_url(self):
        """Book base URL displayed in the API management panel."""
        return settings.FIELDBOOK_BASE_URL + \
                             settings.FIELDBOOK_VERSION + \
                             '/' + \
                             self.userprofile.fieldbook_book;

    def get_client(self):
        """Get Fieldbook client instance."""
        userprofile = self.get_fieldbook_user()

        fieldbook_url = settings.FIELDBOOK_BASE_URL + \
                        settings.FIELDBOOK_VERSION + \
                        '/' + \
                        userprofile.fieldbook_book;

        print "connecting to ", fieldbook_url, " ...."
        # ok connection
        fb = FieldbookClient(userprofile.fieldbook_api_key,
                             userprofile.fieldbook_api_secret,
                             fieldbook_url)
        return fb;

    def get_fieldbook_user(self):
        """Return current fieldbookuser profile."""

        u = User.objects.get(username=self.request.user)
        up = None;
        try:
            up = FieldBookUser.objects.get(user=u)
        except :
            pass
        return up;

    def get_sheet_list(self,
                       fieldbook_url,
                       fieldbook_api_key,
                       fieldbook_api_secret):
        """Return the array of sheets associated with the book."""
        request = requests.get(fieldbook_url,
                               auth=(fieldbook_api_key,
                                     fieldbook_api_secret),
                               params={})
        # raise an exception for error codes (4xx or 5xx)
        request.raise_for_status()
        return json.loads(request.text)


class FieldbookSheetIndexView(FieldBookSheetMixin, TemplateView):
    """View suitable to work with Fieldbook Sheet List.
       Returns the list of sheet names on the book.

       The view responsive for handling GET/POST requests from the browser
       and AJAX from the datatable.
    """
    def get_context_data(self, **kwargs):
        context = super(FieldbookSheetIndexView, self).get_context_data(**kwargs)

        self.sheet_list = self.get_sheet_list(self.fieldbook_url,
                                              self.userprofile.fieldbook_api_key,
                                              self.userprofile.fieldbook_api_secret);
        context.update({
            'sheet_list': self.sheet_list,
        })
        return context


class FieldbookSheetTableView(FieldBookSheetMixin, TemplateView):
    """View suitable to work with Fieldbook Sheet List.
       Returns the list of sheet names on the book.

       The view responsive for handling GET/POST requests from the browser
       and AJAX from the datatable.
    """
    sheet_table = None

    def get_context_data(self, **kwargs):
        context = super(FieldbookSheetTableView, self).get_context_data(**kwargs)

        if 'sheet_name' in self.kwargs:
            self.sheet_name = self.kwargs['sheet_name']
        print 'sheet_name', self.sheet_name

        self.sheet_table = self.get_sheet_table(self.sheet_name);
        context.update({
            'sheet_name': self.sheet_name,
            'sheet_table': self.sheet_table,
        })
        return context

    def get_sheet_table(self, sheet_name):
        """Returns an array of records from a particular sheet."""
        fb = self.get_client()
        rows = fb.get_all_rows(sheet_name)
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
        """Update view context.

        Include `sheet_name` and 'record_id' to
        first page render.
        """
        context = super(FieldbookSheetEntryView, self).get_context_data(**kwargs)

        if 'sheet_name' in self.kwargs:
            self.sheet_name = self.kwargs['sheet_name']

        if 'record_id' in self.kwargs:
            self.record_id = self.kwargs['record_id']
        context.update({
            'sheet_name': self.sheet_name,
            'record_id': self.record_id,
        })

        return context

    def get_sheet_entry(self, sheet_name, record_id):
        """Return a specific record in a sheet."""
        fb = self.get_client()
        entry = fb.get_row(sheet_name,
                          record_id,
                          self.list_include,
                          self.list_exclude)

        return entry

    def remove_sheet_entry(self, sheet_name, record_id):
        """Remove a specific record in a sheet. """
        fb = self.get_client()
        entry = fb.delete_row(sheet_name,
                             record_id)

        return entry

        #@method_decorator(login_required)
    #def dispatch(self, request, *args, **kwargs):
    #    return super(FieldbookSheetEntryView, self).dispatch(request, *args, **kwargs)