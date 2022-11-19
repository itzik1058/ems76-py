from ems76.shared.network.server import Server


class LoginServer(Server):
    def __init__(self, address):
        super(LoginServer, self).__init__(address)
