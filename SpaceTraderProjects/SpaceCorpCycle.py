import sys
import threading
import logging
from RepeatedTimerThread import RepeatedTimerThread
from SpaceCorpActions import SpaceCorpActions as SCA
from time import sleep

class SpaceCorpManagementCycle():

    def __init__(self, companyName):
        self.corp = SCA.loadCompanyFile(companyName)
        if self.corp == None:
            self.corp = SCA.initCompanyFile(companyName)
        else:
            print('Brendan1')
            tempCorp = SCA.refreshCompanyFile(companyName, self.corp['token'])
            print('Brendan2')
            self.corp = tempCorp

    def NewCorpFunction(self, companyName):
        self.corp = None
        ## Create and save the corp id and token
        ## Get the max funds

    def CorpCycle(self):
        ## Check if this is first cycle as this corp.  If so, initialize the corp
        print(f"{self.corp['name']} credits: {self.corp['stats']['credits']}")
        ## Check if current funds are enough to purchase another ship
        ## Manage each individual ship
        ## Check for eccess funds for paying off loans
        ## End cycle


def main(companyName):
    print(f"Loading Company {companyName}")
    corporation = SpaceCorpManagementCycle(companyName)
    print(f"Loaded Company {corporation.corp['name']}")
    
    rt = RepeatedTimerThread(2, corporation.CorpCycle)
    print(f"Starting Cycles for {companyName}")
    rt.start()
    try:
        sleep(10) # your long-running job goes here...
    finally:
        print("stoping...")
        rt.stop() # better in a try/finally block to make sure the program ends!
    print(f"Finished all cycles for {companyName}")


if __name__ == '__main__':
    companyName = sys.argv[1] if len(sys.argv) > 1 else "temp"
    main(companyName);