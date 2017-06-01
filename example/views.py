from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from fieldbook.views.sheet import FieldbookSheetIndexView, FieldbookSheetTableView, FieldbookSheetEntryView


class IndexView(FieldbookSheetIndexView, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)


#Returns the list of sheet names on the book.
class SheetTableView(FieldbookSheetTableView):
    page = None
    paginate_by = 5
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        print "SheetTableView::get_context_data"
        context = super(SheetTableView, self).get_context_data(**kwargs)

        try:
            sheet_table_paginated = self.paginate_sheets(self.sheet_table);
            context.update({
                'headers': self.get_sheet_headers(self.sheet_table) ,
                'data': self.get_sheet_data(sheet_table_paginated),
                'sheet_table_paginated': sheet_table_paginated,
            })
        except TypeError as te: # sheet_table not is an array but a dict {'message':error-message}
            if type(self.sheet_table) is dict:
                if 'message' in self.sheet_table:
                    context.update({
                        'message_error': self.sheet_table['message']
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

    def get_sheet_headers(self, sheet_table):
        """Readable column titles."""
        if len(sheet_table) > 0:
            for k in sheet_table[0].keys():
                yield k, k

    def get_sheet_data(self, sheet_table):
        """Get a page for datatable."""

        for item in sheet_table:#[start:start + length]:
            columns = OrderedDict()
            for field_name in item.keys():
                value = item[field_name]
                columns[field_name] = value

            print "*", item, "--", columns, "*"
            yield item, columns

    def paginate_sheets(self, sheet_table):
        """Get a page for datatable."""
        paginator = Paginator(sheet_table, self.paginate_by)

        page = self.request.GET.get('p')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        return file_exams


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SheetTableView, self).dispatch(request, *args, **kwargs)

class SheetEntryView(FieldbookSheetEntryView, TemplateView):
    """Return a specific record in a sheet.
    OPTIONS can include include/exclude options just as list() can.
    """
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(SheetEntryView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SheetEntryView, self).dispatch(request, *args, **kwargs)


class SheetEntryView(FieldbookSheetEntryView, TemplateView):
    """Remove a specific record in a sheet.
    """
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(SheetEntryView, self).get_context_data(**kwargs)

        entry_to_delete = kwargs.get("to_delete", False)
        print "SheetEntryView::entry_to_delete", entry_to_delete
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
