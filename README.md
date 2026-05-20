# Hybrid Data Platform

A production-style hybrid data platform combining realtime streaming and batch ELT pipelines using modern open-source tools.

---

Architecture

```text
REALTIME PIPELINE
CoinLore Crypto API
        ↓
   Apache NiFi
   (every 30 seconds)
        ↓
ClickHouse Bronze Layer

BATCH PIPELINE
Ecommerce CSV Dataset
        ↓
  Apache Airflow
  (scheduled daily)
        ↓
ClickHouse Bronze Layer

TRANSFORMATION LAYER
     Bronze
       ↓
     Silver  ← dbt cleans and types data
       ↓
      Gold   ← dbt produces business insights
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Docker Compose | Infrastructure orchestration |
| Apache NiFi | Realtime streaming ingestion |
| Apache Airflow | Batch pipeline orchestration |
| ClickHouse | Analytical data warehouse |
| dbt | Data transformation layer |
| Python | DAG scripting |
| Git | Version control |

---

## Project Structure

```text
hybrid-data-platform/
│
├── airflow/
│   └── dags/
│       └── ecommerce_batch_ingestion.py
│
├── clickhouse/
│   └── init/
│       └── init.sql
│
├── data/
│   └── raw/
│       └── ecommerce_data.csv
│
├── hybrid_platform/          ← dbt project
│   └── models/
│       ├── silver/
│       │   ├── silver_crypto_prices.sql
│       │   └── silver_ecommerce_orders.sql
│       └── gold/
│           ├── gold_crypto_summary.sql
│           └── gold_ecommerce_summary.sql
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Medallion Architecture

| Layer | Description | Tables |
|---|---|---|
| Bronze | Raw ingestion — no transformations | crypto_prices, ecommerce_orders_raw |
| Silver | Cleaned, typed, validated data | silver_crypto_prices, silver_ecommerce_orders |
| Gold | Business-ready analytics models | gold_crypto_summary, gold_ecommerce_summary |

---

## Services

| Service | Port | Purpose |
|---|---|---|
| Apache NiFi | 8443 | Realtime ingestion canvas |
| Apache Airflow | 8080 | DAG orchestration UI |
| ClickHouse | 8123, 9000 | Analytical warehouse |
| PostgreSQL | 5432 | Airflow metadata database |
| Redis | 6379 | Airflow backend |

---

## Realtime Pipeline

- Source: CoinLore Crypto API
- Ingestion: Apache NiFi polls every 30 seconds
- Extracts: BTC symbol, price, market cap, volume
- Destination: ClickHouse Bronze layer
- Transformation: dbt Silver and Gold models

---

## Batch Pipeline

- Source: Ecommerce CSV dataset (3,066 rows)
- Ingestion: Apache Airflow DAG runs daily
- Destination: ClickHouse Bronze layer
- Transformation: dbt Silver and Gold models

---

## Sample Analytics Output

### Gold — Crypto Summary
| Symbol | Avg Price | Max Price | Min Price | Records |
|---|---|---|---|---|
| BTC | 76,336 | 76,418 | 76,318 | 16 |

### Gold — Ecommerce Sales by Country
| Country | Orders | Total Sales | Avg Order |
|---|---|---|---|
| United Kingdom | 2894 | £54,593 | £18.86 |
| Norway | 73 | £1,919 | £26.29 |
| France | 20 | £855 | £42.79 |

---

## How to Run

### Prerequisites
- Docker Desktop
- Python 3.12+
- Git

### Start Infrastructure
```bash
docker compose up -d
```

### Verify Services
```bash
docker ps
```

### Run dbt Transformations
```bash
cd hybrid_platform
python -m venv venv
venv\Scripts\activate
pip install dbt-core dbt-clickhouse
dbt run
```

### Query Analytics
```bash
docker exec -it clickhouse clickhouse-client --user admin --password admin123 --query "SELECT * FROM silver_gold.gold_ecommerce_summary LIMIT 10"
```

---

## Key Learnings

- Realtime streaming ingestion with Apache NiFi
- Batch pipeline orchestration with Apache Airflow
- Columnar warehouse design with ClickHouse
- Medallion Architecture (Bronze/Silver/Gold)
- Analytics engineering with dbt
- Dockerized infrastructure with Docker Compose
- ELT pipeline design patterns

---

## Author

**ImeMonday**
GitHub: https://github.com/ImeMonday/hybrid-data-platform