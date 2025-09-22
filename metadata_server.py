# metadata_server.py
"""
Mini-HDFS Metadata Server (FastAPI)
- Register DataNodes
- List DataNodes
- Simple file-to-block metadata storage (in-memory)
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List ,Optional
import uvicorn
import uuid
import time

app = FastAPI(title="Mini-HDFS Metadata Server")

class DataNodeInfo(BaseModel):
    id: str
    host: str
    port: int
    last_seen: Optional[float] = None

class FileBlock(BaseModel):
    file_name: str
    block_id: str
    datanodes: List[str]

datanodes: Dict[str, DataNodeInfo] = {}
file_blocks: Dict[str, List[FileBlock]] = {}

@app.post("/datanodes", status_code=201)
def register_datanode(node: DataNodeInfo):
    node.last_seen = time.time()
    datanodes[node.id] = node
    return {"message": "registered", "node": node}

@app.get("/datanodes", response_model=List[DataNodeInfo])
def list_datanodes():
    return list(datanodes.values())

@app.post("/files/{file_name}/blocks", status_code=201)
def create_file_block(file_name: str, replicas: int = 2):
    # create a block id and assign to first `replicas` datanodes
    if len(datanodes) == 0:
        raise HTTPException(400, "No datanodes registered")
    dn_ids = list(datanodes.keys())[:replicas]
    block = FileBlock(file_name=file_name, block_id=str(uuid.uuid4()), datanodes=dn_ids)
    file_blocks.setdefault(file_name, []).append(block)
    return {"block": block}

@app.get("/files/{file_name}/blocks", response_model=List[FileBlock])
def list_file_blocks(file_name: str):
    return file_blocks.get(file_name, [])

@app.get("/health")
def health():
    return {"status":"ok", "datanode_count": len(datanodes)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
