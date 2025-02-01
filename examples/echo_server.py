from netframework import TCPServer, JSONProtocol

class EchoProtocol(JSONProtocol):
    def process(self, data: bytes) -> str:
        # Deserialize the message and echo it back
        message = self.deserialize(data)
        return f"Echo: {message}"

def main():
    # Create and start an echo server
    server = TCPServer(host='0.0.0.0', port=8000, protocol=EchoProtocol())
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

if __name__ == '__main__':
    main()
