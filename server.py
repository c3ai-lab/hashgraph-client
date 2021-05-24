#!/usr/bin/env python

from thrift_gen import Transaction
from thrift_gen.ttypes import Status, BalanceTransfer

from thrift.transport import TSSLSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from ecdsa import VerifyingKey, SECP256k1, util
from datetime import datetime

import uuid, random, time, hashlib, os

class TransactionHandler:
    def __init__(self):
        self.log = {}

    def transfer(self, payload, target):
        tx_id = uuid.uuid4().hex
        print('transfer(%s, %d, %d)' % (tx_id, payload, target))
        return str(tx_id)

    def crypto_transfer(self, owner, amount, receiver, challenge, signature):
        print('crypto_transfer(%s, %s)' % (amount, receiver))

        #Create address by hashing public key
        public_key = VerifyingKey.from_der(owner)
        public_key_hash = hashlib.sha3_256()
        public_key_hash.update(public_key.to_der())
        address = '11x' + public_key_hash.hexdigest()[24:]
        print('Address: ', address)

        message = challenge + b"|" + bytes(f'{amount}', "utf-8") + b"|" + str.encode(receiver)
        check   = public_key.verify(signature, message, hashlib.sha256, util.sigdecode_der)
        print('Signature verification:', check)
    
    def status(self, tx_id):
        status = Status()
        print(type(status))
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

    def challenge(self):
        challenge = os.urandom(10)
        #Store this challenge in the hashgraph for future retrieval and verification...

        print('challenge(%s)' % (challenge.hex()))
        return challenge
    
    def balance_history(self, address):
        history_list = []

        for x in range(5):
            balance_history = BalanceTransfer()

            balance_history.amount = random.randrange(100)
            balance_history.receiverId = uuid.uuid4().hex
            balance_history.senderId = uuid.uuid4().hex
            balance_history.timestamp = random.randrange(99999999)

            history_list.append(balance_history)

        print('balance_hisotry(%s, %s)' % (address, history_list))
        return history_list


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