import json
import web3
import sys

from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract


IPC_PATH='/home/harnen/.ethereum/geth.ipc'
CONTRACT_ADDR='0x29B471eA3057e459b04497ecf0E8Fa9bFC6162Cf'
URL='http://128.40.39.170:8080/'
contract_file='../contract/pop.sol'
abi_file='../contract/pop.abi'
bin_file='../contract/pop.bin'
contract_abi = ""
contract_bin = ""

if (len(sys.argv) != 5):
    print("Provide filename to register - python3 read_contract.py <contract_address> <fileID> <sender> <recipient>")
    quit()

CONTRACT_ADDR = Web3.toChecksumAddress(str(sys.argv[1]))
fileID = str(sys.argv[2])
sender = Web3.toChecksumAddress(str(sys.argv[3]))
recipient = Web3.toChecksumAddress(str(sys.argv[4]))

with open(abi_file, 'r') as myfile:
    contract_abi = myfile.read()
    myfile.close()
with open(bin_file, 'r') as myfile:
    contract_bin = myfile.read()
    myfile.close()

# web3.py instance
#my_provider = Web3.IPCProvider(IPC_PATH)
my_provider = Web3.HTTPProvider(URL)

w3 = Web3(my_provider)

# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]
w3.personal.unlockAccount(w3.eth.defaultAccount, 'testtest')


print('Using contract address', CONTRACT_ADDR)

# Create the contract instance with the newly-deployed address
pop = w3.eth.contract(
    address=CONTRACT_ADDR,
    abi=contract_abi,
)


tx_hash = pop.functions.registerTransfer(fileID, sender, recipient).transact()
w3.eth.waitForTransactionReceipt(tx_hash)

value = pop.functions.balances(w3.eth.accounts[0]).call()
print("Registered transfer of file", fileID, "from", sender, "to", recipient)

