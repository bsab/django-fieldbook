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

from views import SheetListView, SheetEntryView

urlpatterns = [
    url('^$', login_required(generic.TemplateView.as_view(template_name="index.html")), name="index"),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),

    url(r'^fieldbook/', include('fieldbook.urls')),

    # list sheets
    url(r'^sheet-list/book_name=(?P<book_name>[-\w]+)/$', SheetListView.as_view(), name='sheet_list'),
    # single sheet by id
    url(r'^sheet-entry-(?P<record_id>\w+)/book_name=(?P<book_name>[-\w]+)/$', SheetEntryView.as_view(),
        name='sheet_entry'),

]
