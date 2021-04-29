import requests

class BaseApi:
    def base_url():
        return 'https://api.spacetraders.io'
    def scriptHostName():
        return 'BrendanScript'

class ApiAccount:
    def getAccount(username, token):
        url = BaseApi.base_url() + '/users/' + username
        headers = {'User-Agent': f'{BaseApi.scriptHostName()}'}
        params = {'token': token}
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f'GET {url} {response.status_code}')  
            return response.json()
        except e:
            print('failed to get account info for ', username, e)
        
        return None
    
    def createAccount(username):
        url = f'{BaseApi.base_url()}/users/{username}/token'
        headers = {'User-Agent': f'{BaseApi.scriptHostName()}'}
        try:
            response = requests.post(url, headers=headers)
            print(f'POST {url} {response.status_code}')
            return response.json()
        except e:
            print('failed to get account info for ', username, e)
        
        return None
    
    def getAvailableLoans(token):
        url = f'{BaseApi.base_url()}/game/loans'
        headers = {'User-Agent': f'{BaseApi.scriptHostName()}'}
        params = {'token': token}
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f'GET {url} {response.status_code}')
            return response.json()['loans']
        except e:
            print('failed to get account info for ', username, e)
        
        return None

    def acquireLoan(username, token, loanType):
        url = f'{BaseApi.base_url()}/users/{username}/loans'
        headers = {'User-Agent': f'{BaseApi.scriptHostName()}'}
        params = {'token': token, 'type': loanType}
        try:
            response = requests.post(url, headers=headers, params=params)
            print(f'GET {url} {response.status_code}')
            return response.json()
        except e:
            print('failed to get account info for ', username, e)
        
        return None