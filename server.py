import json
import socket
import time
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

# --- Remote methods ---
def add(a, b):
    return a + b

def echo(message):
    return message

METHODS = {
    "add": add,
    "echo": echo,
}

def log(msg: str):
    print(f"[{datetime.utcnow().isoformat()}Z] {msg}", flush=True)

def handle_request(raw: str) -> dict:
    try:
        req = json.loads(raw)
        request_id = req.get("request_id")
        method = req.get("method")
        params = req.get("params", {})

        log(f"REQ id={request_id} method={method} params={params}")

        if method not in METHODS:
            return {"request_id": request_id, "result": None, "status": "ERROR", "error": "Unknown method"}

        # params can be dict or list
        if isinstance(params, dict):
            result = METHODS[method](**params)
        elif isinstance(params, list):
            result = METHODS[method](*params)
        else:
            return {"request_id": request_id, "result": None, "status": "ERROR", "error": "Invalid params type"}

        return {"request_id": request_id, "result": result, "status": "OK"}

    except Exception as e:
        return {"request_id": None, "result": None, "status": "ERROR", "error": str(e)}

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        log(f"RPC Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                log(f"Connected: {addr}")
                data = conn.recv(4096)
                if not data:
                    continue
                raw = data.decode("utf-8", errors="replace")

                resp = handle_request(raw)
                conn.sendall(json.dumps(resp).encode("utf-8"))

                log(f"RESP to id={resp.get('request_id')} status={resp.get('status')} result={resp.get('result')}")

if __name__ == "__main__":
    main()
