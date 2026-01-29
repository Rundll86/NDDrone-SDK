from socket import AddressFamily, SocketKind, socket

from engine.api.logging import loggerMain


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
                loggerMain.warning(f"Cannot connect to {address}.")
                break
    return resultSocket
