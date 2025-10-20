import time
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from gogle_Api_Interact import download_csv, upload_csv

TEST_URL = "http://httpbin.org/ip"
TIMEOUT = 7
MAX_WORKERS = 80


def test_proxy(proxy):
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        start = time.time()
        r = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        latency = round(time.time() - start, 2)
        if r.status_code == 200:
            ip = r.json().get("origin", proxy.split(":")[0])
            return proxy, True, latency, ip
    except:
        pass
    return proxy, False, None, None


def get_geo_info(ip):
    try:
        r = requests.get(f"http://ipinfo.io/{ip}/json", timeout=5)
        data = r.json()
        return data.get("country", "unknown"), data.get("city", "unknown")
    except:
        return "unknown", "unknown"


def run_proxy_tester():
    df = download_csv("proxy.csv")
    if df is None or df.empty:
        print("❌ No proxies to test.")
        return

    proxies = df["proxy"].astype(str).tolist()
    tested, working = [], []

    print(f"🧪 Testing {len(proxies)} proxies...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(test_proxy, p): p for p in proxies}
        for f in as_completed(futures):
            p, ok, latency, ip = f.result()
            tested.append({"proxy": p, "is_working": ok, "latency": latency})
            if ok:
                c, city = get_geo_info(ip)
                working.append({
                    "proxy": p,
                    "country": c,
                    "city": city,
                    "protocol": "http",
                    "speed": f"{latency}s",
                    "firstscanned": pd.Timestamp.now(),
                    "lastscanned": pd.Timestamp.now(),
                })
                print(f"✅ {p} {c}-{city} {latency}s")
            else:
                print(f"❌ {p}")

    upload_csv(pd.DataFrame(tested), "archive.csv")
    upload_csv(pd.DataFrame(working), "liveproxy.csv")
    upload_csv(pd.DataFrame(columns=["proxy"]), "proxy.csv")
    print("📤 Uploads complete.")
