import sys
import threading
import logging
from time import sleep

from RepeatedTimerThread import RepeatedTimerThread
from SpaceCorpActions import SpaceCorpActions as SCA
from BrendanSpaceTraderApi import AccountApi as STAccountApi
from BrendanSpaceTraderApi import ShipyardApi as STShipyardApi


class SpaceCorpManagementCycler():

    def corpRefresh(self):
        tempCorp = SCA.refreshCompanyFile(self.corp['name'], self.corp['token'])
        if tempCorp != None:
            self.corp = tempCorp

    def corpRefreshFromResponse(self, resp):
        if resp == None:
            return
        if 'credits' in resp: 
            self.corp['stats']['credits'] = resp['credits']

    def getAllAvailableLoans(self):
        print('Getting available loans')
        loans = STAccountApi.getAvailableLoans(self.corp['token'])
        for loan in loans:
            print(f"getting loan for {loan['type']}")
            resp = STAccountApi.acquireLoan(self.corp['name'], self.corp['token'], loan['type'])
            # Update the corp model from the response
            self.corpRefreshFromResponse(resp)

    def __init__(self, companyName):
        self.corp = SCA.loadCompanyFile(companyName)
        if self.corp == None:
            self.corp = SCA.initCompanyFile(companyName)
            ## Get all available loans
            self.getAllAvailableLoans()
        else:
            self.corpRefresh()

    def checkBuyAnotherShip(self):
        if self.corp['stats']['credits'] < 200000:
            return 

        availableShips = STShipyardApi.getAvailableShips(self.corp['token'])
        if availableShips != None: 
            ship = availableShips['ships'][0]
            if self.corp['stats']['credits'] > ship['purchaseLocations'][0]['price']:
                resp = STShipyardApi.postPurchaseShip(self.corp['name'], self.corp['token'], ship['purchaseLocations'][0]['location'], ship['type'])
                # Update the corp model from the response
                self.corpRefreshFromResponse(resp)
                self.corp['ships'][resp['ship']['id']] = dict()
                self.corp['ships'][resp['ship']['id']]['stats'] = resp['ship']

    def manageShips(self):
        for id, ship in self.corp['ships'].items():
            print("SHIP ----------------")
            print(f"--Managing ship id:{id} location:{ship['stats']['location']} cargo:{ship['stats']['cargo']}")
            print("SHIP ----------------")


    def CorpCycle(self):
        print("CYCLE ===================================")
        ## Check if this is first cycle as this corp.  If so, initialize the corp
        print(f"{self.corp['name']} credits: {self.corp['stats']['credits']}")
        
        ## Check if current funds are enough to purchase another ship
        self.checkBuyAnotherShip()
        ## Manage each individual ship
        self.manageShips()
        ## Check for eccess funds for paying off loans
        ## End cycle
        print("CYCLE ===================================")

    def start(self):
        companyName = self.corp['name']
        rt = RepeatedTimerThread(3, self.CorpCycle)
        print(f"Starting Cycles for {companyName}")
        rt.start()
        try:
            sleep(10) # your long-running job goes here...
        finally:
            print("stoping...")
            rt.stop() # better in a try/finally block to make sure the program ends!
        print(f"Finished all cycles for {companyName}")

def main():
    companyName = sys.argv[1] if len(sys.argv) > 1 else "temp"
    print(f"Loading Company {companyName}")    
    corporation = SpaceCorpManagementCycler(companyName)
    print(f"Loaded Company {corporation.corp['name']}")
    corporation.start()

if __name__ == '__main__':
    main()
    