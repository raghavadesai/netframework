# NetFramework

A Python-based TCP/IP networking framework for building networked applications.

## Features

- Easy-to-use TCP Server and Client implementations
- Modular protocol system with JSON support out of the box
- Buffer management for handling incomplete messages
- Built-in logging and error handling
- Thread-safe implementation
- SSL/TLS support for secure communication

## Installation

```bash
pip install netframework
```

## Quick Start

### Basic Echo Server Example

```python
from netframework import TCPServer, JSONProtocol

class EchoProtocol(JSONProtocol):
    def process(self, data: bytes) -> str:
        message = self.deserialize(data)
        return f"Echo: {message}"

# Create and start an echo server
server = TCPServer(host='0.0.0.0', port=8000, protocol=EchoProtocol())
server.start()
```

### Secure Echo Server Example

```python
from netframework import TCPServer, JSONProtocol
from netframework.ssl_context import create_server_ssl_context

# Create SSL context
ssl_context = create_server_ssl_context(
    certfile="server.crt",
    keyfile="server.key"
)

# Create and start a secure echo server
server = TCPServer(
    host='0.0.0.0',
    port=8443,
    protocol=EchoProtocol(),
    ssl_context=ssl_context
)
server.start()
```

### Secure Echo Client Example

```python
from netframework import TCPClient, JSONProtocol
from netframework.ssl_context import create_client_ssl_context
import ssl

# Create SSL context
ssl_context = create_client_ssl_context(
    cafile="server.crt",  # Server's certificate for verification
    verify_mode=ssl.CERT_REQUIRED
)

# Create a secure client
client = TCPClient(JSONProtocol(), ssl_context=ssl_context)
client.connect('localhost', 8443)

# Send a message
client.send("Hello, Secure Server!")
response = client.receive()
print(f"Server response: {response}")
```

## Requirements

- Python 3.7+

## License

MIT License