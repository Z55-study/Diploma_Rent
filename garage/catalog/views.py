from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from catalog.forms import RenewBikeForm
from django.views import generic
from .models import Bike, Author, BikeInstance, Typ
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


def index(request):
    # Сгенерировать подсчет велосипедов
    num_bikes = Bike.objects.all().count()
    num_instances = BikeInstance.objects.all().count()
    # Доступные велосипеды
    num_instances_available = BikeInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # По умолчанию подразумевается 'all ()'.

    # Количество посещений, подсчитанное в переменной сеанса.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # HTML-шаблон index.html с данными в переменной контекста.
    return render(
        request,
        'index.html',
        context={'num_bikes': num_bikes, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_visits': num_visits},
    )


class BikeListView(generic.ListView):
    model = Bike
    paginate_by = 10


class BikeDetailView(generic.DetailView):
    model = Bike


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBikesByUserListView(LoginRequiredMixin, generic.ListView):
    model = BikeInstance
    template_name = 'catalog/bikeinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BikeInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBikesAllListView(PermissionRequiredMixin, generic.ListView):
    model = BikeInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bikeinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BikeInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_bike_librarian(request, pk):
    bike_instance = get_object_or_404(BikeInstance, pk=pk)

    if request.method == 'POST':

        form = RenewBikeForm(request.POST)

        if form.is_valid():
            bike_instance.due_back = form.cleaned_data['renewal_date']
            bike_instance.save()

            # перенаправить на новый URL:
            return HttpResponseRedirect(reverse('all-borrowed'))


    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBikeForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'bike_instance': bike_instance,
    }

    return render(request, 'catalog/bike_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


# Классы, созданные для вызова форм
class BikeCreate(PermissionRequiredMixin, CreateView):
    model = Bike
    fields = ['title', 'author', 'summary', 'isbn', 'typ', 'sex']
    permission_required = 'catalog.can_mark_returned'


class BikeUpdate(PermissionRequiredMixin, UpdateView):
    model = Bike
    fields = ['title', 'author', 'summary', 'isbn', 'typ', 'sex']
    permission_required = 'catalog.can_mark_returned'


class BikeDelete(PermissionRequiredMixin, DeleteView):
    model = Bike
    success_url = reverse_lazy('bikes')
    permission_required = 'catalog.can_mark_returned'
