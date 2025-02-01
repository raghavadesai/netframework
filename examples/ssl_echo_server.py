import os
import ssl
from netframework import TCPServer, JSONProtocol
from netframework.ssl_context import create_server_ssl_context
from netframework.logger import setup_logger

logger = setup_logger(__name__)

class EchoProtocol(JSONProtocol):
    def process(self, data: bytes) -> str:
        # Deserialize the message and echo it back
        message = self.deserialize(data)
        return f"Secure Echo: {message}"

def main():
    server = None  # Initialize server variable
    try:
        # Create SSL context with self-signed certificate
        ssl_context = create_server_ssl_context(
            certfile="examples/server.crt",
            keyfile="examples/server.key"
        )

        # Create and start a secure echo server
        server = TCPServer(
            host='0.0.0.0',
            port=8443,
            protocol=EchoProtocol(),
            ssl_context=ssl_context
        )

        logger.info("Starting secure echo server...")
        server.start()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        server.stop()
    except Exception as e:
        logger.error(f"Server error: {e}")
        if server:
            server.stop()

if __name__ == '__main__':
    main()