import requests
import json

class EventApiService:
    def __init__(self, base_url):
        self.base_url = base_url 
    
    def add_event(self, user_id, event_name, event_date):
        url = self.base_url + "add_event"
        body = { "user_id": user_id, "event_name": event_name, "event_date": event_date }
        res = requests.patch(url, body)
        return { "error": False }   
    
    def get_user_events_day(self, user_id, event_date):
        url = self.base_url + user_id + '/day/' + event_date
        res = requests.get(url)
        return { "error": False, "data": res.json }  
    
    def get_user_events_month(self, user_id, event_date):
        url = self.base_url + user_id + '/month/' + event_date
        res = requests.get(url)
        return { "error": False, "data": res.json }   
    
    def delete_event(self, event_id):
        url = self.base_url + "delete_event"
        body = { "event_id": event_id }
        res = requests.patch(url, body)
        return { "error": False }   
    

                   