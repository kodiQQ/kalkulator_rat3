from django import forms

class NumberForm(forms.Form):
    price = forms.DecimalField(label='Cena skina (z buffa w PLN)', max_digits=10, decimal_places=2)
    number1 = forms.IntegerField(label='Liczba rat:')
    number2 = forms.IntegerField(label='Odstęp (liczba dni pomiędzy ratami):')
    date = forms.DateField(label='Data pierwszej raty', widget=forms.DateInput(attrs={'type': 'date'}))
