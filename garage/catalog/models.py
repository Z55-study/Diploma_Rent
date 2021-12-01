from django.db import models

import uuid  # Требуется для уникальных экземпляров велосипедов
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse  # Создание URL-адресов путем изменения шаблонов URL-адресов


class Typ(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название',
        help_text="Введите тип велосипеда (например, Горный, Шоссейный, BMX и т.д."
    )

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name


class Sex(models.Model):
    name = models.CharField(max_length=200, verbose_name='Пол',
                            help_text="Введите подходящий пол человека (Мужской, Женский, Унисекс)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'


class Bike(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name='Производитель')
    # Используется внешний ключ, потому что у велосипеда может быть только один производитель, но у производителей может быть несколько велосипедов
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the bike",
                               verbose_name='Описание')
    isbn = models.CharField(max_length=13,
                            unique=True, verbose_name='№ рамы',
                            help_text=' Номера рамы расположены в разных местах <a href="https://www.sportek.in.ua/blogs/stati/gde-nanesen-seriynyy-nomer-velosipeda-ili-ego-ramy'
                                      '">Места распаложения</a>')
    typ = models.ManyToManyField(Typ, verbose_name='Тип велосипеда', help_text="Select a typ for this bike")
    # Используется ManyToManyField, потому что тип может может применяться ко многим велосипедам, а велосипед может охватывать многие типы.
    Sex = models.ForeignKey('Sex', verbose_name='Тип рамы', on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='photo/', verbose_name='Фото', blank=True, )

    class Meta:
        ordering = ['title', 'author']
        verbose_name = 'Велосипед'
        verbose_name_plural = 'Велосипеды'

    def display_typ(self):
        return ', '.join([typ.name for typ in self.typ.all()[:3]])

    display_typ.short_description = 'Typ'

    def get_absolute_url(self):
        return reverse('bike-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class BikeInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Уникальный идентификатор этого конкретного велосипеда во всем гараже")
    bike = models.ForeignKey('Bike', on_delete=models.RESTRICT, verbose_name='Веловиспед', null=True)
    imprint = models.CharField(max_length=200, verbose_name='Коментарий')
    due_back = models.DateField(null=True, verbose_name='Дата возврата', blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Зарезервировал', null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('d', 'Техническое обслуживание'),
        ('o', 'В изпользовании'),
        ('a', 'Доступен'),
        ('r', 'Скоро поступит'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d', verbose_name='Статус',
        help_text='Доступность Велосипеда')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set bike as returned"),)
        verbose_name = 'Бронь велосипеда'
        verbose_name_plural = 'Бронь велосипеда'

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.bike.title)


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя производителя')
    last_name = models.CharField(max_length=100, verbose_name='Страна производителя')
    date_of_birth = models.DateField(null=True, verbose_name='Основание фирмы', blank=True)
    date_of_death = models.DateField(null=True, verbose_name='Велосипед произведен', blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)

    class Meta:
        verbose_name = 'Производителя(й)'
        verbose_name_plural = 'Приозводители'
