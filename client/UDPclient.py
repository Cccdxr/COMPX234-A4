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

if __name__ == "__main__":
    main()
