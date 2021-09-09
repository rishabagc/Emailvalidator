from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
import csv
from io import TextIOWrapper
import requests



class DashBoardView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/dashboard/single_validator/")

def check_email_validate(email):
    response = requests.get("https://isitarealemail.com/api/email/validate",params = {'email': email})
    return True if response.json()['status'] == 'valid' else False

class SinglemailValidator(View):
    def get(self, request, *args, **kwargs):
        return render(request, "validator_app/single_mail_validator.html")

    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        status = check_email_validate(email)
        messages.success(request, "Your email is valid") if status else messages.error(request,"Your email is invalid")
        return HttpResponseRedirect("/dashboard/single_validator/")

class BulkmailValidator(View):
    def get(self, request, *args, **kwargs):
        return render(request, "validator_app/bulk_mail_validator.html")

    def post(self, request, *args, **kwargs):
        file_data = TextIOWrapper(request.FILES['csv_data'].file, encoding=request.encoding)
        reader = csv.reader(file_data)
        validate_emails = []
        fieldnames = ["email", "validate"]

        for row in reader:
            if row[0].lower() == 'email':
                continue

            status = check_email_validate(row[0])
            validate_emails.append({'email':row[0],'validate': status})

        with open("temp.csv", "w", encoding="UTF8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(validate_emails)

        with open('temp.csv') as csv_data:
            response = HttpResponse(csv_data, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=validate_emails.csv'

        os.remove("temp.csv")
        return response

class DownloadCSV(View):
    def get(self, request, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "sample.csv")
        if os.path.exists(file_path):
            fs = FileSystemStorage(file_path)
            with fs.open(file_path) as csv:
                response = HttpResponse(csv, content_type="application/csv")
                response["Content-Disposition"] = 'attachment; filename= "{}"'.format(
                    "sample.csv"
                )
                return response
        else:
            return 'Not Found'
