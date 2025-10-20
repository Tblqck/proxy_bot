
## 🛰️ Proxy Data Pipeline & Telegram Bot

### Overview

This project is a **fully automated proxy data pipeline** that continuously:

1. 🕷️ **Scrapes** fresh public proxies from multiple trusted sources.
2. ⚙️ **Tests** and filters proxies for validity, speed, and uptime.
3. 🌍 **Enriches** each working proxy with **geolocation and anonymity data**.
4. ☁️ **Uploads results** (live proxies, tested archives, and metadata) to **Google Drive** for remote access.
5. 🤖 **Provides a Telegram Bot interface** for users to instantly fetch the latest working proxies.

All components are modular and can run independently or as part of the full pipeline.

---

### 🧩 Tech Stack

| Component          | Technology                                                |
| ------------------ | --------------------------------------------------------- |
| Core Language      | **Python 3.10+**                                          |
| API & Data         | **Requests**, **Pandas**, **Google Drive API (v3)**       |
| Async Execution    | **ThreadPoolExecutor** for high-performance proxy testing |
| Telegram Interface | **python-telegram-bot v21+**                              |
| Hosting Options    | Works locally, on **Colab**, or a lightweight VPS         |
| Cloud Sync         | **Google Drive (Service Account)**                        |

---

### 🔄 Pipeline Workflow

1. **`proxy_collector.py`**

   * Aggregates free proxies from 15+ online sources.
   * Removes duplicates and uploads a clean list to `proxy.csv` on Drive.

2. **`test_and_upload_proxies.py`**

   * Tests each proxy for connectivity and latency.
   * Uploads results to `liveproxy.csv` and archives all tested proxies.

3. **`proxy_checker_sync.py`**

   * Enriches working proxies with:

     * 🌍 Country & City
     * 🔒 Anonymity Level
     * ⚡ Speed
     * 🌐 Access to major sites (Google, Facebook, Amazon)
     * ☁️ Cloudflare detection
   * Updates both `liveproxy.csv` and `proxydata.csv` for full analytics.

4. **`proxy_bot.py`**

   * Telegram bot that lets users type commands like:

     ```
     give live proxies
     show working proxies
     send tested ones
     ```
   * Fetches the latest `liveproxy.csv` directly from Drive and sends it as a downloadable file.

5. **`main_pipeline.py`**

   * Runs all stages sequentially:

     ```
     Collector → Tester → Enricher
     ```
   * Ensures a clean and complete update cycle.

---

### 🚀 Quick Start (Local Run)

#### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

#### 2️⃣ Set up Google Drive access

* Create a Google Cloud project and enable the **Drive API**.
* Download your **service account JSON file**.
* Place it in the project root and update these constants in `gogle_Api_Interact.py`:

  ```python
  SERVICE_ACCOUNT_FILE = 'your_service_account.json'
  FOLDER_ID = 'your_drive_folder_id'
  ```

#### 3️⃣ Set up Telegram Bot

* Create a new bot via [@BotFather](https://t.me/BotFather).
* Copy your bot token into `config.py`:

  ```python
  TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
  ```

#### 4️⃣ Run the full pipeline

```bash
python main_pipeline.py
```

#### 5️⃣ Start the Telegram bot

```bash
python proxy_bot.py
```

---

### 🧪 Try the Demo

A limited demo of the bot is available on Telegram:
👉 **[@StreamProxyBots](https://t.me/StreamProxyBots)**

> ⚠️ Please note: The public bot uses a **“dud” config** (no live Drive credentials).
> It exists for demonstration purposes only — feel free to message it and test commands.
> To set up your own fully functional version, follow the steps above.

---

### 🧰 Folder Structure

```
proxy_bot/
│
├── proxy_collector.py          # Collects proxies from sources
├── test_and_upload_proxies.py  # Tests proxies and uploads results
├── proxy_checker_sync.py       # Enriches live proxies with metadata
├── proxy_bot.py                # Telegram interface
├── gogle_Api_Interact.py       # Handles Google Drive read/write
├── main_pipeline.py            # Runs the full pipeline sequence
├── config.py                   # Stores API keys and tokens (excluded from repo)
├── requirements.txt            # All dependencies
└── README.md                   # You’re here
```

---

### 🛡️ Security Notice

Sensitive keys and credentials such as:

* `proxydatacollector-a0c74abdcd83.json`
* `TELEGRAM_TOKEN`
* `FOLDER_ID`

have been **intentionally redacted** from this repository for security reasons.
Users are encouraged to **create their own config** by following the setup guide or requesting help.

---

### 🧠 Features Summary

* ✅ Fully modular pipeline (collector, tester, enricher, bot)
* 🌍 Geolocation + anonymity detection
* ⚡ Latency & uptime tracking
* 🤖 Telegram proxy fetch interface
* ☁️ Google Drive integration (cloud data sync)
* 🔁 Integrity verification between Drive files
* 🧩 Easy customization and redeployment

---

### 🧑‍💻 Author

**T Black (Abasiekeme Hanson)**
Data Analyst & Systems Builder
💬 [Telegram Demo Bot → @StreamProxyBots](https://t.me/StreamProxyBots)

