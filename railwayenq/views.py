import json
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime
class HomePage(TemplateView):
    template_name = 'index.html'


api_key = "rqjexumspi"
base_url = "https://api.railwayapi.com/v2/"

def result(request, train_number):
    try:
        headers = {}
        type = request.GET.get('type')
        date_format = request.GET.get('date')
        print(type)
        if type == 'train-status':
            url = base_url+"live/train/"+train_number+"/date/"+date_format+"/apikey/"+api_key
            print(url)
            response = requests.request("GET", url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                response_data = {}
                response_data['train_name'] = data['train']['name']
                response_data['train_number'] = data['train']['number']
                response_data['start_date'] = data['start_date']
                response_data['current_station'] = data['current_station']['name']
                response_data['position'] = data['position']

                if response_data['position'] == None:
                    error_data = { "msg": "Unable to get train position"}
                    return HttpResponse(json.dumps(error_data), content_type="application/json", status=400)
                else:
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                error_data = { "msg": "Unable to get train position"}
                return HttpResponse(json.dumps(error_data), content_type="application/json", status=400)

           
        else:
            src = request.GET.get('src')
            dest = request.GET.get('dest')

            url = base_url+"check-seat/train/"+train_number+"/source/"+src+"/dest/"+dest+"/date/"+date_format+"/perf/SL/quota/GN"+"/apikey/"+api_key
            print(url)
            response = requests.request("GET", url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                dummy_data = '{"response_code":200,"train":{"name":"NDLS SHATABDI E","number":"12001"},"from_station":{"lat":23.2599333,"name":"BHOPAL  JN","lng":77.412615,"code":"BPL"},"to_station":{"lat":30.6016778,"name":"NEW DELHI","lng":-98.3488272,"code":"NDLS"},"journey_class":{"name":"AC CHAIR CAR","code":"CC"},"quota":{"name":"GENERAL QUOTA","code":"GN"},"availability":[{"date":"14-07-2017","status":"AVAILABLE 364"},{"date":"15-07-2017","status":"AVAILABLE 361"},{"date":"16-07-2017","status":"AVAILABLE 284"},{"date":"17-07-2017","status":"AVAILABLE 351"},{"date":"18-07-2017","status":"AVAILABLE 303"},{"date":"19-07-2017","status":"AVAILABLE 329"}]}'
                data = json.loads(dummy_data)
             
                if data['availability'] == None or (not data['availability']):
                    error_data = { "msg": "Unable to get seat availability data"}
                    return HttpResponse(json.dumps(error_data), content_type="application/json", status=400)
                else:
                    response_data = {}
                    response_data['train_name'] = data['train']['name']
                    response_data['train_number'] = data['train']['number']
                    response_data['from_station'] = data['from_station']['name'] + " (" + data['from_station']['code'] +")"
                    response_data['to_station'] = data['to_station']['name'] + " (" + data['to_station']['code'] +")"
                    response_data['journey_class'] = data['journey_class']['name'] + " (" + data['journey_class']['code'] +")"
                    response_data['quota'] = data['quota']['name'] + " (" + data['quota']['code'] +")"

                    for availability in data['availability']:
                        response_data[availability['date']] = availability['status']
                    return HttpResponse(json.dumps(response_data), content_type="application/json")

            elif response.status_code == 404: # remove if api is working
                dummy_data = '{"response_code":200,"train":{"name":"NDLS SHATABDI E","number":"12001"},"from_station":{"lat":23.2599333,"name":"BHOPAL  JN","lng":77.412615,"code":"BPL"},"to_station":{"lat":30.6016778,"name":"NEW DELHI","lng":-98.3488272,"code":"NDLS"},"journey_class":{"name":"AC CHAIR CAR","code":"CC"},"quota":{"name":"GENERAL QUOTA","code":"GN"},"availability":[{"date":"14-07-2017","status":"AVAILABLE 364"},{"date":"15-07-2017","status":"AVAILABLE 361"},{"date":"16-07-2017","status":"AVAILABLE 284"},{"date":"17-07-2017","status":"AVAILABLE 351"},{"date":"18-07-2017","status":"AVAILABLE 303"},{"date":"19-07-2017","status":"AVAILABLE 329"}]}'
                data = json.loads(dummy_data)
                response_data = {}
                response_data['train_name'] = data['train']['name']
                response_data['train_number'] = data['train']['number']
                response_data['from_station'] = data['from_station']['name'] + " (" + data['from_station']['code'] +")"
                response_data['to_station'] = data['to_station']['name'] + " (" + data['to_station']['code'] +")"
                response_data['journey_class'] = data['journey_class']['name'] + " (" + data['journey_class']['code'] +")"
                response_data['quota'] = data['quota']['name'] + " (" + data['quota']['code'] +")"

                for availability in data['availability']:
                    response_data[availability['date']] = availability['status']
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                error_data = { "msg": "Unable to get seat availability data"}
                return HttpResponse(json.dumps(error_data), content_type="application/json", status=400)

            return HttpResponse("{}", content_type="application/json")
    
    except Exception as e:
        error_data = { "msg": str(e)}
        return HttpResponse(json.dumps(error_data), status=400)
