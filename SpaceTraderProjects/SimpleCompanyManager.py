from BrendanSpaceTraderApi import AccountApi as STAccountApi
import os
import json
import sys
import time
from enum import Enum

def current_milli_time():
    return round(time.time() * 1000)

def saveCompanyStateLocally(companyConfig):
    filename = f"./companyTokens/{companyName}.json"
    with open(filename, 'w') as outfile:
        json.dump(companyConfig, outfile)

def operationSetSate(companyConfig, targetState):
    print("state comparison: ", targetState, "NOOP", "GET_LOANS")
    if targetState == "NOOP":
        companyConfig['management']['state'] = "NOOP"
    if targetState == "GET_LOANS":
        companyConfig['management']['state'] = "GET_LOANS"
    saveCompanyStateLocally(companyConfig)

def operationRefresh(companyConfig):
    print(f"Operation Refresh Company {companyConfig['company']['name']}")
    response = STAccountApi.getAccount(companyConfig['company']['name'], companyConfig['company']['token'])
    response = response['user']
    print(f"Company Details Retrieved {companyConfig['company']['name']} {response}")
    if 'credits' in response:
        print('credits')
        companyConfig['company']['credits'] = response['credits']
    if 'loans' in response:
        print('loans')
        companyConfig['company']['loans'] = response['loans']
    if 'ships' in response:
        print('ships')
        companyConfig['company']['ships'] = response['ships']

    if 'state' not in companyConfig['company']:
        companyConfig['management']['state'] = "NOOP"
        saveCompanyStateLocally(companyConfig)

    saveCompanyStateLocally(companyConfig)
    print(f"Company Refreshed {companyConfig['company']['name']}")
    
def getAllAvailableLoans(companyConfig):
    loans = STAccountApi.getAvailableLoans(companyConfig['company']['token'])
    print('loans:', loans)
    for loan in loans:
        print('loan:', loan)
        STAccountApi.acquireLoan(companyConfig['company']['name'], companyConfig['company']['token'], loan['type'])
    companyConfig['management']['state'] = "BUY_SHIP"
    operationRefresh(companyConfig)

def operationManage(companyConfig):
    print("Operation Manage")
    if 'state' not in companyConfig['company']:
        companyConfig['management']['state'] == "NOOP"
        saveCompanyStateLocally(companyConfig)

    state = companyConfig['management']['state']
    if state == "NOOP":
        print('NOOP: Doing nothing')
    elif state == "GET_LOANS":
        getAllAvailableLoans(companyConfig)
    else:
        print(f"Unknown State: {state}")
        
def operationinfo(companyConfig):
    print(companyConfig)

def loadCompanyConfigFile(companyName):
    filename = f"./companyTokens/{companyName}.json"
    comapnyConfig = None
    if (os.path.exists(filename)):
        print(f"Company config exists: {filename}")
        with open(filename) as configFile:
            comapnyConfig = json.load(configFile)
    else:
        print(f"Company config DOES NOT exist: {filename}")
        response = STAccountApi.createAccount(companyName)
        print(f"{response['user']['username']} {response['token']}")

        now = current_milli_time()
        companyConfig = dict()
        companyConfig['company'] = dict()
        companyConfig['company']['name'] = f'{companyName}'
        companyConfig['company']['token'] = response['token']
        companyConfig['company']['timestamp_created'] = now
        companyConfig['company']['timestamp_modified'] = now
        companyConfig['management'] = dict()
        companyConfig['management']['state'] = "GET_LOANS"
        companyConfig['management']['timestamp_modified'] = now
        with open(filename, 'w') as outfile:
            json.dump(companyConfig, outfile)

        print(f"Does the company config file exist now? {os.path.exists(filename)}")

    return comapnyConfig

def main(companyName, operation):
    print("state comparison: ", "NOOP", "GET_LOANS")
    print("companyName:", companyName)
    companyConfig = loadCompanyConfigFile(companyName)
    
    print("//operations")
    if operation == "refresh":
        operationRefresh(companyConfig)
    elif operation == "manage":
        operationManage(companyConfig)
    elif operation == "info":
        operationinfo(companyConfig)
    elif operation == "set-state":
        operationSetSate(companyConfig, targetState, sys.argv[3])

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    print('---- MAIN START ----')
    main(sys.argv[1], sys.argv[2])
    print('---- MAIN FINISHED ----')
    