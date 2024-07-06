import requests

class UserApiService:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_user(self, user_id, username):
        url = self.base_url + '/create_user'
        body = { "user_id": user_id, "username": username }
        res = requests.post(url, body, timeout=15)
        return { "status_code": res.status_code }

        
