from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from fieldbook.views.sheet import FieldbookException, FieldbookSheetListView, FieldbookSheetEntryView

#Returns the list of sheet names on the book.
class SheetListView(FieldbookSheetListView):
    page = None
    paginate_by = 5
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        print "SheetListView::get_context_data"
        context = super(SheetListView, self).get_context_data(**kwargs)

        try:
            list_sheets_paginated = self.paginate_sheets(self.list_sheets);
            context.update({
                #'datatable_config': json.dumps(self.get_datatable_config()),
                'headers': self.get_sheet_headers(self.list_sheets) ,
                'data': self.get_sheet_data(list_sheets_paginated),
                'page_obj': list_sheets_paginated,
            })
        except TypeError as te: # list_sheets not is an array but a dict {'message':error-message}
            print "TypeError-->", str(te)
            if type(self.list_sheets) is dict:
                if 'message' in self.list_sheets:
                    context.update({
                        'message_error': self.list_sheets['message']
                    })
                else:
                    context.update({
                        'message_error': str(te)
                    })
            else:
                context.update({
                    'message_error': str(te),
                })
        except Exception as e:  # generic exception
                context.update({
                    'message_error': str(e),
                })
        print "context:", context
        return context

    def get_datatable_config(self):
        """Prepare datatable config."""
        config = self.datatable_default_config.copy()
        config['pageLength'] = self.paginate_by
        config['ajax']['url'] = self.request.path
        #config['columns'] = self.get_columns_def()

        # aggiorno il context data
        config['oLanguage']['oPaginate']['sFirst'] = "1"
        config['oLanguage']['oPaginate']['sLast'] = "5"
        config['oLanguage']['oPaginate']['sNext'] = "&rang;"
        config['oLanguage']['oPaginate']['sPrevious'] = "&lang;"

        if self.datatable_config is not None:
            config.update(self.datatable_config)
        print "config"
        print config
        return config

    def get_sheet_headers(self, list_sheets):
        """Readable column titles."""
        if len(list_sheets) > 0:
            for k in list_sheets[0].keys():
                yield k, k

    def get_sheet_data(self, list_sheets):
        """Get a page for datatable."""

        for item in list_sheets:#[start:start + length]:
            columns = OrderedDict()
            for field_name in item.keys():
                value = item[field_name]
                columns[field_name] = value

            print "*", item, "--", columns, "*"
            yield item, columns

    def paginate_sheets(self, list_sheets):
        """Get a page for datatable."""
        paginator = Paginator(list_sheets, self.paginate_by)

        page = self.request.GET.get('p')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        print "paginator-->", paginator
        print "page.count-->", paginator.count
        print "page.num_pages-->", paginator.num_pages

        return file_exams


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SheetListView, self).dispatch(request, *args, **kwargs)

# Return a specific record in a sheet. OPTIONS can include include/exclude options just as list() can.
class SheetEntryView(FieldbookSheetEntryView, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(SheetEntryView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SheetEntryView, self).dispatch(request, *args, **kwargs)

