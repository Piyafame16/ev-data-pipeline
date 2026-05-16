# 🚗 EV Data Pipeline: CSV → MySQL with Airflow + Docker

Pipeline สำหรับโหลดข้อมูล Electric Vehicle Market จาก Kaggle  
เข้า MySQL โดยใช้ Apache Airflow เป็น orchestrator และ Docker เป็น environment

> 📚: Project นี้ออกแบบมาเพื่อสอน Data Engineering pipeline ขั้นพื้นฐาน  
> ครอบคลุม Docker, Airflow DAG, ETL concepts และ Database connection

---

## 📋 สิ่งที่จะได้เรียนรู้

- **Docker & Docker Compose** — รัน multiple services พร้อมกัน
- **Apache Airflow** — จัดการ pipeline ด้วย DAG
- **ETL Pipeline** — Extract, Transform, Load
- **MySQL** — จัดเก็บข้อมูลใน relational database
- **Python** — pandas, SQLAlchemy

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Network (ev_net)                   │
│                                                                   │
│   ┌─────────────┐    ┌──────────────────────────────────────┐   │
│   │  PostgreSQL  │    │           Apache Airflow              │   │
│   │  (port 5432) │◄───│  ┌────────────┐  ┌───────────────┐  │   │
│   │  Airflow DB  │    │  │ Webserver  │  │   Scheduler   │  │   │
│   └─────────────┘    │  │ :8080      │  │  (runs DAGs)  │  │   │
│                       │  └────────────┘  └───────────────┘  │   │
│                       └──────────────────────┬───────────────┘   │
│                                              │ runs                │
│                                              ▼                    │
│   ┌─────────────┐    ┌──────────────────────────────────────┐   │
│   │    MySQL    │◄───│           ev_pipeline DAG             │   │
│   │  (port 3306)│    │                                       │   │
│   │   ev_db    │    │  validate_csv → clean_data → load     │   │
│   └─────────────┘    └──────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Pipeline Flow (DAG)

```
CSV File (Kaggle)
      │
      ▼
┌─────────────┐     ถ้าไฟล์ว่าง หรือ null เกิน 50%
│ validate_csv│──── ❌ FAIL → หยุดทันที (ไม่รัน task ถัดไป)
└──────┬──────┘
       │ ✅ ผ่าน
       ▼
┌─────────────┐
│  clean_data │  - แปลง column names → snake_case
│             │  - ลบ duplicate rows
└──────┬──────┘  - เติม null values
       │         - บันทึกเป็น ev_cleaned.csv
       ▼
┌──────────────┐
│ load_to_mysql│  - อ่าน ev_cleaned.csv
│              │  - เชื่อมต่อ MySQL
└──────────────┘  - load ข้อมูลเข้า table
                  - verify row count
```

---

## 📁 โครงสร้าง Project

```
ev-pipeline/
│
├── 📄 docker-compose.yml     # กำหนด services ทั้งหมด
├── 📄 .env                   # ตัวแปร password (ไม่ commit)
├── 📄 .env.example           # ตัวอย่าง .env
├── 📄 .gitignore
│
├── 📂 dags/
│   └── ev_pipeline_dag.py   # ตัว DAG หลัก (กำหนด flow)
│
├── 📂 tasks/
│   ├── validate.py          # Task 1: ตรวจสอบ CSV
│   ├── clean.py             # Task 2: ทำความสะอาด
│   └── load.py              # Task 3: Load เข้า MySQL
│
└── 📂 data/
    └── ev_dataset.csv       # วางไฟล์ CSV ที่นี่ (ไม่ commit)
```

---

## 🐳 Services ใน Docker Compose

| Service | Image | Port | หน้าที่ |
|---|---|---|---|
| `postgres` | postgres:15 | 5432 | เก็บ metadata ของ Airflow |
| `mysql` | mysql:8.0 | 3306 | เก็บข้อมูล EV (Data Warehouse) |
| `airflow-init` | airflow:2.9.1 | - | สร้าง user admin ครั้งแรก |
| `airflow-webserver` | airflow:2.9.1 | **8080** | UI สำหรับดู DAG |
| `airflow-scheduler` | airflow:2.9.1 | - | ตัวรัน DAG ตามเวลา |

---

## 🚀 วิธีรัน (Step by Step)

### 1. เตรียม Dataset
ดาวน์โหลดจาก Kaggle แล้ววางในโฟลเดอร์ `data/`
```
https://www.kaggle.com/datasets/patelris/electric-vehicle-market-and-pricing-dataset-2026
```

### 2. ตั้งค่า Environment Variables
```bash
cp .env.example .env
# แก้ไข password ตามต้องการใน .env
```

### 3. รัน Docker Compose
```bash
docker compose up --build -d
```

### 4. ตรวจสอบ Services
```bash
docker compose ps
# ทุก container ต้องมีสถานะ healthy
```

### 5. เปิด Airflow UI
```
http://localhost:8080
Username: admin
Password: admin
```

### 6. Trigger DAG
- ไปที่ DAG `ev_pipeline`
- กดปุ่ม ▶️ Trigger DAG
- ดู task แต่ละอันรันสำเร็จ ✅

### 7. ตรวจสอบข้อมูลใน MySQL
```bash
docker exec -it ev_mysql mysql -u ev_user -pev_pass ev_db

# ใน MySQL shell:
SHOW TABLES;
SELECT COUNT(*) FROM electric_vehicles;
SELECT * FROM electric_vehicles LIMIT 5;
```

---

