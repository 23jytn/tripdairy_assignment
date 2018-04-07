import json
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime
class HomePage(TemplateView):
    template_name = 'index.html'


def result(request, train_number):
    try:
        if len(str(train_number)) != 5:
            return HttpResponse("Train Number is in-valid.", status=400)
        else:
            api_key = "rqjexumspi"
            headers = {}
            today = datetime.date.today()
            date_format = today.strftime("%d-%m-%Y")

            url = "https://api.railwayapi.com/v2/live/train/"+str(train_number)+"/date/"+date_format+"/apikey/"+api_key
            print(url)
            response = requests.request("GET", url, headers=headers)

            data = response.json()

            response_data = {}
            response_data['name'] = data['train']['name']
            response_data['number'] = data['train']['number']
            response_data['position'] = data['position']
            response_data['start_date'] = data['start_date']
            response_data['current_station'] = data['current_station']['name']
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        return HttpResponse("Exception occurred in finding Train Number." + str(e), status=400)
