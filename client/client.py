from web3 import Web3
import argparse


class Client:
    def __init__(self, account, provider, address, abi_file):
        self.account = account
        self.w3 = Web3(Web3.HTTPProvider(provider))
        with open(abi_file) as f:
            abi = f.read()
        self.contract = self.w3.eth.contract(address=address, abi=abi)

    def check_connection(self):
        return self.w3.isConnected()

    def submit_bid(self, size, duration, price, gas):
        transaction = self.contract.functions.submitBid(size, duration, price)
        tx_hash = transaction.transact({'from': self.account, 'gas': gas})
        return self.w3.eth.waitForTransactionReceipt(tx_hash)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple Client.')
    # Used for bid submittion
    parser.add_argument('--addr', default='', help='Contract address')
    parser.add_argument(
        '--size', help='Storage size of your bid', required=True)
    parser.add_argument(
        '--duration', help='Duration of your bid', required=True)
    parser.add_argument('--price', help='Price of your bid', required=True)
    parser.add_argument(
        '--gas', help='Gas for your transaction', required=True)
    # used for client initialization
    parser.add_argument('--account', help='Self account', required=True)
    parser.add_argument(
        '--provider', default='http://localhost:30303', help='ethereum HTTP provider URL')
    parser.add_argument(
        '--abi', default='../contract/asterisk.abi', help='price bid parameter')
    args = parser.parse_args()

    client = Client(args.account, args.provider, args.addr, args.abi)
    if client.check_connection() is True:
        client.submit_bid(args.size, args.duration, args.price, args.gas)
    else:
        print('Error: The client is not connected to the Ethereum network.')
