import requests

class BaseApi:
    def base_url():
        return 'https://api.spacetraders.io'

class ApiAccount:
    def getAccount(username, token):
        url = BaseApi.base_url() + '/users/' + username
        headers = {'User-Agent': 'Mozilla/5.0'}
        params = {'token': token}
        try:
            response = requests.get(url, headers=headers, params=params)
            print(response.headers)
            return response.json()
        except e:
            print('failed to get account info for ', username, e)
        
        return None