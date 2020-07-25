from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.formats import localize
from django.views.generic import DeleteView, CreateView, UpdateView, View, RedirectView

from .filters import BookingFilter
from .models import Booking
from .forms import BookingForm, BonusSpendForm
from .tasks import telegram_bot_sendtext_task


# Главная страница, на которой есть форма с записью на брови
class IndexView(View):
    def render(self, request):
        return render(request, 'index.html')

    def get(self, request):
        return self.render(request)


class BookingCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'booking.can_add_booking'
    model = Booking
    fields = '__all__'


class BookingUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'booking.can_change_booking'
    model = Booking
    fields = '__all__'


class BookingDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'booking.can_delete_booking'
    model = Booking
    success_url = reverse_lazy('bookings')


# Список всех бронирований для админа
@login_required
@permission_required('auth.can_add_permission')
def booking_list(request):
    queryset = Booking.objects.filter(status='p').order_by('date')
    booking_filter = BookingFilter(request.GET, queryset=queryset)

    paginator = Paginator(booking_filter.qs, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'booking_list.html', {'filter': booking_filter,
                                                 'page_obj': page_obj})


# Список посещений
@login_required
@permission_required('auth.can_add_permission')
def done_booking_list(request):
    queryset = Booking.objects.filter(status='d').order_by('date')
    booking_filter = BookingFilter(request.GET, queryset=queryset)

    paginator = Paginator(booking_filter.qs, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'done_booking_list.html', {'filter': booking_filter,
                                                      'page_obj': page_obj})


# Меняет статус бронирования на завершенное
# Если бронирования закреплено за пользователем, то
# ему начисляется посещение и бонусные баллы
class BonusRedirectView(PermissionRequiredMixin, LoginRequiredMixin, RedirectView):

    permission_required = 'booking.can_delete_booking'
    pattern_name = 'bookings'
    url = 'booking_list/'

    def get_redirect_url(self, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs['pk'])
        booking.status = 'd'

        if booking.client:
            client = booking.client
            client.visits += 1
            booking.price = int(Booking.PRICE_LIST[booking.work])
            booking.booking_bonus = booking.price / 10
            client.bonus_points += booking.booking_bonus
            client.save()

        booking.save()
            
        return reverse_lazy('bookings')


# Если клиент посетил, но оплачивает со списанием баллов
# Тогда баллы не будут начислены, наоборот, списаны.
class BonusSpendView(View):

    def render(self, request):
        return render(request, 'bonus_spend.html', {'form': self.form})

    def post(self, request, pk):
        self.form = BonusSpendForm(request.POST)

        if self.form.is_valid():
            booking = get_object_or_404(Booking, pk=pk)
            booking.status = 'd'

            client = booking.client
            client.visits += 1
            booking.bonus_spent = int(self.form.cleaned_data['bonus_points'])
            client.bonus_points -= booking.bonus_spent
            booking.price = int(Booking.PRICE_LIST[booking.work]) - booking.bonus_spent
            client.save()

            booking.save()

            return redirect(reverse('bookings'))

        return self.render(request)

    def get(self, request, pk):
        self.form = BonusSpendForm()
        return self.render(request)


class PricingView(View):

    def render(self, request):
        return render(request, 'pricing.html')

    def get(self, request):
        return self.render(request)


class ContactsView(View):

    def render(self, request):
        return render(request, 'contacts.html')

    def get(self, request):
        return self.render(request)


class BookingView(View):

    def render(self, request):
        return render(request, 'book_form.html', {'form': self.form})

    def post(self, request):
        self.form = BookingForm(request.POST)
        if self.form.is_valid():
            if self.request.user.is_authenticated:
                new_booking = self.form.save(commit=False)
                new_booking.client = self.request.user.profile
            new_booking = self.form.save()
            text = "*Новая запись:*\n\n*Дата:* {} в {}.\n*Адрес:* {}.\n*Клиент:* {}, {}.".format(
                localize(new_booking.date), new_booking.get_time_display(),
                new_booking.get_address_display(), new_booking.name,
                new_booking.phone)
            telegram_bot_sendtext_task.delay(text)
            return redirect(reverse('index'))
        return self.render(request)

    def get(self, request):
        if self.request.user.is_authenticated:
            self.form = BookingForm(initial={'name': self.request.user.get_short_name(),
                                             'phone': self.request.user.profile.phone})
        else:
            self.form = BookingForm()
        return self.render(request)
