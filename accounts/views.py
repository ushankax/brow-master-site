from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, View, UpdateView

from .forms import SignUpForm, EditUserForm, EditProfileForm
from .models import Profile
from booking.models import Booking


class SignUpView(View):
    def render(self, request):
        return render(request, 'signup.html', {'form': self.form})

    def post(self, request):
        self.form = SignUpForm(request.POST)

        if self.form.is_valid():
            user = self.form.save()
            user.refresh_from_db()
            user.profile.phone = self.form.cleaned_data.get('phone')
            user.profile.save()
            auth_login(request, user)
            return redirect('/')
        return self.render(request)

    def get(self, request):
        self.form = SignUpForm()
        return self.render(request)


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookings = self.object.bookings.filter(status='d').order_by('date')
        paginator = Paginator(bookings, 5)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context['bookings'] = bookings
        context['paginator'] = paginator
        context['page_number'] = page_number
        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'accounts/user_form.html'

    def get_success_url(self):
        return reverse_lazy('user-profile', kwargs={'pk': self.object.pk})


class UpdateProfileView(LoginRequiredMixin, View):

    def render(self, request):
        return render(request, 'accounts/edit_profile.html', {'user_form': self.user_form,
                                                              'profile_form': self.profile_form})

    def get(self, request):
        self.user_form = EditUserForm(initial={'email': self.request.user.email})
        self.profile_form = EditProfileForm(initial={'phone': self.request.user.profile.phone})
        return self.render(request)

    def post(self, request):
        self.user_form = EditUserForm(request.POST)
        self.profile_form = EditProfileForm(request.POST)
        user = get_object_or_404(User, pk=self.request.user.pk)

        if self.user_form.is_valid() and self.profile_form.is_valid():
            user.email = self.user_form.cleaned_data['email']
            user.profile.phone = self.profile_form.cleaned_data['phone']
            user.save()

            return redirect(reverse('user-profile', kwargs={'pk': self.request.user.profile.pk}))

        return self.render(request)