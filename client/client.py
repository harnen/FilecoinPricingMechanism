from web3 import Web3

class Client:
    def __init__(self, account, provider, address, abi):
        self.account = account
        self.web3 = Web3(provider)
        self.contract = self.web3.eth.contract(address=address, abi=abi)

    def check_connection(self):
        return self.web3.isConnected()

    def submit_bid(self, size, duration, price):
        transaction = self.contract.functions.submitBid(size, duration, price)
        tx_hash = transaction.transact({'from': self.account})
        return web3.eth.waitForTransactionReceipt(tx_hash)
