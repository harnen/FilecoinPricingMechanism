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
    parser.add_argument('--size', help='size bid parameter')
    parser.add_argument('--duration', help='duration bid parameter')
    parser.add_argument('--bid', help='price bid parameter')
    args = parser.parse_args()

    ok = args.size is not None
    ok &= args.duration is not None
    ok &= args.bid is not None
    if not ok:
        parser.error('All parameters must be specified.')
