import socket
import sys
import os
import random

DATA_PORT_RANGE = (50000, 51000)

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
                parts = decoded_msg.split(" ")  # 解析命令
                if len(parts) != 2:  # 检查格式
                    response = "ERR MALFORMED_REQUEST"  
                else:
                    filename = parts[1]  
                    if os.path.isfile(filename):  # 检查文件是否存在
                        file_size = os.path.getsize(filename)  # [NEW] 获取文件大小
                        data_port = random.randint(*DATA_PORT_RANGE)  # [NEW] 随机分配数据传输端口
                        response = f"OK {filename} SIZE {file_size} PORT {data_port}"  # [NEW] 构造成功响应
                    else:
                       response = f"ERR {filename} NOT_FOUND"  # [NEW]   
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

