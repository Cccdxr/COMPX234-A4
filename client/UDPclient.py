import socket
import sys
import os

def main():
    # 检查参数
    if len(sys.argv) != 4:
        print("Usage: python UDPclient.py <server_host> <port> <filelist.txt>")
        sys.exit(1)
        
    server_host = sys.argv[1]
    port = int(sys.argv[2])
    filelist_path = sys.argv[3]
    
    # 检查文件列表文件是否存在
    if not os.path.exists(filelist_path):
        print("[ERROR] filelist.txt not found")
        sys.exit(1)
        
    # 读取文件列表并打印
    with open(filelist_path, "r") as filelist:
        for line in filelist:
            filename = line.strip()
            if filename:
                print(f"[INFO] Need to download: {filename}")
                
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
            timeout *= 2  # 指数退避
    print("[FAIL] No response after maximum retries.", flush=True)
    return None


if __name__ == "__main__":
    main()
