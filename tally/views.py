from django.shortcuts import render,redirect
import requests
import xmltodict
from .models import Ledger
from django.http import JsonResponse
import xml.etree.ElementTree as ET
import re
# Create your views here.
TALLY_URL = 'http://localhost:9000'

# XML Request to fetch Ledger data from Tally
ledger_request_xml = """
<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>Ledger Vouchers</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>Abc</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>

"""

def parse_tally_response(xml_response):
    """
    Parse the XML response from Tally into a simple JSON format.
    """
    root = ET.fromstring(xml_response)  # Parse the XML response
    data = []

    # Iterate through each TALLYMESSAGE entry in the XML response and get ledgers
    for tally_message in root.findall(".//TALLYMESSAGE"):
        ledger = tally_message.find("LEDGER")
        if ledger is not None:
            # Extract basic ledger details
            ledger_data = {
                "name": ledger.get("NAME"),
                "parent": ledger.findtext("PARENT"),
                "closing_balance": ledger.findtext("CLOSINGBALANCE"),
            }
            data.append(ledger_data)
    
    return data



def list_ledgers(request):
    ledgers = Ledger.objects.all()
    return render(request, 'tally/ledger_list.html', {'ledgers': ledgers})

def fetch_tally_data(request):
    tally_request_xml = """
    <ENVELOPE>
        <HEADER>
            <TALLYREQUEST>Export Data</TALLYREQUEST>
        </HEADER>
        <BODY>
            <EXPORTDATA>
                <REQUESTDESC>
                    <REPORTNAME>List of Accounts</REPORTNAME>  <!-- Using List of Accounts report -->
                    <STATICVARIABLES>
                        <SVCURRENTCOMPANY>Abc</SVCURRENTCOMPANY><!-- Ensure correct company name -->
                        <EXPLODEVOUCHERS>Yes</EXPLODEVOUCHERS>
                        <SHOWOPENINGBALANCE>Yes</SHOWOPENINGBALANCE>
                        <SHOWCLOSINGBALANCE>Yes</SHOWCLOSINGBALANCE>
                        
                    </STATICVARIABLES>
                </REQUESTDESC>
            </EXPORTDATA>
        </BODY>
    </ENVELOPE>
    """

    headers = {'Content-Type': 'application/xml'}

    try:
        # Send HTTP POST request to TallyPrime
        response = requests.post(TALLY_URL, data=tally_request_xml, headers=headers)

        # Sanitize the raw XML response to avoid invalid characters
        sanitized_xml = sanitize_xml(response.text)

        print(sanitized_xml)  # Log the sanitized XML response to the terminal

        if response.status_code == 200:
            # Parse the sanitized XML response
            parsed_data = parse_tally_response(sanitized_xml)
            # Save parsed data to the Ledger model
            save_ledger_data({"tally_data": parsed_data})
            # return JsonResponse({"tally_data": parsed_data})
            return redirect ('tally:ledger_list')
        else:
            return JsonResponse({"error": "Failed to connect to Tally"}, status=500)
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
def import_ledger_data(request):
    tally_data = fetch_tally_data()
    
    if tally_data:
        ledgers = tally_data['ENVELOPE']['BODY']['DATA']['COLLECTION']['LEDGER']
        
        for ledger in ledgers:
            Ledger.objects.update_or_create(
                name=ledger['LEDGERNAME'],
                defaults={
                    'opening_balance': ledger.get('OPENINGBALANCE', 0),
                    'closing_balance': ledger.get('CLOSINGBALANCE', 0)
                }
            )
    
    return render(request, 'tally/import_success.html')
def sanitize_xml(xml_str):
    """
    Replaces problematic characters in the XML response.
    """
    # Replace any invalid characters like '&', '<', etc.
    xml_str = re.sub(r'&(?!amp;|lt;|gt;|apos;|quot;)', '&amp;', xml_str)  # Replace '&' not followed by valid entity
    return xml_str

def save_ledger_data(response_content):
    """
    Save the parsed ledger data into the Ledger model.
    """
    # Parse the JSON response (assuming response_content is JSON)
    data = response_content.get("tally_data", [])

    # Iterate over the ledger data and save it into the database
    for ledger in data:
        name = ledger.get("name")
        closing_balance = ledger.get("closing_balance")
        
        # If you also have opening balance in response, fetch it like this:
        opening_balance = ledger.get("opening_balance", 0)  # Default to 0 if not present

        # Create or update the Ledger instance
        Ledger.objects.update_or_create(
            name=name,
            defaults={
                'opening_balance': opening_balance or 0,  # Save 0 if not provided
                'closing_balance': closing_balance or 0   # Save 0 if not provided
            }
        )
