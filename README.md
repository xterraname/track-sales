# Track Sales
## Project setup
Copy .env
```bash
cp .env.example .env
```
Create and activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Install the required dependencies
```bash
pip install -r requirements.txt
```
Migrate Database
```bash
make migrate
```
Create superuser
```bash
make superuser
```
## Load data
### Run script
Load clients, employees and products
```bash
python3 scripts/load_data.py

----------------------
 1. Load from csv
 2. Load to database
 3. Create random orders
----------------------
Enter command:2
```
Create a random orders (x200)
```bash
python3 scripts/load_data.py

----------------------
 1. Load from csv
 2. Load to database
 3. Create random orders
----------------------
Enter command:3
Number of orders to create: 200
```

## Usage
### Run
```bash
make run-server
```
- Admin: http://localhost:8000/admin
- Swagger: http://localhost:8000/api/schema/swagger-ui/
## Docker
### Run
```bash
docker compose up -d
```
### Create superuser
```bash
docker exec -it track_sales-app-1 make superuser
```
### Run script on Docker
```bash
docker exec -it track_sales-app-1 python3 scripts/load_data.py
```
### Rebuild
```bash
docker compose up -d --build app
```
