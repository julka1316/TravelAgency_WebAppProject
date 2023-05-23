from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-customer', views.add_customer, name='add_customer'),
    path('add-trip', views.add_trip, name='add_trip'),
    path('buy-ticket', views.buy_ticket, name='buy_ticket'),
    path('list-customer', views.list_customer, name='list_customer'),
    path('list-trips', views.list_trips, name='list_trips'),
    path('show-trip/<trip_id>', views.show_trip, name = 'show-trip'),
    path('customer-orders/<customer_id>', views.customer_orders, name='customer_orders'),
    path('analytics', views.analytics, name='analytics'),
    path('transactions-csv', views.get_transactions_csv),
    path('transactions-pdf', views.pobierz_pdf),
    path('delete_event/<event_id>', views.delete_event, name='delete-event'),
    #path('student/edytuj/<int: student_id>/edytuj_studenta')

]