# Distributed-File-System
A lightweight Distributed File System (mini-HDFS) built with Python, FastAPI, and Docker. Supports file chunking, replication, fault tolerance, and CLI-based file operations.
# Distributed File System (mini-HDFS)

A lightweight **Distributed File System** inspired by Hadoop HDFS, implemented in **Python, FastAPI, and Docker**.  
This project demonstrates core distributed systems concepts like **file chunking, replication, fault tolerance, metadata management, and resilient data access**.

## Features
-  **File Storage** – Splits large files into fixed-size chunks for distributed storage  
-  **Replication** – Stores multiple replicas of each chunk across DataNodes for fault tolerance  
-  **Metadata Server (NameNode)** – Tracks file-to-chunk mapping and DataNode locations  
-  **DataNodes** – Handle chunk storage, replication, checksums, and health heartbeats  
-  **Client CLI Tool** – Supports file upload (`put`), download (`get`), and listing (`ls`)  
-  **Data Integrity** – Ensures correctness with checksums  
-  **Dockerized Cluster** – Easily spin up a distributed environment with Docker Compose  

## What does this project do?
This project is a **scalable, fault-tolerant file storage system** that:  
- Splits large files into smaller **chunks**  
- Stores these chunks across multiple **DataNodes**  
- Maintains a **Metadata Server** (NameNode) to track where chunks are located  
- **Replicates chunks** to ensure availability even if a node fails  
- Provides a **CLI tool** to upload, download, and list files seamlessly

## Install dependencies
- python -m venv .venv
- source .venv/bin/activate   # Windows: .venv\Scripts\activate
- pip install -r requirements.txt

## Run with Docker Compose
- docker compose up --build

## Use the CLI
- Upload a file
- python client/cli.py put sample.txt /foo.txt --meta http://localhost:8000

## Download a file
- python client/cli.py get /foo.txt downloaded.txt --meta http://localhost:8000

## Future Enhancements
- Automated re-replication on node failure
- Performance monitoring dashboard
- Rebalancer to distribute chunks evenly
