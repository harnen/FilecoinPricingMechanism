from client import Client

import pytest
from web3 import EthereumTesterProvider, Web3
from unittest.mock import MagicMock


@pytest.fixture
def tester_provider():
    return EthereumTesterProvider()


@pytest.fixture
def eth_tester(tester_provider):
    return tester_provider.ethereum_tester


@pytest.fixture
def w3(tester_provider):
    return Web3(tester_provider)


@pytest.fixture
def contract(eth_tester, w3):
    deploy_address = eth_tester.get_accounts()[0]

    with open('../contract/asterisk.abi', 'r') as f:
        abi = f.read()
    with open('../contract/asterisk.bin', 'r') as f:
        bytecode = f.read()

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact(
        {'from': deploy_address, 'gas': 1000}
    )
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, 180)
    return contract(tx_receipt.contractAddress)


@pytest.fixture
def client(w3, contract):
    client = Client(MagicMock(), MagicMock(), 0, '../contract/asterisk.abi')
    client.contract = contract
    client.account = w3.eth.accounts[1]
    client.w3 = w3
    return client


def test_submit_bid(w3, client):
    ret = client.submit_bid(10, 10, 10, 1000)
    assert ret['blockNumber'] == 2
