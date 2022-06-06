from web3 import Web3
import json
import Constants as keys
from datetime import datetime, timezone
from utils.timesince import timesince, timeuntil
import pytz

bsc1 = "https://bsc-dataseed.binance.org/"
bsc2 = "https://bsc-dataseed1.defibit.io/"
bsc3 = "https://bsc-dataseed1.ninicoin.io/"
w3 = Web3(Web3.HTTPProvider(bsc2))

contractAddr = "0xeba5ef26c655E25fcbA6778b1D755a8f67bC1387"

abijson = open('./las_abi.json')
contractAbi = json.load(abijson)

contractObject = w3.eth.contract(address=contractAddr, abi=contractAbi)

# totalSupply = contractObject.functions.totalSupply().call()
# name = contractObject.functions.name().call()


# # return bool
# tokenamount = 133
# isJackpotEligible = contractObject.functions.isJackpotEligible(tokenamount).call()
# # print(isJackpotEligible)


# # return (bnb, tokens)
# jackpotBuyerShareAmount = contractObject.functions.jackpotBuyerShareAmount().call()
# # print(jackpotBuyerShareAmount)


# # return (bnb, tokens)
# jackpotBuybackAmount = contractObject.functions.jackpotBuybackAmount().call()
# # print(jackpotBuybackAmount)




# bnbamount = 1
# usdEquivalent = contractObject.functions.usdEquivalent(bnbamount).call()
# print(usdEquivalent)

def guardPot():
    # return _pendingJackpotBalance, _jackpotTokens
    guardPot = contractObject.functions.getJackpot().call()

    guardPotBnb = w3.fromWei(guardPot[0], 'ether')
    guardPotUsd = guardPotBnb * contractObject.functions.usdEquivalent(1).call() 
    guardPotToken = w3.fromWei(guardPot[1], 'gwei')


    return (keys.TEXT_GUARDPOT.format(totalusd='{0:.2f}'.format(guardPotUsd), cashedbnb='{0:.2f}'.format(guardPotBnb), tokensout='{0:.2f}'.format(guardPotToken)))


def lastBigBang():
    # Return _lastBigBangCash, _lastBigBangTokens, _lastBigBangTimestamp
    lastbigbang = contractObject.functions.getLastBigBang().call()
    dt_object = datetime.fromtimestamp(lastbigbang[2], timezone.utc)
    bigbangdate = timesince(dt_object)
    
    bigbangBnb = w3.fromWei(lastbigbang[0], 'ether')
    bigbangUsd = bigbangBnb * contractObject.functions.usdEquivalent(1).call() 
    bigbangToken = w3.fromWei(lastbigbang[1], 'gwei')

    return (keys.TEXT_LASTBIGBANG.format(totalusd='{0:.2f}'.format(bigbangUsd), formateddate=bigbangdate, cashedbnb='{0:.2f}'.format(bigbangBnb), tokensout='{0:.2f}'.format(bigbangToken)))



def lastBuy():
    # Return _lastBuyer and _lastBuyTimestamp 
    lastbuy = contractObject.functions.getLastBuy().call()

    buyWallet = lastbuy[0]
    dt_object = datetime.fromtimestamp(lastbuy[1], timezone.utc)

    buydate = timesince(dt_object)

    return (keys.TEXT_LASTBUY.format(wallet=buyWallet, formateddate=buydate))




def pendingBalance():
    # Return  _pendingMarketingBalance,_pendingDevBalance, _pendingJackpotBalance
    # need to be autorized
    getPendingBalances = contractObject.functions.getPendingBalances().call()
    return getPendingBalances


def lastAwarded():

    # Return  _lastAwarded,_lastAwardedCash, _lastAwardedTokens, _lastAwardedTimestamp
    lastawarded = contractObject.functions.getLastAwarded().call()
    print(lastawarded)

    wonWallet = lastawarded[0]
    dt_object = datetime.fromtimestamp(lastawarded[3], timezone.utc)

    wondate = timesince(dt_object)

    wonbnb = w3.fromWei(lastawarded[1], 'ether')
    wonUsd = wonbnb * contractObject.functions.usdEquivalent(1).call() 
    tokensout = w3.fromWei(lastawarded[2], 'gwei')

    return (keys.TEXT_LASTWON.format(wallet=wonWallet, totalusd='{0:.2f}'.format(wonUsd), formateddate=wondate, cashedbnb='{0:.2f}'.format(wonbnb), tokensout='{0:.2f}'.format(tokensout)))


def guardTimer():
    # Return _lastBuyer, _lastBuyTimestamp
    lastBuy = contractObject.functions.getLastBuy().call()

    lastbuyWallet = lastBuy[0]
    lastbuytimestamp = lastBuy[1]
    dt_object = datetime.fromtimestamp((lastbuytimestamp + (10*60)) , timezone.utc)
    leftime = timeuntil(dt_object)
   
    guardPot = contractObject.functions.getJackpot().call()
    guardPotBnb = w3.fromWei(guardPot[0], 'ether')
    guardPotUsd = guardPotBnb * contractObject.functions.usdEquivalent(1).call() 
    guardPotToken = w3.fromWei(guardPot[1], 'gwei')

   
    return (keys.TEXT_GUARDPOT_TIMER.format(wallet=lastbuyWallet,formateddate=leftime, totalusd='{0:.2f}'.format(guardPotUsd), cashedbnb='{0:.2f}'.format(guardPotBnb), tokensout='{0:.2f}'.format(guardPotToken)))
    


# # collectDevFees
# # collectMarketingFees

# print("Project Name : "+name)
# # print(w3.fromWei(totalSupply, 'ether'))