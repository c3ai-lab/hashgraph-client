#!/usr/bin/env python

from thrift_gen import Transaction

from thrift import Thrift
from thrift.transport import TSSLSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import time, uuid, random, sys, getopt, argparse, ecdsa, pathlib, os, codecs, sha3
from random import randrange
from Crypto.Hash import keccak

from ecdsa import SigningKey, SECP256k1
import sha3, random, binascii


pub_key_path = os.path.join(pathlib.Path(__file__).parent.absolute(), "public_key.pem")
priv_key_path = os.path.join(pathlib.Path(__file__).parent.absolute(), "private_key.pem")

#python3 client.py -n localhost -p 9090 --calls 1000 --delay 1
#python3 client.py -n localhost -p 9090 --amount 11 --target 11xa202effc3bb275689552d1ad1b0264c68de036dd
#python3 client.py -n localhost -p 9090 --status e45cc861a742436f9a27f88c081433d1
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", "-n", help="Define node address")
    parser.add_argument("--port", "-p", help="Define node port")
    parser.add_argument("--calls", "-c", help="Set amount of transaction calls to be done against the node")
    parser.add_argument("--delay", "-d", help="Set delay between amount of transaction calls")
    parser.add_argument("--amount", "-a", help="Set amount to be transferred")
    parser.add_argument("--target", "-t", help="Set target for transfer")
    parser.add_argument("--status", "-s", help="Request status from transaction id")
    parser.add_argument("--balance", "-b", help="Get balance from address")

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    if args.node and args.port:
        print("Set node to %s" % args.node)
        print("Set port to %s" % args.port)
        transport = TSSLSocket.TSSLSocket(host=args.node, port=args.port, certfile='.ssh/client.crt', keyfile='.ssh/client.key', ca_certs='.ssh/CA.pem')
    elif args.node:
        print("Set node to %s" % args.node)
        transport = TSSLSocket.TSSLSocket(host=args.node, certfile='.ssh/client.crt', keyfile='.ssh/client.key', ca_certs='.ssh/CA.pem')
    else:
        parser.print_help()
        sys.exit(0)

    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Transaction.Client(protocol)

    if args.status:
        transport.open()
        status(args.status, client)
        transport.close()
    elif args.balance:
        transport.open()
        balance(args.balance, client)
        transport.close()
    elif args.amount and args.target:
        transport.open()
        crypto_transfer(int(args.amount), str(args.target), client)
        transport.close()
    elif args.calls and args.delay:
        transport.open()
        benchmark(int(args.calls), int(args.delay), client)
        transport.close()
    else:
        parser.print_help()
        sys.exit(0)

def generate_key_pair():
    priv_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    pub_key = priv_key.get_verifying_key()
    open(priv_key_path, "wb").write(priv_key.to_pem())
    open(pub_key_path, "wb").write(pub_key.to_pem())
    
    return pub_key, priv_key

def get_key_pair():
    if not os.path.exists(pub_key_path) and not os.path.exists(priv_key_path):
        pub_key, priv_key = generate_key_pair()
    else:
        priv_key = ecdsa.SigningKey.from_pem(open(priv_key_path).read())
        pub_key = ecdsa.VerifyingKey.from_pem(open(pub_key_path).read())
    
    return pub_key, priv_key

def checksum(address):
    checksum = ''
    address = address[3:]
    address_byte_array = address.encode('utf-8')
    keccak = sha3.keccak_256()
    keccak.update(address_byte_array)
    keccak_digest = keccak.hexdigest()
    for i in range(len(address)):
        address_char = address[i]
        keccak_char = keccak_digest[i]
        if int(keccak_char, 16) >= 8:
            checksum += address_char.upper()
        else:
            checksum += str(address_char)
    
    #assert checksum(address) == address, f"{checksum(address)} != expected {address}"
    
    return '11x' + checksum

def benchmark(calls, delay, client):
    starttime = time.time()
    while True:
        print("Executing " + str(calls) + " transactions...")
        for _ in range(calls):
            crypto_transfer(randrange(100), str(random.randint(-1,3)), client)
        time.sleep(delay - ((time.time() - starttime) % delay))

def transfer(amount, target, client):
    tx_id = client.transfer(amount, target)
    print('tx_id: %s' % tx_id)

def crypto_transfer(amount, receiver, client):
    public_key, private_key = get_key_pair()
    challenge = os.urandom(10)
    signature = private_key.sign(bytes(amount) + str.encode(receiver) + challenge)

    #check = public_key.verify(sig, bytes(amount) + str.encode(receiver) + challenge)
    #print('check: %s' % check)

    tx_id = client.crypto_transfer(public_key.to_string(), amount, receiver, challenge, signature)
    print('tx_id: %s' % tx_id)

def status(tx_id, client):
    status = client.status(tx_id)
    print('status: %s' % status.status)
    if status.consensus_time != 0:
        print('consensus time: %s' % status.consensus_time)

def balance(address, client):
    balance = client.balance(address)
    print('balance: %s' % balance)

if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)