from django.db import models
from django.core.validators import MinValueValidator


class QuoteForm(models.Model):
    quote_choices = [
        ('offer-one', 'Package Type One - $250'),
        ('offer-two', 'Package Type Two - $500'),
        ('offer-three', 'Package Type Three - $1000'),
    ]

    client_name = models.CharField(max_length=100)
    yearly_salary = models.FloatField(validators=[MinValueValidator(0)])
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=10)
    quote_type = models.CharField(max_length=20, choices=quote_choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['client_name', 'client_email']
        app_label = 'FinalProj'

    def __str__(self):
        return self.client_name


class VerifyQuote(models.Model):
    quote = models.OneToOneField('QuoteForm', on_delete=models.CASCADE, default=None)
    is_verified = models.BooleanField(default=False)
    admin_notif_sent = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Verify Quote'

    def validate_quote(self):
        client_salary = self.quote.yearly_salary
        quote_type = self.quote.quote_type

        if quote_type == 'offer-one' and client_salary < 25000:
            return False
        elif quote_type == 'offer-two' and client_salary < 50000:
            return False
        elif quote_type == 'offer-three' and client_salary < 100000:
            return False
        else:
            return True

    def save(self, *args, **kwargs):
        if self.validate_quote():
            self.is_verified = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quote.client_name} - Verified: {self.is_verified} "


class QueryDatabase(models.Model):
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()

    class Meta:
        verbose_name = 'Query Database'

    def __str__(self):
        return f"{self.client_name} - {self.client_email}"
