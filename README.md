# Chrysós Hashgraph Python Client
This is a Python Client which can be used to connect and interact with the [Chrysós Hashgraph Network](https://github.com/c3ai-lab/hashgraph) via SSL sockets utilizing the [Apache Thrift Framework](https://thrift.apache.org) for RPC communication with the nodes.

It currently supports the following functionalities:
- Key generation
- Address display
- Transactions
- Balance and history requests
- Benchmarking
- Node specification

## Prerequisites
- python3
- thrift

### Thrift
You can either use the included `thrift_gen` folder or generate your own by running `thrift -r -out . --gen py hashgraph-client.thrift`

## Key pairs
The client will automatically check for ECDSA SECP256k1 PEM keys (`public_key.pem`, `private_key.pem`) in the root folder  and if none are present, they will automatically be generated. These keys will be used to sign transactions and generate your address.

## Usage
You can use the client functionalities via your command line. Just execute the python file (`python3 client.py`) and add your command as argument to the call, i.e. (`python3 client.py --address`).

### Examples
- Displaying your own address: `python3 client.py --address`
- Retrieving your own balance: `python3 client.py -n localhost -p 9090 -c .ssh/CA.pem --balance`
- Transfer to address 11xa202effc3bb275689552d1ad1b0264c68de036dd: `python3 client.py -n localhost -p 9090 -c .ssh/CA.pem --amount 11 --target 11xa202effc3bb275689552d1ad1b0264c68de036dd`
- Retrieving the balance for address 11xa202effc3bb275689552d1ad1b0264c68de036dd `python3 client.py -n localhost -p 9090 -c .ssh/CA.pem --balance 11xa202effc3bb275689552d1ad1b0264c68de036dd`
- Retrieving your own history: `python3 client.py -n localhost -p 9090 -c .ssh/CA.pem --history`
- Retrieving the history for address 11xa202effc3bb275689552d1ad1b0264c68de036dd `python3 client.py -n localhost -p 9090 -c .ssh/CA.pem --history 11xa202effc3bb275689552d1ad1b0264c68de036dd`

Note that for a majority of the calls, you need to specify the address `-n` (and port `-p`, if applicable) of the node you'd like to use. To establish a connection via SSL, you will also need to specify the path to the certificate `-c` of the node. A list of all publicly available nodes will soon™ be added.

You can also use `--help` to receive a full list of all arguments and their descriptions.

### Server
This project also contains a test server, which is used to simulate a working [Chrysós Hashgraph Network](https://github.com/c3ai-lab/hashgraph) node including the same RPC endpoints. It is contained for testing and integration purposes, since both this test server and the nodes work with the same Thrift file.

Once you start the server (`python3 server.py`), it should be reachable at `localhost:9090`.