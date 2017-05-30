from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic.edit import FormView

from fieldbook.forms import RegistrationForm
from fieldbook.models import FieldBookUser

class FieldBookUserRegistration(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = '/sheets/'

    def get_context_data(self, **kwargs):
        context = super(FieldBookUserRegistration, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated():  # se vado sull'url register da autenticato torno alla home
            return HttpResponseRedirect(reverse('index'))
        return self.render_to_response(context)

    def form_valid(self, form):
        # Creo il nuovo utente (inattivo)
        user = form.save(commit=False);
        user.set_password(form.cleaned_data['password']);
        user.username = form.cleaned_data['username'].lower();
        user.username = form.cleaned_data['username'].lower();
        user.fieldbook_book= form.cleaned_data['fieldbook_book'];
        user.email = form.cleaned_data['email'].lower();
        user.is_active = True;
        user.save();

        userprofile = FieldBookUser();
        userprofile.user = user;
        # saving the fieldbook key and password
        userprofile.fieldbook_api_key = form.cleaned_data['username'].lower();
        userprofile.fieldbook_api_secret = form.cleaned_data['password'];

        userprofile.save();

        # Effettuo il login
        user_logged = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password']);
        login(self.request, user_logged);

        return HttpResponseRedirect(self.get_success_url())
