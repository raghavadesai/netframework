from netframework import TCPClient, JSONProtocol

def main():
    # Create a client with JSON protocol
    client = TCPClient(JSONProtocol())
    
    try:
        # Connect to the echo server
        client.connect('localhost', 8000)
        
        while True:
            # Get user input
            message = input("Enter message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
                
            # Send the message
            client.send(message)
            
            # Receive and print the response
            response = client.receive()
            print(f"Server response: {response}")
            
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        client.close()

if __name__ == '__main__':
    main()
