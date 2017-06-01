django-fieldbook
================

django-fieldbook is a reusable Django app for interacting with the Fieldbook.com API.
Fieldbook is the fastest and easiest way to create custom information tools.
It’s as easy to get started with as a spreadsheet, but gives you all the power of a
database-driven business application. Teams use it to track projects and clients,
implement data collection workflows, and create custom content management systems.

Overview
--------

Django-Fieldbook works with Django 1.8/1.9/1.10/1.11


Quick start
-----------

-  Setup Django-fieldbook application in Python environment:

   ::

       $ pip install django-fieldbook


-  Migrate the fieldbook app to create the user model:

   ::
        $ migrate fieldbook

-  Add "fieldbook" to your INSTALLED\_APPS setting like this:

   ::

       INSTALLED_APPS = (
           ...,
           'fieldbook',
       )

- Write your views with different types (in view.py file or if you want in a nameview.py file):

    * A view to get the list of sheet names on the book extending the FieldbookSheetIndexView:

   ::

    class IndexView(FieldbookSheetIndexView):
        """Index class based view.

        Return the list of sheets associated with the book and render it
        into a bootstrap list-group.
        """
        template_name = "index.html"

        def get_context_data(self, **kwargs):
            context = super(IndexView, self).get_context_data(**kwargs)
            return context

        @method_decorator(login_required)
        def dispatch(self, request, *args, **kwargs):
            return super(IndexView, self).dispatch(request, *args, **kwargs)


   * A view to get the list of records on the selected sheet extending the FieldbookSheetTableView:

   ::

    class SheetTableView(FieldbookSheetTableView):
        """Sheet class based view.

        Returns the array of records (object) for the sheet and render it
        into a jquery datatable.
        """
        template_name = "index.html"

        def get_context_data(self, **kwargs):
            context = super(SheetTableView, self).get_context_data(**kwargs)
            return context


   * A view to get a specific record in a sheet extending the FieldbookSheetEntryView:

   ::

    class SheetEntryView(FieldbookSheetEntryView):
        """Return or remove a specific record in a sheet.

        If is present the url pramater 'to_delete', the current
        entry is removed.
        """
        template_name = "index.html"

        def get_context_data(self, **kwargs):
            """Update view context."""
            context = super(SheetEntryView, self).get_context_data(**kwargs)

            entry_to_delete = kwargs.get("to_delete", False)
            if entry_to_delete:
                context.update({
                    'sheet_entry': self.remove_sheet_entry(self.sheet_name, self.record_id),
                })
            else:
                context.update({
                    'sheet_entry': self.get_sheet_entry(self.sheet_name, self.record_id),
                })
            return context

        @method_decorator(login_required)
        def dispatch(self, request, *args, **kwargs):
            return super(SheetEntryView, self).dispatch(request, *args, **kwargs)

   * Then you need to map the views to an url in url.py file:

   ::

    url('^$', IndexView.as_view(), name="index"),
    # list sheets
    url(r'^sheet-table/sheet_name=(?P<sheet_name>[-\w]+)/$', SheetTableView.as_view(), name='sheet_table'),
    # single sheet by id
    url(r'^sheet-entry-(?P<record_id>\w+)/sheet_name=(?P<sheet_name>[-\w]+)/$', SheetEntryView.as_view(),
        name='sheet_entry'),
    url(r'^sheet-entry-(?P<record_id>\w+)/sheet_name=(?P<sheet_name>[-\w]+)/delete/$', SheetEntryView.as_view(),
        {'to_delete': True}, name='sheet_entry_delete'),


-  If you want you can use the base FieldBookUser model or extend it defining a simple model like this example:

   ::

       from fieldbook.models import FieldBookUser
       class CustomFieldBookUser(FieldBookUser):
           nick = models.CharField(max_length=100)

- Map the login, logout and register to an url in url.py:

    ::

    url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^fieldbook/', include('fieldbook.urls')),
