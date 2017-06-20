from web3 import Web3, KeepAliveRPCProvider, IPCProvider
from time import sleep, time


web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
# Unlock accounts using super secret password
for x in web3.personal.listAccounts:
    web3.personal.unlockAccount(x, 'traffic', 0)


MyContract = web3.eth.contract([{"constant":True,"inputs":[],"name":"maxTraffic","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"priceRatio","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"getMaxPrice","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"currentPrice","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"newMaxTraffic","type":"uint256"}],"name":"setMaxTraffic","outputs":[],"payable":False,"type":"function"},{"constant":False,"inputs":[],"name":"buyPassage","outputs":[],"payable":True,"type":"function"},{"constant":True,"inputs":[],"name":"maxPrice","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"getCurrentPrice","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"newMaxPrice","type":"uint256"}],"name":"setMaxPrice","outputs":[],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"currentTraffic","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"inputs":[{"name":"initMaxTraffic","type":"uint256"},{"name":"initMaxPrice","type":"uint256"}],"payable":False,"type":"constructor"}]
)
MyContract.address = '0x1ce75c4d7a896ba4eb717c7e0f15ec9031ecbe72'

cur_price = MyContract.call().getCurrentPrice()
cur_max = MyContract.call().getMaxPrice()
estimatedGas = web3.eth.estimateGas({'to': MyContract.address, 'from': web3.eth.accounts[1], 'value': cur_price})
transaction_ = MyContract.transact({'from': web3.eth.accounts[1], 'value': estimatedGas+cur_price}).buyPassage()
#estimatedGas = web3.eth.estimateGas({'to': MyContract.address, 'from': web3.eth.accounts[2], 'value': cur_price})
#transaction2_ = MyContract.transact({'from': web3.eth.accounts[2], 'value': estimatedGas}).buyPassage()
while (web3.eth.getTransactionReceipt(transaction_) == None): #and web3.eth.getTransactionReceipt(transaction2_) == None):
	print "Sleeping for 10 seconds"
	sleep(10)

# DEBUG
print "Transaction: " + str(transaction_)
#print "Transaction: " + str(transaction2_)
print "Current price: " + str(cur_price)
print "Max price: " + str(cur_max)
