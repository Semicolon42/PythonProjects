import os
import json
import time
from BrendanSpaceTraderApi import AccountApi as STAccountApi

class SpaceCorpActions():
    def current_milli_time():
        return round(time.time() * 1000)

    def getCompanyFilename(companyName):
        return f"./companyTokens/{companyName}.json"

    def saveCompanyFile(companyConfig):
        filename = SpaceCorpActions.getCompanyFilename(companyConfig['name'])
        companyConfig['timestamp_modified'] = SpaceCorpActions.current_milli_time()
        with open(filename, 'w') as outfile:
            json.dump(companyConfig, outfile, indent=4)
        print(f"Saved corp file {filename}")

    def initCompanyFile(companyName):
        response = STAccountApi.createAccount(companyName)
        print(f"{response['user']['username']} {response['token']}")

        now = SpaceCorpActions.current_milli_time()
        companyConfig = dict()
        companyConfig['name'] = f'{companyName}'
        companyConfig['token'] = response['token']
        companyConfig['timestamp_created'] = now
        companyConfig['timestamp_modified'] = now
        companyConfig['ships'] = dict()

        response2 = STAccountApi.getAccount(response['user']['username'], response['token'])
        companyConfig['stats'] = response2['user']
        SpaceCorpActions.saveCompanyFile(companyConfig)
        return companyConfig

    def loadCompanyFile(companyName):
        filename = SpaceCorpActions.getCompanyFilename(companyName)
        companyConfig = None
        if (os.path.exists(filename)):
            print(f"Company config exists: {filename}")
            with open(filename) as configFile:
                companyConfig = json.load(configFile)
        else:
            print(f"Company config DOES NOT exist: {filename}")
        return companyConfig
    
    def refreshCompanyFile(companyName, companyToken):
        print(f"Operation Refresh Company {companyName}")
        companyConfig = SpaceCorpActions.loadCompanyFile(companyName)
        if companyConfig == None:
            print(f"No company file for {companyName}")
            return None

        response = STAccountApi.getAccount(companyName, companyToken)
        if response is not None:
            companyConfig['stats'] = response['user']
            for ship in response['user']['ships']:
                companyConfig['ships'][ship['id']] = dict()
                companyConfig['ships'][ship['id']]['stats'] = ship

        SpaceCorpActions.saveCompanyFile(companyConfig)
        print(f"Company Refreshed {companyConfig['name']}")
        return companyConfig
