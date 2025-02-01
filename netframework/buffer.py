class Buffer:
    def __init__(self, delimiter: bytes = b'\n'):
        self.delimiter = delimiter
        self.buffer = bytearray()
        
    def append(self, data: bytes):
        """Append data to the buffer."""
        self.buffer.extend(data)
        
    def has_complete_message(self) -> bool:
        """Check if there's a complete message in the buffer."""
        return self.delimiter in self.buffer
        
    def get_message(self) -> bytes:
        """Get the next complete message from the buffer."""
        if not self.has_complete_message():
            return None
            
        # Find the delimiter
        delimiter_index = self.buffer.index(self.delimiter)
        
        # Extract the message
        message = bytes(self.buffer[:delimiter_index])
        
        # Remove the message and delimiter from the buffer
        self.buffer = self.buffer[delimiter_index + len(self.delimiter):]
        
        return message
        
    def clear(self):
        """Clear the buffer."""
        self.buffer.clear()
