# Filecoin Pricing Mechanism (PASTRAMI)

This repository contains implementation for Filecoin Pricing Mechanism aka PASTRAMI. The mechanism was described in details in [this paper](https://arxiv.org/pdf/2004.06403.pdf). For a quick overview you can watch this [highlight video](https://www.youtube.com/watch?v=hM1afoJ4KCI).

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
