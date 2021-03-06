import requests

class BaseApi:
    def base_url():
        return 'https://api.spacetraders.io'
    def scriptHostName():
        return 'BrendanScript'

class AccountApi:
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

class ShipyardApi:
    def getAvailableShips(token):
        url = BaseApi.base_url() + '/game/ships'
        headers = {'User-Agent': f'{BaseApi.scriptHostName()}'}
        params = {'token': token}
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f'GET {url} {response.status_code}')  
            return response.json()
        except e:
            print('failed to get available ships', e)
        
        return None
    
    def postPurchaseShip(username, token, location, shipType):
        url = f'{BaseApi.base_url()}/users/{username}/ships'
        headers = {'User-Agent': f'{BaseApi.scriptHostName()}'}
        params = {'token': token, 'location': location, 'type': shipType}
        try:
            response = requests.post(url, headers=headers, params=params)
            print(f'POST {url} {response.status_code}')
            return response.json()
        except e:
            print(f'failed to purchase ship info for username={username} location={location} type={type}', e)
        
        return None


class MarketApi:
    def getAvailableGoods(token, location):
        url = BaseApi.base_url() + f'/game/locations/{location}/marketplace'
        headers = {'User-Agent': f'{BaseApi.scriptHostName()}'}
        params = {'token': token}
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f'GET {url} {response.status_code}')  
            return response.json()
        except e:
            print(f'failed to get available goods for location={location}', e)
        
        return None


class SystemsApi:
    def getLocationsInSystem(token, system):
        url = BaseApi.base_url() + f'/game/systems/{system}/locations'
        headers = {'User-Agent': f'{BaseApi.scriptHostName()}'}
        params = {'token': token}
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f'GET {url} {response.status_code}')  
            return response.json()
        except e:
            print(f'failed to get locations for system={system}', e)
        
        return None

class ManageShipApi:

    def postPurchaseGood(username, token, shipId, good, quantity):
        url = f'{BaseApi.base_url()}/users/{username}/purchase-orders'
        headers = {'User-Agent': f'{BaseApi.scriptHostName()}'}
        params = {'token': token, 'shipId': shipId, 'good': good, 'quantity': quantity}
        try:
            response = requests.post(url, headers=headers, params=params)
            print(f'POST {url} {response.status_code}')
            return response.json()
        except e:
            print(f'failed to purchase goods for username={username} shipid={location} good={type} quantity={quantity}', e)
        
        return None

    def postSellGoodsFromShip():
        url = f'{BaseApi.base_url()}/users/{username}/sell-orders'
        headers = {'User-Agent': f'{BaseApi.scriptHostName()}'}
        params = {'token': token, 'shipId': shipId, 'good': good, 'quantity': quantity}
        try:
            response = requests.post(url, headers=headers, params=params)
            print(f'POST {url} {response.status_code}')
            return response.json()
        except e:
            print(f'failed to sell goods for username={username} shipid={location} good={type} quantity={quantity}', e)
        
        return None

    def getShipFlightPlan(username, token, flightPlanId):
        url = BaseApi.base_url() + f'/users/{username}/flight-plans/{flightPlanId}'
        headers = {'User-Agent': f'{BaseApi.scriptHostName()}'}
        params = {'token': token}
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f'GET {url} {response.status_code}')  
            return response.json()
        except e:
            print(f'failed to get flight plan for username={username} flightPlanId={flightPlanId}', e)
        
        return None

    def postUpdateFlightPlan(username, token, shipId, destination):
        url = f'{BaseApi.base_url()}/users/{username}/ships'
        headers = {'User-Agent': f'{BaseApi.scriptHostName()}'}
        params = {'token': token, 'destination': destination}
        try:
            response = requests.post(url, headers=headers, params=params)
            print(f'POST {url} {response.status_code}')
            return response.json()
        except e:
            print(f'failed to purchase goods for username={username} shipid={location} good={type} quantity={quantity}', e)
        
        return None