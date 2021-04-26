import BrendanSpaceTraderApi.ApiAccount as ApiAccount
import os

def main():
    print('hello world')
    token = ''
    workingDirectory = os.path.dirname(__file__)
    with open(workingDirectory + '/token') as f:
        try:
            token = f.read().splitlines()[0]
        except e:
            print('failed to get token', e)
    print(str(token))

    account = ApiAccount.getAccount('semicolon42', token)
    if account == None:
        print('no account info')
    else:
        print(account)

    


if __name__ == "__main__":
    # execute only if run as a script
    main()

