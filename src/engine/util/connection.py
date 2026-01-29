import socket


def connectSocket(address: tuple[str, int], retryTimes: int) -> socket.socket:
    result = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    notconnect = True
    reconnecttime = 0
    while notconnect:
        try:
            result.connect(address)
            notconnect = False
        except Exception:
            reconnecttime += 1
            if reconnecttime > retryTimes:
                raise ValueError(f"Cannot connect to {address}.")
    return result
