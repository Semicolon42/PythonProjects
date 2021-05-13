import sys
import threading
from SpaceTraderClient import SpaceTraderClient

def main():
    st_client = SpaceTraderClient('Semicolon42a', '1791656b-d9e4-4e99-90ae-a0b6c6fad301')

    print('Hello World')
    user = st_client.getUserInfo()
    print(user)
    systems=st_client.getSystems()
    for system in systems['systems']:
        print(system['symbol'])
        response = st_client.getLocationsInSystem(system['symbol'])
        for location in response['locations']:
            print(f"- {location['symbol']} \t:: ({location['x']},{location['y']}) \t:: {location['name']}")

if __name__ == '__main__':
    main()