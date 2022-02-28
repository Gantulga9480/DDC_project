import socket
import select


class UdpBase:

    def __init__(self) -> None:
        self.soc = None
        self.ip = None
        self.port = None
