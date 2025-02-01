import ssl
from netframework import TCPClient, JSONProtocol
from netframework.ssl_context import create_client_ssl_context

def main():
    # Create SSL context for client
    ssl_context = create_client_ssl_context(
        cafile="examples/server.crt",  # Use server's certificate for verification
        verify_mode=ssl.CERT_REQUIRED
    )

    # Create a secure client with JSON protocol
    client = TCPClient(
        JSONProtocol(),
        ssl_context=ssl_context
    )

    try:
        # Connect to the secure echo server
        client.connect('localhost', 8443)

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
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    main()