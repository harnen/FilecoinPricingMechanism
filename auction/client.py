from web3 import Web3
import argparse


class Client:
    def __init__(self, account, provider, address, abi_file):
        self.w3 = Web3(Web3.IPCProvider(provider))
        with open(abi_file) as f:
            abi = f.read()
        self.contract = self.w3.eth.contract(address=address, abi=abi)
        self.w3.eth.defaultAccount = self.w3.eth.accounts[0]
        self.unlockAccount()


    def check_connection(self):
        return self.w3.isConnected()

    def listAccounts(self):
        for account in self.w3.eth.accounts:
            print(account, self.w3.eth.getBalance(account))


    def submit_bid(self, size, duration, price, gas):
        transaction = self.contract.functions.submitBid(size, duration, price)
        tx_hash = transaction.transact({'from': self.account, 'gas': gas})
        return self.w3.eth.waitForTransactionReceipt(tx_hash)

    def bid(self):
        size = input("How much storage do you need?[GB]:")
        duration = input("What's the length of the lease?[days]:")
        price = input("How much are you willing to pay?[ETH]:")
        print("Submitting bid for", size, "GB of storage for", duration, "days")
        transaction = self.contract.functions.submitBid(int(size), int(duration), int(price))
        tx_hash = transaction.transact()
        return self.w3.eth.waitForTransactionReceipt(tx_hash)

    def unlockAccount(self):
        self.w3.geth.personal.unlockAccount(self.w3.eth.defaultAccount, 'password')

    def deployContract(self, abi_file, bin_file):
        with open(abi_file, 'r') as myfile:
            contract_abi = myfile.read()
            myfile.close()
        with open(bin_file, 'r') as myfile:
            contract_bin = myfile.read()
            myfile.close()

        #print("Accounts", self.listAccounts())
        contract = self.w3.eth.contract(abi=contract_abi, bytecode=contract_bin)
        tx_hash = contract.constructor().transact()
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print("Contract deployed at", tx_receipt.contractAddress)
        return tx_receipt.contractAddress

    def solve(self):
        bidsCounter = self.contract.functions.bidsCounter().call()
        print("Bids(", bidsCounter, ")" )
        for i in range(1, bidsCounter + 1):
            print("Bid:", self.contract.functions.bids(i).call())



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FilecoinPricingMechanism Client.')
    # Used for bid submittion
    parser.add_argument('--addr', default='', help='Contract address')
    parser.add_argument("command", choices=['list', 'deploy', 'bid', 'verify', 'solve'], help="Command to execute")
    parser.add_argument('--account', help='Self account', required=False)
    parser.add_argument(
        '--provider', default='../data/geth.ipc', help='ethereum IPC provider URL')
    parser.add_argument(
        '--abi', default='../contract/asterisk.abi', help='Contract ABI file')
    parser.add_argument(
        '--bin', default='../contract/asterisk.bin', help='Contract BIN file')
    args = parser.parse_args()

    client = Client(args.account, args.provider, args.addr, args.abi)

    if(args.command == 'bid'):
        result = client.bid()
        print("Your bid was submitted.")
    elif(args.command == 'deploy'):
        client.deployContract(args.abi, args.bin)
    elif(args.command == 'list'):
        client.listAccounts()
    elif(args.command == 'solve'):
        client.solve()
    else:
        print(command, "is not yet implemented")
        quit()
