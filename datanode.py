# datanode.py
import requests
import threading
import os
from fastapi import FastAPI, UploadFile, File
import uvicorn
import uuid
import time

METADATA_SERVER = "http://localhost:8000"
DATA_DIR = "data"
PORT = 5001  # change for each datanode

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

app = FastAPI(title=f"DataNode on port {PORT}")

def register_datanode():
    node_info = {
        "id": str(uuid.uuid4()),
        "host": "localhost",
        "port": PORT
    }
    try:
        requests.post(f"{METADATA_SERVER}/datanodes", json=node_info)
        print(f"Registered DataNode {node_info['id']} with Metadata Server")
    except Exception as e:
        print("Error registering DataNode:", e)

@app.post("/store/{block_id}")
async def store_block(block_id: str, file: UploadFile = File(...)):
    path = os.path.join(DATA_DIR, block_id)
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"status": "stored", "block_id": block_id}

@app.get("/retrieve/{block_id}")
def retrieve_block(block_id: str):
    path = os.path.join(DATA_DIR, block_id)
    if not os.path.exists(path):
        return {"status": "error", "message": "block not found"}
    with open(path, "rb") as f:
        content = f.read()
    return {"status": "ok", "content": content.hex()}

if __name__ == "__main__":
    threading.Thread(target=register_datanode).start()
    uvicorn.run(app, host="0.0.0.0", port=PORT)
