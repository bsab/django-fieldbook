from django.conf.urls import url, include

from fieldbook.views.user import FieldBookUserRegistration

urlpatterns = [
    url(r'^user-register/$', FieldBookUserRegistration.as_view(), name="fieldbook_registration"),
]