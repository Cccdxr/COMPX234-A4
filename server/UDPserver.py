import socket
import sys

def start_server(host, port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the specified host and port
    server_socket.bind((host, port))
    
    # Print server startup information
    print(f"[INFO] Server started on {host}:{port}", flush=True)

    while True:
        try:
            # Receive data from client
            message, client_address = server_socket.recvfrom(1024)
            decoded_msg = message.decode().strip()
            print(f"[RECEIVED] From {client_address}: {decoded_msg}", flush=True)

            # Check the command and respond accordingly
            if decoded_msg.startswith("DOWNLOAD"):
                response = "OK dummy.pdf SIZE 123456 PORT 50001"
            else:
                response = "ERR UNKNOWN_COMMAND"

            # Send the response to the client
            server_socket.sendto(response.encode(), client_address)
            print(f"[SENT] To {client_address}: {response}", flush=True)
            
        except KeyboardInterrupt:
            # Handle the interrupt signal
            print("\n[INFO] Server shutting down...", flush=True)
            server_socket.close() # Close the socket
            sys.exit(0) # Exit the program

if __name__ == "__main__":
    # Ensure the port argument is passed
    if len(sys.argv) != 2:
        print("Usage: python UDPserver.py <port>", flush=True)
        sys.exit(1)

    port = int(sys.argv[1]) # Get the port number
    start_server("0.0.0.0", port) # Start the server

