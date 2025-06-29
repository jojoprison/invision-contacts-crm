# invision-contacts-crm

Contacts service for SaaS-CRM with schema-based multi-tenancy.

⸻

🚀 Prerequisites
•	Python 3.11 installed (python3.11 in PATH)
•	Poetry (>= 2.1)
•	PostgreSQL 14+ (local or Docker)
•	Docker & Docker Compose (optional, for full-stack)

⸻

📦 Installation & Setup

# 1. Clone the repository
git clone https://github.com/jojoprison/invision-contacts-crm.git
cd invision-contacts-crm

# 2. Ensure Python 3.11 is available
python3.11 --version   # should output 3.11.x

# 3. Remove any existing venv and create a new one on 3.11
poetry env remove python  || true
poetry env use python3.11

# 4. Install dependencies (prod + dev)
poetry lock --no-update
poetry install --with dev
