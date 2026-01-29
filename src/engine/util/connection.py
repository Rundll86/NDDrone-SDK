from socket import AddressFamily, SocketKind, socket


def connectSocket(
    address: tuple[str, int],
    retryTimes: int,
    af: AddressFamily = AddressFamily.AF_INET,
    type: SocketKind = SocketKind.SOCK_STREAM,
) -> socket:
    resultSocket = socket(af, type)
    connected = False
    reconnectedTimes = 0
    while not connected:
        try:
            resultSocket.connect(address)
            connected = True
        except Exception:
            reconnectedTimes += 1
            if reconnectedTimes > retryTimes:
                raise ValueError(f"Cannot connect to {address}.")
    return resultSocket
