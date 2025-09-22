# cli.py
import requests
import os

METADATA_SERVER = "http://localhost:8000"

def upload_file(file_path):
    file_name = os.path.basename(file_path)
    r = requests.post(f"{METADATA_SERVER}/files/{file_name}/blocks", params={"replicas": 2})
    block_info = r.json()["block"]
    block_id = block_info["block_id"]
    datanodes = block_info["datanodes"]

    with open(file_path, "rb") as f:
        content = f.read()

    for dn_id in datanodes:
        dn_list = requests.get(f"{METADATA_SERVER}/datanodes").json()
        dn = next(x for x in dn_list if x["id"] == dn_id)
        url = f"http://{dn['host']}:{dn['port']}/store/{block_id}"
        files = {"file": (file_name, content)}
        requests.post(url, files=files)
    print(f"Uploaded {file_name} as block {block_id} to {len(datanodes)} datanodes.")

def download_file(file_name, save_path):
    r = requests.get(f"{METADATA_SERVER}/files/{file_name}/blocks")
    blocks = r.json()
    full_content = b""
    for blk in blocks:
        for dn_id in blk["datanodes"]:
            dn_list = requests.get(f"{METADATA_SERVER}/datanodes").json()
            dn = next(x for x in dn_list if x["id"] == dn_id)
            url = f"http://{dn['host']}:{dn['port']}/retrieve/{blk['block_id']}"
            r2 = requests.get(url)
            if r2.json()["status"] == "ok":
                full_content += bytes.fromhex(r2.json()["content"])
                break
    with open(save_path, "wb") as f:
        f.write(full_content)
    print(f"Downloaded {file_name} to {save_path}")

if __name__ == "__main__":
    while True:
        cmd = input("Command (upload/download/exit): ")
        if cmd.startswith("upload"):
            _, path = cmd.split()
            upload_file(path)
        elif cmd.startswith("download"):
            _, fname, save = cmd.split()
            download_file(fname, save)
        elif cmd == "exit":
            break
        else:
            print("Invalid command")
