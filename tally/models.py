from django.db import models

# Create your models here.
class Ledger_old(models.Model):
    name = models.TextField(max_length=255)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=12, decimal_places=2)
    parent = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.name
    
from django.db import models

class Company(models.Model):
    guid = models.CharField(max_length=100, primary_key=True)
    company = models.CharField(max_length=100)
    gstin_number = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=50, blank=True, null=True)
    starting_from = models.CharField(max_length=100, blank=True, null=True)
    end_in_gat = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    fax = models.CharField(max_length=100, blank=True, null=True)
    company_email = models.CharField(max_length=100, blank=True, null=True)
    company_website = models.CharField(max_length=100, blank=True, null=True)
    company_last_voucher_date = models.CharField(max_length=100, blank=True, null=True)
    cmpvch_alter_id = models.CharField(max_length=100, blank=True, null=True)
    cmpmst_alter_id = models.CharField(max_length=100, blank=True, null=True)
    alt_master_id = models.CharField(max_length=100, blank=True, null=True)

class CompanyCostCategory(models.Model):
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    alter_id = models.IntegerField(blank=True, null=True)
    allocate_non_revenue = models.CharField(max_length=100, blank=True, null=True)
    allocate_revenue = models.CharField(max_length=100, blank=True, null=True)
    guid = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.CharField(max_length=100, blank=True, null=True)

class CompanyCurrency(models.Model):
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    guid = models.CharField(max_length=100, blank=True, null=True)
    master_id = models.CharField(max_length=100, blank=True, null=True)
    alter_id = models.CharField(max_length=100, blank=True, null=True)
    symbol = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    decimal_places = models.CharField(max_length=10, blank=True, null=True)
    show_in_millions = models.CharField(max_length=10, blank=True, null=True)
    decimal_places_in_words = models.CharField(max_length=10, blank=True, null=True)
    is_suffix = models.CharField(max_length=10, blank=True, null=True)

class CompanyGroup(models.Model):
    alter_id = models.IntegerField(blank=True, null=True)
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    group_positive = models.CharField(max_length=50, blank=True, null=True)
    guid = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.CharField(max_length=100, blank=True, null=True)

class CompanyTax(models.Model):
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    gst = models.CharField(max_length=200, blank=True, null=True)
    last_voucher_date = models.CharField(max_length=50, blank=True, null=True)
    number_of_ledgers = models.IntegerField(blank=True, null=True)

class CostCentre(models.Model):
    guid = models.CharField(max_length=100, blank=True, null=True)
    master_id = models.CharField(max_length=100, blank=True, null=True)
    alter_id = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.CharField(max_length=100, blank=True, null=True)
    opening_balance_revenue = models.CharField(max_length=200, blank=True, null=True)
    for_job_casting = models.CharField(max_length=10, blank=True, null=True)
    for_payroll = models.CharField(max_length=10, blank=True, null=True)
    email_id = models.CharField(max_length=100, blank=True, null=True)
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)

class Godowns(models.Model):
    guid = models.CharField(max_length=100, blank=True, null=True)
    master_id = models.CharField(max_length=100, blank=True, null=True)
    alter_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    our_stock_with_third_party = models.CharField(max_length=10, blank=True, null=True)
    third_party_stock_with_us = models.CharField(max_length=10, blank=True, null=True)
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)

class Ledger(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.CharField(max_length=100, blank=True, null=True)
    gstin = models.CharField(max_length=100, blank=True, null=True)
    vattin = models.CharField(max_length=100, blank=True, null=True)
    guid = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    income_tax_number = models.CharField(max_length=100, blank=True, null=True)
    bill_credit_period = models.CharField(max_length=100, blank=True, null=True)
    is_tds_applicable = models.CharField(max_length=10, blank=True, null=True)
    tds_deductee_type = models.CharField(max_length=100, blank=True, null=True)
    gst_registration_type = models.CharField(max_length=100, blank=True, null=True)
    ledger_positive = models.CharField(max_length=10, blank=True, null=True)
    alter_id = models.CharField(max_length=100, blank=True, null=True)
    opening_balance = models.CharField(max_length=50, blank=True, null=True)
    closing_balance = models.CharField(max_length=50, blank=True, null=True)
    iso_debit = models.CharField(max_length=10, blank=True, null=True)
    iscb_debit = models.CharField(max_length=10, blank=True, null=True)
    ledger_contact_person = models.CharField(max_length=100, blank=True, null=True)
    ledger_phone = models.CharField(max_length=100, blank=True, null=True)
    ledger_mobile = models.CharField(max_length=100, blank=True, null=True)
    ledger_fax = models.CharField(max_length=100, blank=True, null=True)
    ledger_email = models.CharField(max_length=100, blank=True, null=True)
    ledger_email_cc = models.CharField(max_length=100, blank=True, null=True)
    ledger_state = models.CharField(max_length=100, blank=True, null=True)
    ledger_country = models.CharField(max_length=100, blank=True, null=True)
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)

class StockCategory(models.Model):
    guid = models.CharField(max_length=100, blank=True, null=True)
    master_id = models.CharField(max_length=100, blank=True, null=True)
    alter_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.CharField(max_length=100, blank=True, null=True)
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)

class StockGroups(models.Model):
    guid = models.CharField(max_length=100, blank=True, null=True)
    master_id = models.CharField(max_length=100, blank=True, null=True)
    alter_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.CharField(max_length=100, blank=True, null=True)
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)

class StockItem(models.Model):
    guid = models.CharField(max_length=100, blank=True, null=True)
    master_id = models.CharField(max_length=100, blank=True, null=True)
    alter_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    group = models.CharField(max_length=100, blank=True, null=True)
    opening_balance = models.CharField(max_length=100, blank=True, null=True)
    closing_balance = models.CharField(max_length=100, blank=True, null=True)
    stock_positive = models.CharField(max_length=10, blank=True, null=True)
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)

class UnitOfMeasurement(models.Model):
    guid = models.CharField(max_length=100, blank=True, null=True)
    master_id = models.CharField(max_length=100, blank=True, null=True)
    alter_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    abbreviation = models.CharField(max_length=100, blank=True, null=True)
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)

class VoucherType(models.Model):
    guid = models.CharField(max_length=100, blank=True, null=True)
    master_id = models.CharField(max_length=100, blank=True, null=True)
    alter_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.CharField(max_length=100, blank=True, null=True)
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)

class Voucher(models.Model):
    guid = models.CharField(max_length=100, blank=True, null=True)
    master_id = models.CharField(max_length=100, blank=True, null=True)
    alter_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.CharField(max_length=100, blank=True, null=True)
    company_guid = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)

    
    
    
    
    