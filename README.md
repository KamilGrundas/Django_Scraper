# Django Scraper

A minimal article-scraping service.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (package & environment manager)

## Installation (with uv)

1. Install **uv**  
    **macOS/Linux**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ````

    **Windows (PowerShell)**

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

2. Clone the repository

    ```bash
    git clone https://github.com/KamilGrundas/Django_Scraper.git
    cd Django_Scraper
    ```

3. Create a virtual environment and install dependencies

    ```bash
    uv venv
    uv sync
    ```
