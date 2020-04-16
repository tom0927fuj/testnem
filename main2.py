#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal, getcontext
from binascii import hexlify
from pprint import pprint

def main():
    rpc_user = 'rpcuser'
    rpc_password = 'Cq@q7K&pYX3e4eCM!7'
    rpc = AuthServiceProxy(f'http://{rpc_user}:{rpc_password}@127.0.0.1:18332/')
    #rpc = AuthServiceProxy(f'http://{rpc_user}:{rpc_password}@172.17.0.2:18332/')
    print(rpc.getinfo())
    best_block_hash = rpc.getbestblockhash()
    print(rpc.getblock(best_block_hash))
    blhash = rpc.getblockhash(0) #blhashはブロックのhash文字列
    bl = rpc.getblock(blhash) #blはブロック情報
    print(bl)
    dummy_address = '2MudgRfNaaw96kqAWziZ5JGsPbo2pzQp7Jy'
    change_address = '2NAVrak22jX3DQyDqnoqdm5ZTak1RgXWPzo'

    filename = 'mark_token.btc.json'
    url='https://drive.google.com/file/d/1ZR6Q5sCM_acUpPy7s3d9GJH8I2Plh4FI/view?usp=sharing'

    with open(filename, 'rb') as f:
        data2 = f.read()
    hashdata=hashlib.sha256(data2).hexdigest()
    js={'file_hash':hashdata,'url':url}
    data=json.dumps(js).encode("UTF-8")


    while True:
        if len(data) >= 80:
            buffer = data[:80]
            data = data[80:]
        elif len(data) == 0:
            break
        else:
            buffer = data
            data = b''

        first_unspent = rpc.listunspent()[0]
        txid = first_unspent['txid']
        vout = first_unspent['vout']
        input_amount = first_unspent['amount']
        SATOSHI = Decimal("0.00000001")
        change_amount = input_amount - Decimal("0.005") - SATOSHI

        tx = rpc.createrawtransaction([{"txid": txid, "vout": vout}],[{change_address: change_amount}, {'data': hexlify(buffer).decode('utf-8')}, ])
        tx = rpc.signrawtransactionwithwallet(tx)['hex']
        rpc.sendrawtransaction(tx)

    block_hash = rpc.generatetoaddress(1, change_address)[0]
    block = rpc.getblock(block_hash)
    txs = block['tx'][1:]

    print(f'# of txs: {len(txs)}')
    pprint(txs)

    for tx_hash in txs:
        raw_tx = rpc.gettransaction(tx_hash)['hex']
        decoded_tx = rpc.decoderawtransaction(raw_tx)
        # pprint(decoded_tx)
        print(decoded_tx['vout'][1]['scriptPubKey']['asm'])

if __name__ == '__main__':
    main()
