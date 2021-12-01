from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # для проверки диапазона дат продления.

from django import forms


class RenewBikeForm(forms.Form):

    renewal_date = forms.DateField(
            help_text="Введите дату от настоящего момента до 4 недель (по умолчанию 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Дата проверки не в прошлом.
        if data < datetime.date.today():
            raise ValidationError(_('Недействительная дата - продление в прошлом'))
        # Дата проверки находится в диапазоне, который может изменить Админ (+4)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Недействительная дата - продление более чем на 4 недели вперед'))


        return data