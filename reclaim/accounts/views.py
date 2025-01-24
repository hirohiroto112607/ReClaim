from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import CreateView

from .forms import SignUpForm
from .models import User

# Create your views here.


class IndexView(TemplateView):
    """ ホームビュー """
    template_name = "accounts/index.html"


class SignupView(CreateView):
    """ ユーザー登録用ビュー """
    form_class = SignUpForm  # 作成した登録用フォームを設定
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:index")  # ユーザー作成後のリダイレクト先ページ

    def form_valid(self, form):
        # ユーザー作成後にそのままログイン状態にする設定
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return response


class LoginForm(AuthenticationForm):
    class Meta:
        model = User


class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("accounts:index")


def profile(request):
    return render(request, "accounts/profile.html")


def logout_get(request):
    return render(request, "accounts/logout.html")


def edit_profile(request):
    # return render(request, "accounts/edit_profile.html")
    form = SignUpForm()
    if request.method == 'POST':
        # form = RegisterForm(request.POST)
        if form.is_valid():
            item_instance = form.save()
            return redirect('', )
    else:
        form = SignUpForm()
    return render(request, 'accounts/edit_profile.html',)


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        print(request.user.id)
        user_data = User.objects.get(id=request.user.id)
        print(user_data.birth_date)
        form = SignUpForm(
            request.POST or None,
            initial={
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'birth_date': user_data.birth_date,
            }
        )

        return render(request, 'accounts/edit_profile.html', {
            'form': form,
            'user_data': user_data
        })

    def post(self, request, *args, **kwargs):
        user_data = User.objects.get(id=request.user.id)
        form = SignUpForm(request.POST, request.FILES, instance=user_data)
        if form.is_valid():
            user_data = User.objects.get(id=request.user.id)
            user_data.email = form.cleaned_data['email']
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.birth_date = form.cleaned_data['birth_date']
            print(user_data.birth_date)
            user_data.save()
            return redirect('accounts:profile')
        else:
            return render(request, 'accounts/profile.html', {
                'form': form
            })


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context