from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .essearch import SearchElasticSearch
import json
from . import exceptions
from . import helpers
# Create your views here.

def id_match(name):
    return name+"-id"

@api_view(['GET'])
@permission_classes((IsAuthenticated, ) )
def get_user_id(request, id):
    data = {'user-id': id}
    res, status_code = helpers.handle_response(request, data)
    return Response(res, status = status_code)
    
@api_view(['GET'])
@permission_classes((IsAuthenticated, ) )
def get_event_id(request, param1, eid):
    # id_name=id_match(param1)
    data = {
                'event_name': ".".join(["event", param1]),
                id_name: eid
            }
    res, status_code = helpers.handle_response(request, data)
    return Response(res, status = status_code)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ) )
def get_user_id_event_id(request, id, param1, eid):
    # id_name=id_match(param1)
    data = {
            'user-id': id,
            "event_name": ".".join(["event", param1]),
            id_name: eid
           }
    res, status_code = helpers.handle_response(request, data)
    return Response(res, status = status_code)
