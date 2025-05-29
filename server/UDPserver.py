import socket
import sys
import os
import random
import base64     
import threading  

DATA_PORT_RANGE = (50000, 51000)

def handle_file_transfer(filename, port, client_ip):
    print(f"[THREAD] Starting transfer for {filename} on port {port}", flush=True)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))

    with open(filename, "rb") as f:
        while True:
            try:
                packet, addr = sock.recvfrom(2048)
                if addr[0] != client_ip:
                    continue  # 忽略非本客户端的包

                message = packet.decode().strip()
                print(f"[THREAD RECEIVE] {message}", flush=True)

                parts = message.split(" ")
                if parts[0] != "FILE" or parts[1] != filename:
                    continue

                if parts[2] == "CLOSE":
                    response = f"FILE {filename} CLOSE_OK"
                    sock.sendto(response.encode(), addr)
                    break

                elif parts[2] == "GET" and parts[3] == "START" and parts[5] == "END":
                    start = int(parts[4])
                    end = int(parts[6])
                    f.seek(start)
                    data = f.read(end - start + 1)
                    encoded = base64.b64encode(data).decode()
                    response = f"FILE {filename} OK START {start} END {end} DATA {encoded}"
                    sock.sendto(response.encode(), addr)

            except Exception as e:
                print(f"[ERROR] Thread error: {e}", flush=True)
                break

    print(f"[THREAD] Transfer for {filename} finished.", flush=True)
    sock.close()

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
                        file_size = os.path.getsize(filename)  # 获取文件大小
                        data_port = random.randint(*DATA_PORT_RANGE)  #  随机分配数据传输端口
                        response = f"OK {filename} SIZE {file_size} PORT {data_port}"  # 构造成功响应
                    else:
                       response = f"ERR {filename} NOT_FOUND"     
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

