# -*- coding: utf-8 -*-
from nemnis import Client, explain_status
import json
from decimal import Decimal, getcontext
from binascii import hexlify
from pprint import pprint



def main():
    nis = Client()
    hb = nis.heartbeat()

    senderAddress="TCPWWG327BPLTSB62733CWEV3L37INFRZ4A6TKUR"
    pubkey="2e884d52108390c45511a4f2e3d734769645513e23883646e8f31d99a068f6a5"
    prikey="5a82f55131b407aa6e295688a16e801cba922b0346a79e23c3348fc84893ff61"

    status = nis.status()
    timestamp=nis.call('GET', 'time-sync/network-time').json()['sendTimeStamp']
    recipient="TAJQJIVTOOZNBYSVWDXUEZESPLO6AL456NBBO24L"
    version=-1744830463
    type=257

    filename = 'mark_token.nem.json'
    with open(filename, 'rb') as f:
        data = f.read()
    print(len(data))

    while True:
        if len(data) >= 1024:
            buffer = data[:1024]
            data = data[1024:]
        elif len(data) == 0:
            break
        else:
            buffer = data
            data = b''
        microFee=((int)(len(buffer)/32)+1)*1000000*0.05
        microAmount=0
        print(len(buffer))
        print(microFee)
        exit()
        txObj = {'timeStamp': timestamp,
              'amount': microAmount,
              'fee': microFee,
              'recipient': recipient,
              'type': 257,  #transter transaction
              'deadline': deadline,
              'message': {
                'type': 1, #暗号化なし 1 暗号化あり 2
                'payload': hexlify(buffer).decode('utf-8')
              },
              'version': version,
              'signer': pubkey
            }

    exit()
    print(status.json())

    # you can use following function to get verbose message for status
    print(explain_status(status.json()))

    print(hb.status_code)

    print(hb.json())

    acc = nis.account.get('TAJQJIVTOOZNBYSVWDXUEZESPLO6AL456NBBO24L')

    print(acc.status_code)

    print(acc.json())

    acc2 = nis.account.get('TCPWWG327BPLTSB62733CWEV3L37INFRZ4A6TKUR')

    print(acc2.status_code)

    print(acc2.json())

    ### You can connect to other nodes just by passing it address:
    new_client =  Client('http://127.0.0.1:7890')

    new_hb = new_client.heartbeat()

    print(new_hb.status_code)

    print(new_hb.json())


if __name__ == '__main__':
    main()
