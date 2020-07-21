from django import forms
from .models import Booking
from accounts.models import Profile


class BookingForm(forms.ModelForm):
    date = forms.DateField(input_formats=['%d-%m-%Y'],
                           label='Дата',
                           widget=forms.DateInput(format='%d-%m-%Y', attrs={'class': 'datepicker'}))

    class Meta:
        model = Booking
        fields = ('name', 'date', 'time', 'address', 'work', 'phone', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 1}),
        }
        labels = {
            "name": "Имя",
            "phone": "Телефон",
            "time": "Время",
            "work": "Услуга",
            "comment": "Комментарий",
            "address": "Адрес",
        }

    # Проверка на то, что дата не занята
    def clean(self):
        new_date = self.cleaned_data.get('date')
        new_time = self.cleaned_data.get('time')
        db_date = Booking.objects.filter(date=new_date).filter(time=new_time)

        if db_date:
            raise forms.ValidationError("Простите, на данное время уже есть запись")
        return self.cleaned_data


class BonusSpendForm(forms.ModelForm):
    bonus_points = forms.IntegerField(required=True, label='Списать бонусов')

    class Meta:
        model = Profile
        fields = ('bonus_points',)
