from django import forms
from .models import QuoteForm, QueryDatabase


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteForm
        fields = [
            'client_name',
            'yearly_salary',
            'client_email',
            'client_phone',
            'quote_type',
        ]


class QuoteQueryForm(forms.ModelForm):
    class Meta:
        model = QueryDatabase
        fields = [
            'client_name',
            'client_email',
        ]
