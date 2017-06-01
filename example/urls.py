"""django_fieldbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views import generic
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from views import IndexView, SheetTableView, SheetEntryView

urlpatterns = [
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),

    url(r'^fieldbook/', include('fieldbook.urls')),

    url('^$', IndexView.as_view(), name="index"),
    # list sheets
    url(r'^sheet-table/sheet_name=(?P<sheet_name>[-\w]+)/$', SheetTableView.as_view(), name='sheet_table'),
    # single sheet by id
    url(r'^sheet-entry-(?P<record_id>\w+)/sheet_name=(?P<sheet_name>[-\w]+)/$', SheetEntryView.as_view(),
        name='sheet_entry'),
    url(r'^sheet-entry-(?P<record_id>\w+)/sheet_name=(?P<sheet_name>[-\w]+)/delete/$', SheetEntryView.as_view(),
        {'to_delete': True}, name='sheet_entry_delete'),

]
