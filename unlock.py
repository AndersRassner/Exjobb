from web3 import Web3, KeepAliveRPCProvider, IPCProvider

web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
iteration = 0
# Unlock accounts using super secret password
for x in web3.personal.listAccounts:
    web3.personal.unlockAccount(x, 'traffic', 0)
    iteration += 1
    if iteration % 50 == 0:
        print str(iteration) + " accounts out of 3000 unlocked..."
