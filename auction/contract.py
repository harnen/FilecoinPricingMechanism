import json
import web3
import sys
from web3 import Web3
from web3.contract import ConciseContract


IPC_PATH='../data/geth.ipc'
ABI_FILE='../contract/asterisk.abi'
BIN_FILE='../contract/asterisk.bin'
contract_abi = ""
contract_bin = ""

def connect(ipc_path):
    my_provider = Web3.IPCProvider(ipc_path)
    w3 = Web3(my_provider)
    if(w3.isConnected()):
        print("Connected to geth!")
        return w3
    else:
        print("Couldn't connect to geth")
        quit()

def deployContract(w3, contract_abi, contract_bin):
    # Instantiate and deploy contract
    contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bin)
    tx_hash = contract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt.contractAddress

    
def getContract(w3, contract_abi, contract_bin, contract_addr):
    # Create the contract instance with the newly-deployed address
    print('Getting contract at', contract_addr)
    contract = w3.eth.contract(
        address=contract_addr,
        abi=contract_abi,
    )
    return contract

def readContract(w3, contract):
    value = contract.functions.balances(w3.eth.accounts[0]).call()
    print("Registered transfer of file", fileID, "from", sender, "to", recipient)

def addItem(w3, contract, size, duration, price):
    tx_hash = contract.functions.addItem(size, duration, price).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

with open(ABI_FILE, 'r') as myfile:
    contract_abi = myfile.read()
    myfile.close()
with open(BIN_FILE, 'r') as myfile:
    contract_bin = myfile.read()
    myfile.close()

w3 = connect(IPC_PATH)
w3.eth.defaultAccount = w3.eth.accounts[0]
w3.geth.personal.unlockAccount(w3.eth.defaultAccount, 'password')

contract_addr = deployContract(w3, contract_abi, contract_bin)
print("Deployed a contract at:", contract_addr)
contract = getContract(w3, contract_abi, contract_bin, contract_addr)
print("Got contract instance:", contract)

addItem(w3, contract, 10, 99, 5)






