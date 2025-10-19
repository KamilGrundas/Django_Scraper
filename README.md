# Django Scraper

A minimal article-scraping service.

## Requirements

- Python 3.12+
- Git
- (optional) Docker + Docker Compose

## Installation

### Option 1 (Docker Compose)

1. **Clone the repository**

   ```bash
   git clone https://github.com/KamilGrundas/Django_Scraper.git
   cd Django_Scraper
   ```
2. **Run the entire stack**
    ```bash
    docker compose up --build
    ```

3. **Access the Django container**
    ```bash
    docker compose exec backend bash
    ```
4. **Run management commands inside the container**
    
    Scrape predefined articles:
    ```bash
    python manage.py scrape_articles
    ```
    or
    ```bash
    python manage.py scrape_articles --url "article url"
    ```

### Option 2 - Local env (venv / uv)


1. Clone the repository

    ```bash
    git clone https://github.com/KamilGrundas/Django_Scraper.git
    cd Django_Scraper
    ```

2. **Configure environment**

   Edit a `.env` file in the project root:

   ```dotenv
   POSTGRES_SERVER=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=articles_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   ```

   If you prefer Postgres in Docker (recommended locally):

   ```bash
   docker compose up -d db
   ```

   *This will create and run the PostgreSQL database container.*

---

#### 2A) Using **venv**

3. **Create & activate venv**

   ```bash
   python -m venv .venv
   ```

   **Linux/macOS:**
   ```bash
   source .venv/bin/activate
   ```
   **Windows:**
   ```bash
   .venv\Scripts\activate
   ```

4. **Install deps**

   ```bash
   pip install -r requirements.txt
   playwright install --with-deps chromium
   ```

5. **Migrate, scrape, run**

   ```bash
   python manage.py migrate
   python manage.py scrape_articles
   python manage.py runserver
   ```


#### 2B) Using **uv**

3. Install **uv**

    **macOS/Linux**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ````

    **Windows (PowerShell)**

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

4. **Create a virtual environment and install dependencies**

    ```bash
    uv venv
    uv sync
    uv run playwright install --with-deps chromium
    ```


5. **Migrate, scrape, run**

   ```bash
   uv run manage.py migrate
   uv run manage.py scrape_articles
   uv run manage.py runserver
   ```
---



