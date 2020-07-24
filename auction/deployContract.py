import json
import web3

from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract


IPC_PATH='~/.ethereum/geth.ipc'
URL='http://128.40.39.170:8080/'
contract_file='../contract/pastrami.sol'
abi_file='../contract/pastrami.abi'
bin_file='../contract/pastrami.bin'
contract_abi = ""
contract_bin = ""



#with open(contract_file, 'r') as myfile:
#    contract_source_code=myfile.read()
#    myfile.close()
#compiled_sol = compile_source(contract_source_code) # Compiled source code
#contract_interface = compiled_sol['<stdin>:pop']
with open(abi_file, 'r') as myfile:
    contract_abi = myfile.read()
    myfile.close()
with open(bin_file, 'r') as myfile:
    contract_bin = myfile.read()
    myfile.close()

print("Read abi:", contract_abi)
print("Read bin:", contract_bin)

# web3.py instance
#w3 = Web3(Web3.EthereumTesterProvider())
#my_provider = Web3.IPCProvider(IPC_PATH)
my_provider = Web3.HTTPProvider(URL)
w3 = Web3(my_provider)


print("Am I connected?", w3.isConnected())

# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]

w3.personal.unlockAccount(w3.eth.defaultAccount, 'testtest')

# Instantiate and deploy contract
Greeter = w3.eth.contract(abi=contract_abi, bytecode=contract_bin)

# Submit the transaction that deploys the contract
tx_hash = Greeter.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print('Contract address', tx_receipt.contractAddress)

# Create the contract instance with the newly-deployed address
greeter = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_abi,
)

# Display the default greeting from the contract
print('Calling a function: {}'.format(
    greeter.functions.put().transact()
))


# Wait for transaction to be mined...
w3.eth.waitForTransactionReceipt(tx_hash)

