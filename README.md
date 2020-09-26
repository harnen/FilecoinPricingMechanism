# Filecoin Pricing Mechanism (PASTRAMI)

This repository contains implementation for Filecoin Pricing Mechanism aka PASTRAMI. The mechanism was described in details in [this paper](https://arxiv.org/pdf/2004.06403.pdf). For a quick overview you can watch this [highlight video](https://www.youtube.com/watch?v=hM1afoJ4KCI).

## Prerequisite
To run the FPM you need [geth](https://geth.ethereum.org/downloads/), Python > 3.6 and bash.

On ubuntu run:

```sudo apt install geth python3 python3-pip```

Furthermore, FPM uses numpy, pandas and [web3py](https://github.com/ethereum/web3.py) Python libraries that can be installed using pip:

`pip3 install web3py numpy pandas`

## Blockchain

To simplify tests, the software version in this repository creates a new private Ethereum blockchain with preseeded accounts. To create a new blockchain execute
```
cd ./scripts
./initialize_blockchain.sh
```

To run a geth node with the default configutation run:
``` 
cd ./scripts
./run_blockchain
```

To submit transactions you need to start mining and type the following in the geth console open by the previous command:
`miner.start()`

## CLI
FPM implements a simple CLI to interact with the Python client reading from and writing to the blockchain. By default, the client will interact with the local geth instance created in the previous step. 

The client is located in the auction folder:
`cd auction`

You can list current accounts using:
`./client list`

You need to use one of those accounts to interact with the blockchains. The accounts have pre-allocated funds that can be spent. 

To deploy the FPM contract use:
`./client deploy --account 0x5AB16852FB28d800994cD3a7F69359AD062f497b`
The command will return the address of the contract. You'll have to use it in the next steps.

To submit items:
`./client item --account 0x5AB16852FB28d800994cD3a7F69359AD062f497b --addr <contract_address>`

To bid for items:
`./client bid --account 0x5AB16852FB28d800994cD3a7F69359AD062f497b --addr <contract_address>`

NOTE: in the `scripts` folder, you'll find a `populate.sh` script automatically adding mutiple bids and items to the contract without user interaction.

To solve an auction:
`./client solve --account 0x5AB16852FB28d800994cD3a7F69359AD062f497b --addr <contract_address>`

The client allows to submit an incorrect solution using:
`./client solve-fake --account 0x5AB16852FB28d800994cD3a7F69359AD062f497b --addr <contract_address>`

To verify an auction:
`./client verify --account 0x5AB16852FB28d800994cD3a7F69359AD062f497b --addr <contract_address>`


## Recreating paper results
This section provides information on how to run FPM. The comparison in the paper was made against VSA available [here](https://github.com/HSG88/AuctionContract). 

To benchmark auction solving and verification prosess run:

```
cd auction
./multi_dutch.py
```
The main function creates random auction of increasing size, measures the time required to perform each procedure and create a Python dictionary with aggregated results. 

For the Ethereum gas measurements, you can use CLI (deploy, item, bid) and observe the gas usage returned by Geth. 

To recreate Filecoin results (Fig. 7, 8) run:

```
cd auction
./read_filecoin.py
````
The script reads storage node prices from `./data/filecoin_miners.json` and benchmarks the auction mechanism with different number of of bidders. Note that the prices declared might have changed in the meantime. You can thus update the JSON file and the script will perform the same calculations over new data. 



