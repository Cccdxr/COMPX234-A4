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
            timeout *= 2  # 指数退避
    print("[FAIL] No response after maximum retries.", flush=True)
    return None

def download_file(server_host, port, filename):
    print(f"[INFO] Requesting file: {filename}", flush=True)

    # 创建 UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 构造并发送 DOWNLOAD 请求
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
        fsize = parts[3]
        data_port = parts[5]
        print(f"[OK] {fname} is available, size={fsize} bytes, data_port={data_port}")
        # 下一步我们将使用这些信息下载数据
    else:
        print(f"[ERROR] Unexpected server response: {response}")
    
    sock.close()



if __name__ == "__main__":
    main()
