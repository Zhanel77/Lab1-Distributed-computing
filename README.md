# Lab1-Distributed-computing
# Lab 1 — Remote Procedure Call (RPC) Implementation on AWS EC2

## Overview
This project implements a simple Remote Procedure Call (RPC) system using **Python** and **TCP sockets**.  
The system consists of two nodes deployed on **AWS EC2**:

- **Server node** (`rpc-server-node`)
- **Client node** (`rpc-client-node`)

The client sends RPC requests to the server using a custom JSON-based protocol.  
The server executes the requested function and returns the result.

The project also demonstrates **failure handling**, including **timeouts and retry logic**, and evaluates **RPC semantics**.

---

## Technologies Used
- Python 3
- TCP sockets
- JSON serialization
- AWS EC2 (Ubuntu 22.04)

---

## Project Structure
```yaml
.
├── server.py # RPC server
├── client.py # RPC client
└── README.md

```
---

## RPC Message Format
Requests are sent in JSON format:

```json
{
  "request_id": "uuid",
  "method": "add",
  "params": { "a": 5, "b": 7 },
  "timestamp": 1734870000.0
}
```
Responses from the server:

```json
{
  "request_id": "uuid",
  "status": "OK",
  "result": 12
}
```
## Setup Instructions
1. Create EC2 Instances
Launch two EC2 instances with Ubuntu 22.04

Name them:
- rpc-server-node
- rpc-client-node
- Instance type: t2.micro or t3.micro

Open TCP port 5000 in the Security Group inbound rules

2. Install Dependencies (on both server and client)
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```
3. Test Network Connectivity (from client)
```bash
ping <SERVER_PUBLIC_IP>
nc -vz <SERVER_PUBLIC_IP> 5000
```
Running the Application
1. Start the Server (on rpc-server-node)
```bash
python3 server.py
```
Expected output:

```csharp
[SERVER] listening on 0.0.0.0:5000
```
2. Run the Client (on rpc-client-node)
```bash
python3 client.py <SERVER_PUBLIC_IP>
```
Example:
```bash
python3 client.py 13.222.2.127
```
The client sends multiple RPC requests:
- add(a, b)
- reverse_string(s)
- get_time()
- 
## Failure Handling Demonstration
To demonstrate failure handling, the server is intentionally slowed down.
Start the server with artificial delay:
```bash
RPC_DELAY_SEC=5 python3 server.py
```
The client timeout is set to 2 seconds, with 3 retries.
Observed behavior:
- The client does not receive a response in time
- The request is retried multiple times

After all retries, the client returns:
```makefile
ERROR: Timeout after retries
```
## RPC Semantics
This implementation demonstrates at-least-once RPC semantics.
Because the client retries requests after a timeout, the same RPC request may be executed multiple times on the server.
To achieve at-most-once semantics, the server would need to store processed request IDs and return cached responses for duplicate requests.

