from django.shortcuts import render
from .forms import NumberForm
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Wspolczynnik
class Rata:
    def __init__(self, numer_raty, kwota_raty, data):
        self.numer_raty = numer_raty
        self.kwota_raty = kwota_raty
        self.data = data

    # def get_book_info(self):
    #     return f'Tytuł: {self.title}, Autor: {self.author}, Data wydania: {self.release_date}'
    #
    # def is_recent(self):
    #     """
    #     Sprawdza, czy książka została wydana w ciągu ostatnich 5 lat.
    #
    #     :return: True jeśli książka jest nowa, False w przeciwnym razie
    #     """
    #     from datetime import datetime
    #
    #     current_year = datetime.now().year
    #     release_year = self.release_date.year
    #
    #     return (current_year - release_year) <= 5


#c - cena, r - ilosc rat, w - wspolczynnik: 1,0065, d - odstep dni, n numer raty
# def kalkulator_raty(c,r,w,d,n):
#     return (c/r+(c-(c/r*n))*(pow(w,d)-1))

def kalkulator_raty(c, r, w, d, n):
    # Zakładam, że c, r, w i d są zdefiniowane w tej funkcji
    c = Decimal(c)  # Przykładowe przypisanie
    r = Decimal(r)  # Upewnij się, że te wartości są Decimal
    w = Decimal(w)  # Konwertuj float na Decimal
    d = Decimal(d)  # Przykład, upewnij się, że i jest odpowiednie

    # Obliczenia
    return round((c/r+(c-(c/r*n))*(pow(w,d)-1)),2)
def home(request):
    model_wspolczynnik=Wspolczynnik.objects.first()
    wspolczynnyk=model_wspolczynnik.value
    numbers = None
    date = datetime(1, 1,1)
    price = None
    ilosc_rat=0
    if request.method == 'POST':
        form = NumberForm(request.POST)
        if form.is_valid():
            #ilosc rat
            number1 = form.cleaned_data['number1']
            ilosc_rat=int(number1)
            #odstep dni
            number2 = form.cleaned_data['number2']
            date = form.cleaned_data['date']
            price = form.cleaned_data['price']
            numbers = (number1, number2)

    else:
        form = NumberForm()

    # iter=[]
    #
    # for i in range(ilosc_rat):
    #     iter.append(i+1)
    #
    # indexy=[]
    # for i in range(ilosc_rat):
    #     iter.append(i)

    lista_rat = []
    for i in range(ilosc_rat):
        if i!=ilosc_rat-1:
            rata=""
            kwota_raty=kalkulator_raty(price,number1,wspolczynnyk,number2,i+1)
            rata=str(kwota_raty)+" zł"
            lista_rat.append(rata)
        else:
            rata=""
            kwota_raty=round(price/number1,2)
            rata=str(kwota_raty)+" zł"
            lista_rat.append(rata)


    lista_dat=[]
    # Ustal datę
    data = datetime(date.year, date.month, date.day)
    for i in range(ilosc_rat):
        # Dodaj 5 dni

        nowa_data = data + timedelta(days=(number2*i))
        nowa_data_str = nowa_data.strftime('%d.%m.%Y')
        lista_dat.append(nowa_data_str)

    # Zapisz wynik jako string w formacie 'DD.MM.YYYY'

    raty=[]
    for i in range(ilosc_rat):
        rata=Rata(i+1,lista_rat[i],lista_dat[i])
        raty.append(rata)

    # Wyświetl wynik
    # print(nowa_data_str)

    return render(request, 'base/home.html', {'form': form, 'numbers': numbers, 'date': date, 'iter':iter, 'raty':raty})
