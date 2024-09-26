from django.urls import path
from . import views
app_name = 'tally'
urlpatterns = [
    path('import/', views.import_ledger_data, name='import_ledger_data'),
    path('ledgers/', views.list_ledgers, name='ledger_list'),
]