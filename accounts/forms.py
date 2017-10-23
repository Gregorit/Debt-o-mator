from django import forms

from accounts.models import Debtor


class DebtorForm(forms.ModelForm):
    class Meta:
        model = Debtor
        fields = '__all__'
