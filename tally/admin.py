from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Ledger_old)

admin.site.register(Company)
admin.site.register(CompanyCostCategory)
admin.site.register(CompanyCurrency)
admin.site.register(CompanyGroup)
admin.site.register(CompanyTax)
admin.site.register(CostCentre)
admin.site.register(Godowns)
admin.site.register(Ledger)
admin.site.register(StockCategory)
admin.site.register(StockGroups)
admin.site.register(StockItem)
admin.site.register(UnitOfMeasurement)
admin.site.register(VoucherType)
admin.site.register(Voucher)