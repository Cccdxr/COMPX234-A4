import socket
import sys
import os
import base64


def main():
    # Check command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python UDPclient.py <server_host> <port> <filelist.txt>")
        sys.exit(1)
        
    server_host = sys.argv[1]
    port = int(sys.argv[2])
    filelist_path = sys.argv[3]
    
    # Check if the file list exists
    if not os.path.exists(filelist_path):
        print("[ERROR] filelist.txt not found")
        sys.exit(1)
        
    # Read and process each file name from the list
    with open(filelist_path, "r") as filelist:
        for line in filelist:
            filename = line.strip()
            if filename:
                download_file(server_host, port, filename)
                
def send_and_receive(sock, message, server_address, retries=5, timeout=1.0):
    attempt = 0
    while attempt < retries:
        try:
            sock.settimeout(timeout)
            sock.sendto(message.encode(), server_address)
            response, _ = sock.recvfrom(4096)
            return response.decode()
        except socket.timeout:
            attempt += 1
            print(f"[TIMEOUT] Attempt {attempt}: No response. Retrying...", flush=True)
            timeout *= 2  # Exponential backoff
    print("[FAIL] No response after maximum retries.", flush=True)
    return None

def download_file(server_host, port, filename):
    print(f"[INFO] Requesting file: {filename}", flush=True)

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Construct and send DOWNLOAD request
    request = f"DOWNLOAD {filename}"
    response = send_and_receive(sock, request, (server_host, port))

    if response is None:
        print(f"[FAIL] No response from server for file {filename}")
        return

    parts = response.strip().split(" ")

    if parts[0] == "ERR":
        print(f"[ERROR] Server responded: {response}")
    elif parts[0] == "OK":
        fname = parts[1]
        
        try:
            filesize = int(parts[parts.index("SIZE") + 1])
            data_port = int(parts[parts.index("PORT") + 1])
        except (ValueError, IndexError) as e:
            print(f"[ERROR] Malformed OK response: {response}")
            return

        print(f"[OK] {fname} is available, size={filesize} bytes, data_port={data_port}")
        
        # Create a new socket for data transfer
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        with open(filename, "wb") as f:
            total_received = 0
            block_size = 1000
            
            while total_received < filesize:
                start = total_received
                end = min(start + block_size - 1, filesize - 1)
                
                request = f"FILE {filename} GET START {start} END {end}"
                response = send_and_receive(data_sock, request, (server_host, data_port))
                
                if response is None:
                    print(f"[FAIL] No response for block {start}-{end}")
                    break
                
                # Extract Base64 encoded data
                if "DATA" not in response:
                    print("[ERROR] Malformed data response:", response)
                    break
                
                data_parts = response.split("DATA", 1)
                encoded_data = data_parts[1].strip()
                
                # Decode and write data to file
                raw_data = base64.b64decode(encoded_data)
                f.seek(start)
                f.write(raw_data)
                
                total_received += len(raw_data)
                print("*", end="", flush=True) 
                
                # After download, send FILE CLOSE
                close_request = f"FILE {filename} CLOSE"
                close_response = send_and_receive(data_sock, close_request, (server_host, data_port))
                
                if close_response and close_response.strip() == f"FILE {filename} CLOSE_OK":
                    print(f"\n[INFO] File {filename} closed successfully")
                else:
                    print(f"\n[WARN] CLOSE_OK not received for {filename}")
                                     
    else:
        print(f"[ERROR] Unexpected server response: {response}")
    
    sock.close()
    print(f"\n[INFO] Finished downloading {filename}")



if __name__ == "__main__":
    main()
