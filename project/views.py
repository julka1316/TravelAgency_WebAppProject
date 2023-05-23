import datetime
import json
import math
from xml.dom import minidom
import io
from django.http import FileResponse,HttpResponseRedirect
from reportlab.pdfgen import canvas

from django.core.exceptions import BadRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect

from project.forms import RegisterCustomerForm, RegisterTripForm, CustomerFilterForm, TripFilterForm
from project.models import Customer, Trip, Transaction, TransactionItem
from django.core.paginator import Paginator

DEFAULT_PAGE_SIZE = 5


def index(request):
    return render(request, 'project/index.html')


def add_customer(request):
    if request.method == 'POST':
        returned_form = RegisterCustomerForm(request.POST)
        customer = Customer(
            customername=returned_form.data['customername'],
            surname=returned_form.data['surname'],
            age=returned_form.data['age'],
            email=returned_form.data['email'],
        )
        customer.save()
        return redirect('index')
    else:
        form = RegisterCustomerForm()
        return render(request, 'project/add_customer.html', {'form': form})



def add_trip(request):
    if request.method == 'POST':
        returned_form = RegisterTripForm(request.POST, request.FILES)
        if returned_form.is_valid():
            returned_form.save()
            return HttpResponseRedirect('add-trip')
    else:
        form = RegisterTripForm()
        return render(request, 'project/add_trip.html', {'form': form})


def buy_ticket(request):
    if request.method == 'POST':
        raw = request.POST.get('order_payload')
        if raw != '':
            request_json = json.loads(raw)
            if is_valid_order_json(request_json):
                customer_id = request_json.get('user_id')
                customer = Customer.objects.get(pk=customer_id)
                items = request_json.get('items')

                total = 0
                transaction_items = []
                for item in items:
                    item_model = Trip.objects.get(pk=item['id'])
                    quantity = float(item['quantity'])
                    subtotal = float(item_model.price)-(float(item_model.price)*quantity)
                    total = total + subtotal
                    transaction_items.append(TransactionItem(item=item_model, quantity=quantity, subtotal=subtotal))

                transaction = Transaction(customer=customer, date =datetime.datetime.now(), total=total)
                transaction.save()

                for txn_item in transaction_items:
                    txn_item.save()

                transaction.items.set(transaction_items)
                transaction.save()

                return redirect('index')
            else:
                raise BadRequest('Invalid request content')
        else:
            raise BadRequest('Empty reqeust')
    else:
        customers = Customer.objects.all()
        products = Trip.objects.all()
        return render(
            request,
            'project/buy_ticket.html',
            {'customers': [c.json() for c in customers], 'products': [p.json() for p in products]}

        )

def customer_orders(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    transactions = Transaction.objects.filter(customer=customer)
    return render(request, 'project/customer_orders.html', {'customer': customer, 'transactions': transactions})

def analytics(request):
    now = datetime.datetime.now()
    thirty_day_ago = now - datetime.timedelta(days=30)
    transactions = Transaction.objects.filter(date__range=[thirty_day_ago, now])

    revenue_by_date = {}

    iteration_dt = thirty_day_ago.date()
    while iteration_dt <= now.date():
        revenue_by_date[str(iteration_dt)] = 0
        iteration_dt = iteration_dt + datetime.timedelta(days=1)

    for txn in transactions:
        dt = str(txn.date.date())
        revenue_by_date[dt] = revenue_by_date[dt] + float(txn.total)

    return render(request, 'project/analytics.html', {'revenue_by_date': revenue_by_date})

def get_transactions_csv(request):
    customer = Customer.objects.get(pk=request.GET.get('user_id'))
    transactions = Transaction.objects.filter(customer=customer)

    header_row = 'date;total\n'
    rows = [f'{txn.date};{txn.total}' for txn in transactions]

    csv = header_row + '\n'.join(rows)

    response = HttpResponse(csv, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{customer.customername.replace(" ", "_")}_transactions.csv"'
    return response

def pobierz_pdf(request):
    customer = Customer.objects.get(pk=request.GET.get('user_id'))

    transactions = Transaction.objects.filter(customer=customer)

    header_row = 'Data;Cenal\n'
    rows = [f'{txn.date};{txn.total}' for txn in transactions]


    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()


    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, f"Imię: {customer.customername}")
    p.drawString(100, 150, f"Nazwisko: {customer.surname}")
    p.drawString(100, 200, f"Wiek: {customer.age}")
    p.drawString(100, 250, f"Email: {customer.email}")
    for txn in transactions:
        p.drawString(100, 300, f"{txn.date}")
        p.drawString(100, 350, f"{txn.total};")
        #for item in item in txn.items.all:
            #p.drawString(100, 300, f"{item.item.tripname}")





    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename = f"customer_{request.GET.get('user_id')}.pdf")




def list_customer(request):
    customer_list = Customer.objects.all().order_by('surname', 'customername')
    formularz_wyszukiwania = CustomerFilterForm(request.GET)
    if formularz_wyszukiwania.is_valid():
        cd = formularz_wyszukiwania.cleaned_data
        if cd['age']:
            customer_list=customer_list.filter(age=cd['age'])
        if cd['surname']:
            customer_list = customer_list.filter(surname__startswith=cd['surname'])
        if cd['customername']:
            customer_list = customer_list.filter(customername__startswith=cd['customername'])
    paginator = Paginator(customer_list, 10)
    strona = request.GET.get('strona',1)
    return render(request, 'project/list_customer.html', {'paginator':paginator, 'customer_site':paginator.get_page(strona), 'formularz_wyszukiwania':formularz_wyszukiwania})

def list_trips(request):
    trip_list = Trip.objects.all().order_by('tripname')
    formularz_wyszukiwania = TripFilterForm(request.GET)
    if formularz_wyszukiwania.is_valid():
        cd = formularz_wyszukiwania.cleaned_data
        if cd['tripname']:
            trip_list=trip_list.filter(tripname__startswith=cd['tripname'])
        if cd['date']:
            trip_list = trip_list.filter(date=cd['date'])
        if cd['price']:
            trip_list = trip_list.filter(price=cd['price'])
    paginator = Paginator(trip_list, 7)
    strona = request.GET.get('strona',1)
    return render(request, 'project/list_trips.html', {'paginator':paginator, 'trip_site':paginator.get_page(strona), 'formularz_wyszukiwania':formularz_wyszukiwania})

def show_trip(request, trip_id):
    trip = Trip.objects.get(pk=trip_id)
    return render(request, 'project/show_trip.html', {'trip':trip})


def is_valid_order_json(order_json):
    has_two_keys = len(order_json.keys()) == 2
    correct_key_names = 'user_id' in order_json.keys() and 'items' in order_json.keys()
    correct_user = order_json.get('user_id') != -1
    correct_items = len(order_json.get('items')) != 0
    return has_two_keys and correct_key_names and correct_user and correct_items

def delete_event(request, event_id):
    event = Trip.objects.get(pk=event_id)
    event.delete()
    return redirect('list_trips')
