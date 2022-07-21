import requests
import json
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

winnerCount = 0

def saveWallet(wallet):
    with open(__location__+"/winners.txt", "a") as f:
        f.write(wallet+"\n")
        print("Saved wallet: "+str(wallet))
        f.close()

def checkWallet(wallet):
    global winnerCount
    response = requests.get("https://mint.tajigen.xyz/api/verify?account="+str(wallet))
    if response.status_code == 200:
        responseJson = json.loads(response.content)
        saleId = responseJson['saleId']
        if str(saleId) == "3":
            winnerCount += 1
            print("Found waitlisted Wallet: "+str(wallet))
            wallet = wallet+" - 2022/07/22 8:00 pm UTC"
            saveWallet(wallet)
        elif str(saleId) == "2":
            winnerCount += 1
            print("Found mintlisted Wallet: "+str(wallet))
            wallet = wallet+" - 2022/07/22 4:00 pm UTC"
            saveWallet(wallet) 
        elif str(saleId) == "1":
            winnerCount += 1
            print("Found shelterpass Wallet: "+str(wallet))
            wallet = wallet+" - 2022/07/22 4:00 pm UTC"
            saveWallet(wallet) 
        else:
            pass
    elif response.status_code == 204:
        print("Wallet: "+str(wallet)+" not WL: "+str(response.status_code))
    else:
        print("Error checking wallet: "+str(response.status_code))

with open(__location__+"/wallets.txt", "r") as f:
    walletLines = f.readlines()
    walletCount = len(walletLines)
    print("Checking "+str(walletCount)+" wallets..")
    for wallet in walletLines:
        wallet = wallet.strip("\n")
        try:
            checkWallet(str(wallet))
        except Exception as e:
            print("Error checking wallet: "+str(e))
    print(str(winnerCount)+"/"+str(walletCount)+" Wallets Whitelisted.")