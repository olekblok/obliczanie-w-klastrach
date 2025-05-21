
```markdown
# 📈 ETF to HBase Uploader

This project reads ETF data from CSV `.txt` files in a folder and uploads it into an HBase database running in Docker. It uses Python and the `happybase` library to interact with HBase via Thrift.

---

## 🗂️ Folder Structure

```

.

├── ETFs/

│   ├── xle.us.txt

│   ├── acwi.us.txt

│   └── ... (other ETF files)

├── upload_etfs_to_hbase.py

├── requirements.txt

├── Dockerfile

├── docker-compose.yml

└── README.md

```

---

## 🚀 Getting Started

### 1. Start Docker Services

Run this to build and start the entire system (HBase + uploader):

```bash
docker-compose up --build
```

This will:

* Start HBase master, region server, and ZooKeeper
* Build the uploader Python script into a Docker container
* Automatically run the upload to HBase

### 2. View Logs

You can monitor logs from the uploader with:

```bash
docker-compose logs -f uploader
```

### 3. Access HBase Web UI

Visit: [http://localhost:16010](http://localhost:16010)

---

## 📄 ETF Data Format

Each file in the `ETFs/` folder should be a `.txt` CSV file named like the ETF it represents (e.g. `xle.us.txt`), with contents formatted like:

```csv
Date,Open,High,Low,Close,Volume,OpenInt
2020-01-02,61.50,62.80,61.20,62.45,123456,0
```

Each line is uploaded to HBase under the row key:

```
<etf_name>_<date>
```

e.g.:

```
xle.us_2020-01-02
```

---

## 🧠 How It Works

* Python script connects to HBase via Thrift (`port 9090`)
* Ensures the table `etfs` with column family `data` exists
* Reads all `.txt` files from `ETFs/`
* For each file, inserts every row into HBase under the proper row key

---

## ⚙️ Configuration

* Table name: `etfs`
* Column family: `data`
* Thrift host: `hbase-thrift` (Docker service name)
* Port: `9090`

---

## 🐍 Python Requirements

If running the script locally (not in Docker):

```bash
pip install -r requirements.txt
```

---

## 🧹 Cleanup Commands

Stop and remove containers:

```bash
docker-compose down -v
```

Remove all Docker images (⚠️ all images on your system):

```bash
docker rmi -f $(docker images -q)
```

---

## 📄 License

MIT License — free to use, modify, and distribute.
