from django.urls import path
from . import views
app_name = 'tally'
urlpatterns = [
    path('ledgers/', views.list_ledgers, name='ledger_list'),
    path('',views.import_successfull,name='import_successfull'),
    path('download-ledger-backup/', views.download_ledger_backup, name='download_ledger_backup'),
    path('download-custom-backup/', views.generate_custom_backup, name='download_custom_backup'),
]