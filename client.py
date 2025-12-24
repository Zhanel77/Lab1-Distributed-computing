import json, socket, uuid, time, sys

SERVER_IP = sys.argv[1]
PORT = 5000
TIMEOUT = 2
RETRIES = 3

def call(method, params):
    rid = str(uuid.uuid4())
    req = {"request_id": rid, "method": method, "params": params, "timestamp": time.time()}
    payload = (json.dumps(req) + "\n").encode()

    for attempt in range(1, RETRIES + 1):
        try:
            print(f"[CLIENT] attempt {attempt}/{RETRIES}, rid={rid}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(TIMEOUT)
                s.connect((SERVER_IP, PORT))
                s.sendall(payload)

                resp_line = b""
                while not resp_line.endswith(b"\n"):
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    resp_line += chunk

            return json.loads(resp_line.decode())

        except socket.timeout:
            print("[CLIENT] timeout -> retry")
        except Exception as e:
            print("[CLIENT] error:", e)

    return {"request_id": rid, "status": "ERROR", "error": "Timeout after retries"}

print(call("add", {"a": 5, "b": 7}))
print(call("reverse_string", {"s": "hello"}))
print(call("get_time", {}))
