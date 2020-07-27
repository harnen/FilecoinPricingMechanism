# Filecoin Pricing Mechanism (FPM)


We can build and test the project using [scaffold-eth](https://github.com/austintgriffith/scaffold-eth). It's a framework for quickly deploying and running smart contracts and is explained  [here](https://www.youtube.com/watch?v=eUAc2FtC0_s).

For the fronted, [fleek](https://fleek.co/) seems like a good solution. We can create a simple website interface and deploy it on IPFS.


# Prerequisites

To compile the smart contract you'll need solc: `sudo snap install solc`

The scripts require Python > 3.6 and following packages: `sudo pip3 install web3 numpy pandas`

You need geth to run your local blockchain instance

# Running

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
