import socket
from time import sleep


def sendSocket(_type, _state):
    interfaces = socket.getaddrinfo(
        host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]

    port = 1688
    serverMac = "123"
    state = _state if len(_state) > 0 else "0"
    clientId = "all"
    type = _type if len(_type) > 0 else "1"
    body = serverMac+'-'+state+'-'+clientId+'-'+type

    bodyBytes = bytearray()
    bodyBytes.extend(map(ord, body))

    socketHeaderLength = 12
    socketBodyLength = bodyBytes.__len__()
    socketVersionHeader = 8899
    socketCommand = 142
    socketRequestId = 0

    buff = bytearray(socketHeaderLength + socketBodyLength)
    # header version: int
    buff[0] = socketVersionHeader & 0xff
    buff[1] = socketVersionHeader >> 8 & 0xff

    # header command: int
    buff[2] = socketCommand & 0xff
    buff[3] = socketCommand >> 8 & 0xff

    # header request id: unique Int, optional
    buff[4] = socketRequestId & 0xff
    buff[5] = socketRequestId >> 8 & 0xff
    buff[6] = socketRequestId >> 16 & 0xff
    buff[7] = socketRequestId >> 24 & 0xff

    if (body.__len__() > 0):
        # header body length: int
        buff[8] = socketBodyLength & 0xff
        buff[9] = socketBodyLength >> 8 & 0xff
        buff[10] = socketBodyLength >> 16 & 0xff
        buff[11] = socketBodyLength >> 24 & 0xff

        # body
        buff[socketHeaderLength:] = bodyBytes

    print('body length: ', body, socketBodyLength, bodyBytes)
    print('port: %d' % port)
    print("data: ", "".join(format(x, '02x') for x in buff))
    print('buff', buff.__len__(), buff)

    for ip in allips:
        try:
            print('sending on ',ip)
            sock = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip, 0))
            sock.sendto(buff, ("255.255.255.255", port))
            sock.close()
        except:
            print("An exception occurred when sending to", ip)

    print(f'Done sending')
