#!/usr/bin/env python

from thrift_gen import Transaction

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class TransactionHandler:
    def __init__(self):
        self.log = {}

    def transfer(self, payload, target):
        print('transfer(%d,%d)' % (payload, target))


if __name__ == '__main__':
    handler = TransactionHandler()
    processor = Transaction.Processor(handler)
    # TODO: Switch to SSL sockets
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('Done.')