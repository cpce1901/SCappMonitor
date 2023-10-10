from django.views.generic import ListView, FormView, View
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import LoginForm, UpdatePassForm


# Create your views here.
class Login(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("sensors_app:places")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(username=username, password=password)

        if user:
            login(self.request, user)
            return super(Login, self).form_valid(form)
        else:
            messages.error(
                self.request,
                "La credenciales ingresadas no son validas. Inténtalo de nuevo.",
            )
            return self.form_invalid(form)


class Logout(View):
    def get(self, request, *args, **kargs):
        messages.info(self.request, "Haz cerrado la secion exitosamente.")
        logout(request)
        return HttpResponseRedirect(reverse("users_app:login"))


class UpdatePass(LoginRequiredMixin, FormView):
    template_name = "users/updatepass.html"
    form_class = UpdatePassForm
    success_url = reverse_lazy("users_app:login")

    def form_valid(self, form):
        usuario = self.request.user
        current_password = form.cleaned_data["password1"]
        new_password = form.cleaned_data["password2"]

        if usuario.check_password(current_password):
            usuario.set_password(new_password)
            usuario.save()
            update_session_auth_hash(self.request, usuario)
            messages.success(
                self.request,
                "Contraseña actualizada con éxito. Por favor, inicia sesión nuevamente.",
            )
            return super().form_valid(form)
        else:
            messages.error(
                self.request, "La contraseña actual no es válida. Inténtalo de nuevo."
            )

            return self.form_invalid(form)


class DetailUser(LoginRequiredMixin, ListView):
    template_name = "users/detailuser.html"
    model = get_user_model()
    context_object_name = "usuario"
    login_url = reverse_lazy("users_app:login")
