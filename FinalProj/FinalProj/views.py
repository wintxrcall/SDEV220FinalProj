from django.shortcuts import render
from .forms import QuoteRequestForm, QuoteQueryForm
from .models import QuoteForm, VerifyQuote


def request_quote(request):
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)

        if form.is_valid():
            context = form.cleaned_data
            quote = QuoteForm.objects.create(
                client_name=context['client_name'],
                client_email=context['client_email'],
                yearly_salary=context['yearly_salary'],
                client_phone=context['client_phone'],
                quote_type= context['quote_type'],
            )
            # verify = VerifyQuote(quote=quote)
            # verify.save()
            verify = VerifyQuote.objects.create(quote=quote)
            # verify.validate_quote()

            return render(request, 'quote_saved.html', context)

    else:
        form = QuoteRequestForm()
        return render(request, 'request_quote.html', {'form': form})


def query_quotes(request):
    require_verif_quotes = VerifyQuote.objects.filter(is_verified=False)

    if request.method == 'GET':
        form = QuoteQueryForm(request.GET)
        if form.is_valid():
            client_email = form.cleaned_data.get('client_email', '')
            client_name = form.cleaned_data.get('client_name', '')
            if client_email and client_name:
                queried_quotes = QuoteForm.objects.filter(
                    client_email__icontains=client_email,
                    client_name__icontains=client_name
                )

            return render(request, 'quote_list.html', {'quotes': queried_quotes,
                                               'require_verif_quotes': require_verif_quotes,
                                               'form': form})
    else:
        form = QuoteQueryForm()

    return render(request, 'quote_list.html', {
        'require_verif_quotes': require_verif_quotes,
        'form': form
    })


def quote_saved(request):
    return render(request, 'quote_saved.html')


def failed_quotes(request):
    need_verif_quotes = VerifyQuote.objects.filter(is_verified=False)

    failed_quotes = [verify_quote.quote for verify_quote in need_verif_quotes]

    return render(request, 'quote_list.html', {'require_verif_quotes': failed_quotes})
