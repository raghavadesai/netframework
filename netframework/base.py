import socket
import threading
import asyncio
from typing import Optional, Callable, Any
from .logger import setup_logger
from .buffer import Buffer
from .errors import NetworkError
from .protocol import Protocol, JSONProtocol

logger = setup_logger(__name__)

class TCPServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8000, 
                 protocol: Optional[Protocol] = None):
        self.host = host
        self.port = port
        self.protocol = protocol or JSONProtocol()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = set()
        self.running = False
        
    def start(self):
        """Start the server in blocking mode."""
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            logger.info(f"Server started on {self.host}:{self.port}")
            
            while self.running:
                client_socket, address = self.socket.accept()
                logger.info(f"New connection from {address}")
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                self.clients.add(client_socket)
                
        except Exception as e:
            logger.error(f"Server error: {e}")
            self.stop()
            
    def stop(self):
        """Stop the server and close all connections."""
        self.running = False
        for client in self.clients:
            client.close()
        self.socket.close()
        logger.info("Server stopped")
        
    def _handle_client(self, client_socket: socket.socket, address: tuple):
        """Handle individual client connections."""
        buffer = Buffer()
        
        try:
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                    
                buffer.append(data)
                
                while buffer.has_complete_message():
                    message = buffer.get_message()
                    processed = self.protocol.process(message)
                    if processed:
                        response = self.protocol.serialize(processed)
                        client_socket.sendall(response)
                        
        except Exception as e:
            logger.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            self.clients.remove(client_socket)
            logger.info(f"Connection closed from {address}")

class TCPClient:
    def __init__(self, protocol: Optional[Protocol] = None):
        self.protocol = protocol or JSONProtocol()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = Buffer()
        
    def connect(self, host: str, port: int):
        """Connect to a remote server."""
        try:
            self.socket.connect((host, port))
            logger.info(f"Connected to {host}:{port}")
        except Exception as e:
            raise NetworkError(f"Connection failed: {e}")
            
    def send(self, data: Any):
        """Send data to the server."""
        try:
            serialized = self.protocol.serialize(data)
            self.socket.sendall(serialized)
        except Exception as e:
            raise NetworkError(f"Send failed: {e}")
            
    def receive(self) -> Any:
        """Receive data from the server."""
        try:
            data = self.socket.recv(4096)
            if not data:
                return None
                
            self.buffer.append(data)
            
            if self.buffer.has_complete_message():
                message = self.buffer.get_message()
                return self.protocol.process(message)
        except Exception as e:
            raise NetworkError(f"Receive failed: {e}")
            
    def close(self):
        """Close the connection."""
        self.socket.close()
        logger.info("Connection closed")
