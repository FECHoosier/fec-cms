
from django import template
import requests
from django.conf import settings
from django.conf import os
import dateutil.parser

register = template.Library()

@register.inclusion_tag('partials/jobs.html')
def get_jobs():
    url = "https://data.usajobs.gov/api/Search"

    querystring = {"Organization":"LF00","WhoMayApply":"All"}
    headers = {
        'authorization-key': settings.USAJOBS_API_KEY,  
        'user-agent': "jcarroll@fec.gov",
        'host': "data.usajobs.gov",
        'cache-control': "no-cache",
        }
    
    response = requests.request("GET", url, headers=headers, params=querystring)

    responses=response.json()    

    jobData = []
    for i in responses['SearchResult']['SearchResultItems']:
        x= {}
        x = { 
        "position_title": i["MatchedObjectDescriptor"]["PositionTitle"] , 
        "position_id": i["MatchedObjectDescriptor"]["PositionID"], 
        "position_uri": i ["MatchedObjectDescriptor"]["PositionURI"],
        "position_start_date" : dateutil.parser.parse(i['MatchedObjectDescriptor']['PositionStartDate']),
        "position_end_date" : dateutil.parser.parse(i['MatchedObjectDescriptor']['PositionEndDate']),
        "who_may_apply" : i['MatchedObjectDescriptor']['UserArea']['Details']['WhoMayApply']['Name'],
        "job_grade" : i['MatchedObjectDescriptor']['JobGrade'][0]['Code'],
        "low_grade" : i['MatchedObjectDescriptor']['UserArea']['Details']['LowGrade'],
        "high_grade" : i['MatchedObjectDescriptor']['UserArea']['Details']['HighGrade'] }
        jobData.append(x)

    return ({'jobData':jobData})


