import json
import web3
import sys

from web3 import Web3


URL='http://128.40.39.170:8080/'



if (len(sys.argv) != 3):
    print("Provide filename to register - python3 send_money_to.py <recipient> <amount_in_wei>")
    quit()

recipient = str(sys.argv[1])
amount = int(sys.argv[2])

my_provider = Web3.HTTPProvider(URL)
w3 = Web3(my_provider)

# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]
w3.personal.unlockAccount(w3.eth.defaultAccount, 'testtest')

#web3py requires the address to be in this specific format when sending money to
converted_address = w3.toChecksumAddress(recipient)
#print("Converted address:", converted_address)

#quit()

tx = w3.personal.sendTransaction({'from': w3.eth.accounts[0], 'to': converted_address, 'value': amount}, passphrase='testtest')

w3.eth.waitForTransactionReceipt(tx)

print(amount, "wei sent to ", converted_address)

