from django.shortcuts import render,redirect
import requests
from .models import Ledger
from django.http import JsonResponse,HttpResponse
import xml.etree.ElementTree as ET
import re
import json
import csv
import struct  # For creating binary-like formats
# Create your views here.
TALLY_URL = 'http://localhost:9000'




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
                        <SVCURRENTCOMPANY>Yhn</SVCURRENTCOMPANY><!-- Ensure correct company name -->
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

def import_successfull(request):
    return render(request,'tally/import_success.html')

def download_ledger_backup(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ledger_backup.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['Name', 'Parent', 'Opening Balance', 'Closing Balance'])

    # Write data rows
    ledgers = Ledger.objects.all()
    for ledger in ledgers:
        writer.writerow([ledger.name, ledger.parent, ledger.opening_balance, ledger.closing_balance])

    return response

def generate_custom_backup(request):
    # Define the binary or custom data you want to write to the file
    data = b"TAPE  \x03 \x8C\x0E\x01                                    \x02 \x87\x05\x8A\x1C\x1B\x81\x05   \x01   \x01\x03             , ^  \x04\x12\x1F\x98\xC9)Z\x01M i c r o s o f t   S Q L   S e r v e r       RAID                ;\x05\x9A\xB2\x1CBr\xA6\xD6\xE4\x4C\xA9\xCE5L\x8D\x16\xFFI\xAD  \xF0\x01\x01\x01     \x01   SPAD    &\x03          4\x17..."

    # Create the HttpResponse object with the appropriate headers
    response = HttpResponse(content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="custom_backup.bak"'

    # Write the binary data to the response
    response.write(data)

    return response