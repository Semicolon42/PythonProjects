import BrendanSpaceTraderApi as STApi
import os
import configparser

def workingFilepath(fpath):
    return os.path.dirname(__file__) + "/" + fpath

def configGetUserToken():
    config = configparser.ConfigParser()
    config.sections()

    print(workingFilepath('token.ini'))
    config.read(workingFilepath('token.ini'))
    print(config)
    print(config.sections())
    
    username = config['default']['username']
    token = config['default']['token']
    return (username, token)

def main():
    print('hello world')
    username, token = configGetUserToken()
    print(str(token))

    account = STApi.ApiAccount.getAccount('semicolon42', token)
    if account == None:
        print('no account info')
    else:
        print(account)

    


if __name__ == "__main__":
    # execute only if run as a script
    main()

