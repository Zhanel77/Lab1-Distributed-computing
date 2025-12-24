import json, socket, time, os
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000
DELAY_SEC = float(os.getenv("RPC_DELAY_SEC", "0"))

def add(params):
    return params["a"] + params["b"]

def get_time(params):
    return datetime.utcnow().isoformat() + "Z"

def reverse_string(params):
    return params["s"][::-1]

METHODS = {
    "add": add,
    "get_time": get_time,
    "reverse_string": reverse_string
}

def handle(req):
    rid = req.get("request_id")
    method = req.get("method")
    params = req.get("params", {})

    if DELAY_SEC > 0:
        time.sleep(DELAY_SEC)

    if method not in METHODS:
        return {"request_id": rid, "status": "ERROR", "error": "Unknown method"}

    try:
        result = METHODS[method](params)
        return {"request_id": rid, "status": "OK", "result": result}
    except Exception as e:
        return {"request_id": rid, "status": "ERROR", "error": str(e)}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(20)
    print(f"[SERVER] listening on {HOST}:{PORT}, delay={DELAY_SEC}s")

    while True:
        conn, addr = s.accept()
        with conn:
            buf = b""
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                buf += data
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    if not line.strip():
                        continue
                    req = json.loads(line.decode())
                    print("[SERVER] req:", req)
                    resp = handle(req)
                    conn.sendall((json.dumps(resp) + "\n").encode())
                    print("[SERVER] resp:", resp)
