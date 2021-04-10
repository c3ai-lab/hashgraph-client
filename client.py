#!/usr/bin/env python

from thrift_gen import Transaction

from thrift import Thrift
from thrift.transport import TSSLSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import time, uuid, random, sys, getopt, argparse
from random import randrange


#python3 client.py -n localhost -p 9090 --calls 1000 --delay 1
#python3 client.py -n localhost -p 9090 --amount 99 --target 1
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
    elif args.amount and args.target:
        transport.open()
        transfer(int(args.amount), int(args.target), client)
        transport.close()
    elif args.calls and args.delay:
        transport.open()
        benchmark(int(args.calls), int(args.delay), client)
        transport.close()
    else:
        parser.print_help()
        sys.exit(0)

def benchmark(calls, delay, client):
    starttime = time.time()
    while True:
        print("Executing " + str(calls) + " transactions...")
        for _ in range(calls):
            transfer(randrange(100), random.randint(-1,3), client)
        time.sleep(delay - ((time.time() - starttime) % delay))

def transfer(amount, target, client):
    tx_id = client.transfer(amount, target)
    print('tx_id: %s' % tx_id)

def status(tx_id, client):
    status = client.status(tx_id)
    print('status: %s' % status.status)
    if status.consensus_time != 0:
        print('consensus time: %s' % status.consensus_time)

if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)
