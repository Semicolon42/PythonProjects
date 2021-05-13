import requests

class SpaceTraderClient():
    def __init__(self, username=None, token=None):
        self.token = token
        self.username = username

    def base_url(self):
        return 'https://api.spacetraders.io'
    def scriptHostName(self):
        return 'BrendanScript'

    def makeRequest(self, http_method, path, headers=None, params=None):
        url = self.base_url() + path

        if headers == None:
            headers = {'User-Agent': f'{self.scriptHostName()}'}
        else:
            headers['User-Agent'] = f'{self.scriptHostName()}'

        if params == None:
            params = {'token': self.token}
        else:
            params['token'] = self.token

        try:
            if http_method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif http_method == 'POST':
                response = requests.post(url, headers=headers, params=params)
            response.raise_for_status()

            print(f'{response.status_code} {http_method} {url}')  
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"REQUEST FAILED: {response.status_code} {http_method} {url}", e)
        except requests.exceptions.Timeout as e:
            print(f"REQUEST FAILED: {response.status_code} {http_method} {url}", e)
        except:
            print(f"REQUEST FAILED: {response.status_code} {http_method} {url}")
        
        return None

    def getUserInfo(self):
        http_method = 'GET'
        path = '/users/' + self.username
        return self.makeRequest(http_method=http_method, path=path)

    def getLocationsInSystem(self, system):
        http_method = 'GET'
        path = f'/game/systems/{system}/locations'
        return self.makeRequest(http_method=http_method, path=path)

    def getSystems(self):
        http_method = 'GET'
        path = '/game/systems/'
        return self.makeRequest(http_method=http_method, path=path)

