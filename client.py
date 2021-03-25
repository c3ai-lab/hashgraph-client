#!/usr/bin/env python

from thrift_gen import Transaction

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import time
import random
from random import randrange


def main():
    # Make socket
    # TODO: Use SSL sockets
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = Transaction.Client(protocol)

    # Load test parameters
    starttime = time.time()
    amount_calls = 1000
    delay_seconds = 1.0

    # Connect!
    transport.open()

    while True:
        print("Executing " + str(amount_calls) + " calls...")
        for _ in range(amount_calls):
            client.transfer(randrange(100), random.randint(-1,3))
        time.sleep(delay_seconds - ((time.time() - starttime) % delay_seconds))

    # Close!
    transport.close()


if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)
