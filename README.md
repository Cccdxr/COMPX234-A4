# COMPX234-A4

# COMPX234-A4: UDP Multithreaded File Transfer System

This project implements a reliable file transfer system using UDP sockets for COMPX234 Assignment 4. The system includes a multithreaded server and a client that requests and downloads one or more files from the server.

---

## Features

- UDP-based file transmission with reliable delivery
- Server supports multiple clients concurrently using threads
- Client downloads files using stop-and-wait (timeout + retry)
- File data transmitted using Base64 encoding
- Blocked file transfer: 1000-byte chunks
- Protocol uses simple text messages (e.g., DOWNLOAD, FILE GET START/END)
- Each file transfer uses a dynamically assigned port (50000–51000)
- Progress indicator prints `*` for each block received

---

## Files

- `server/UDPserver.py` — Server implementation
- `client/UDPclient.py` — Client implementation
- `client/files.txt` — List of filenames to request from the server
- `server/*.pdf / *.mov` — Test files available on the server
- `README.md` — This file

---

## Protocol

### Initial request:

- `DOWNLOAD filename`

### Server responses:

- `OK filename SIZE <size> PORT <port>`
- `ERR filename NOT_FOUND`
- `ERR MALFORMED_REQUEST`

### Data transfer:

- Client sends:
  - `FILE filename GET START <start> END <end>`
- Server responds:
  - `FILE filename OK START <start> END <end> DATA <base64_data>`

### End of transfer:

- Client sends:
  - `FILE filename CLOSE`
- Server responds:
  - `FILE filename CLOSE_OK`

---

## Usage

### Start the server

```bash
cd server
python UDPserver.py 51234
```

### Start the client

```bash
cd client
python UDPclient.py localhost 51234 files.txt
```

- `files.txt` should list one filename per line, matching files available on the server.

---

## Testing

### Basic steps

1. Place test files (e.g. `07.pdf`, `IM-NZ.mov`) into the `server/` folder
2. Create a `files.txt` in the `client/` folder with matching filenames
3. Start the server and then the client
4. Client downloads each file and prints `*` per chunk

### Integrity verification

Use MD5 to check that downloaded files match originals:

#### On Windows (PowerShell):

```powershell
CertUtil -hashfile 07.pdf MD5
CertUtil -hashfile ..\server\07.pdf MD5
```

#### On Linux/macOS:

```bash
md5sum 07.pdf ../server/07.pdf
```

---

## Server Threads

- Each client is assigned a random port in the range 50000–51000
- A separate thread is started for each file download
- Threads handle one file transfer per client independently

---

## Reliability Features

- Stop-and-wait retransmission with timeout (starts at 1s, doubles each retry)
- Maximum 5 retries per message
- Handles malformed requests and client disconnects

---

## Requirements

- Python 3.10 or above
- No external dependencies
- Works on Windows, Linux, macOS

---




