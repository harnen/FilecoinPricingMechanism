import pytest
from web3 import EthereumTesterProvider, Web3

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

    abi = """ """  # TODO
    bytecode = """ """  # TODO

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact({'from': deploy_address,})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, 180)
    return contract(tx_receipt.contractAddress)


def test_submit_bid(w3, contract):
    assert True # TODO https://web3py.readthedocs.io/en/stable/examples.html#contract-unit-tests-in-python
