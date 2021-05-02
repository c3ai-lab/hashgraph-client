#!/usr/bin/env python

from thrift_gen import Transaction
from thrift_gen.ttypes import Status

from thrift.transport import TSSLSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from ecdsa import VerifyingKey, SECP256k1

import uuid, random, time, sha3

class TransactionHandler:
    def __init__(self):
        self.log = {}

    def transfer(self, payload, target):
        tx_id = uuid.uuid4().hex
        print('transfer(%s, %d, %d)' % (tx_id, payload, target))
        return str(tx_id)

    def crypto_transfer(self, owner, amount, receiver, challenge, signature):
        tx_id = uuid.uuid4().hex
        print('crypto_transfer(%s, %s, %s)' % (tx_id, amount, receiver))

        #Create address by hashing public key
        public_key = VerifyingKey.from_string(owner, curve=SECP256k1)
        keccak = sha3.keccak_256()
        keccak.update(public_key.to_string())
        address = '11x' + keccak.hexdigest()[24:]
        print('Address: ', address)

        check = public_key.verify(signature, bytes(amount) + str.encode(receiver) + challenge)
        print('Signature verification:', check)

        return str(tx_id)
    
    def status(self, tx_id):
        status = Status()
        options = ['submitted to node', 'submitted for consensus', 'consensus reached']
        status.status = random.choice(options)
        status.consensus_time = int()
        if status.status == 'consensus reached':
            status.consensus_time = int(time.time())

        print('status(%s, %s, %d)' % (tx_id, status.status, status.consensus_time))
        return status
    
    def balance(self, address):
        balance = random.randrange(1000)

        print('balance(%s, %s)' % (address, balance))
        return balance


if __name__ == '__main__':
    handler = TransactionHandler()
    processor = Transaction.Processor(handler)
    transport = TSSLSocket.TSSLServerSocket(host='127.0.0.1', port=9090, certfile='.ssh/server.crt', keyfile='.ssh/server.key')
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('Done.')