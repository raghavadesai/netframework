# NetFramework

A Python-based TCP/IP networking framework for building networked applications.

## Features

- Easy-to-use TCP Server and Client implementations
- Modular protocol system with JSON support out of the box
- Buffer management for handling incomplete messages
- Built-in logging and error handling
- Thread-safe implementation

## Installation

```bash
pip install netframework
```

## Quick Start

### Echo Server Example

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

### Echo Client Example

```python
from netframework import TCPClient, JSONProtocol

# Create a client with JSON protocol
client = TCPClient(JSONProtocol())
client.connect('localhost', 8000)

# Send a message
client.send("Hello, Server!")
response = client.receive()
print(f"Server response: {response}")
```

## Requirements

- Python 3.7+

## License

MIT License
