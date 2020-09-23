# Filecoin Pricing Mechanism (PASTRAMI)

This repository contains implementation for Filecoin Pricing Mechanism aka PASTRAMI. The mechanism was described in details in [this paper](https://arxiv.org/pdf/2004.06403.pdf). For a quick overview you can watch this [highlight video](https://www.youtube.com/watch?v=hM1afoJ4KCI).

## Prerequisite
To run the FPM you need [geth](https://geth.ethereum.org/downloads/), Python > 3.6 and bash.

On ubuntu run:

```sudo apt install geth python3 python3-pip```

Furthermore, FPM uses numpy, pandas and [web3py](https://github.com/ethereum/web3.py) Python libraries that can be installed using pip:

`pip3 install web3py numpy pandas`

## Blockchain

Init a new blockchain with preseeded accounts:
```
cd ./scripts
./initialize_blockchain.sh
```

Run a geth node:
``` 
cd ./scripts
./run_blockchain
```

To submit transactions you need to start mining and type the following in the geth console:
`miner.start()`
