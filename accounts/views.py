from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, DeleteView

from accounts.decorators import user_login_required
from accounts.forms import DebtorForm
from accounts.models import Debtor


@user_login_required
class DebtorTotalListView(TemplateView):
    template_name = 'accounts/debtor_list.html'

    def get_context_data(self, **kwargs):
        records = []
        dict = {}
        dict_person = []

        for deb_x in Debtor.objects.all():
            if {'in_debt': deb_x.in_debt,
                'owes': deb_x.owes,
                'amount': 0}\
                    not in dict_person:
                dict_person.append({'in_debt': deb_x.in_debt,
                                    'owes': deb_x.owes,
                                    'amount': 0})

            if {'in_debt': deb_x.owes,
                'owes': deb_x.in_debt,
                'amount': 0}\
                    not in dict_person:
                dict_person.append({'in_debt': deb_x.owes,
                                    'owes': deb_x.in_debt,
                                    'amount': 0})

        for deb in Debtor.objects.all():
            records.append({'id': deb.pk,
                            'in_debt': deb.in_debt,
                            'owes': deb.owes,
                            'item_name': deb.item_name,
                            'category': deb.category,
                            'amount': deb.amount})

            if deb.in_debt in dict:
                dict[deb.in_debt] += deb.amount
            else:
                dict[deb.in_debt] = deb.amount

            if deb.owes in dict:
                dict[deb.owes] -= deb.amount
            else:
                dict[deb.owes] = -deb.amount

            for row in dict_person:
                if row['in_debt'] == deb.in_debt and row['owes'] == deb.owes:
                    row['amount'] += deb.amount
                if row['in_debt'] == deb.owes and row['owes'] == deb.in_debt:
                    row['amount'] -= deb.amount
        context = super(DebtorTotalListView, self).get_context_data(**kwargs)
        context['records'] = records
        context['dict'] = dict
        context['dict_person'] = dict_person
        return context


@user_login_required
class DebtorDeleteView(DeleteView):
    model = Debtor
    success_url = reverse_lazy('show')


@user_login_required
class HomeView(TemplateView):
    template_name = 'accounts/home.html'


@user_login_required
class DebtorView(FormView):
    template_name = 'accounts/debtors.html'
    form_class = DebtorForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return super(DebtorView, self).form_valid(form)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
