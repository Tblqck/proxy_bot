import os
import time
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from gogle_Api_Interact import download_csv, upload_csv

# Constants
TEST_URL = "http://httpbin.org/get"
TIMEOUT = 7
MAX_WORKERS = 80

# Get real IP once at startup
def get_real_ip():
    try:
        r = requests.get(TEST_URL, timeout=5)
        return r.json().get("origin", "").split(",")[0].strip()
    except:
        return None

REAL_IP = get_real_ip()

# Main proxy tester
def enrich_and_verify_proxy(proxy):
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    result = {
        'proxy': proxy,
        'status_code': None,
        'latency_seconds': None,
        'leaks_ip': 'unknown',
        'anonymity': 'unknown',
        'can_access_google': False,
        'can_access_facebook': False,
        'can_access_amazon': False,
        'is_likely_bot': False,
        'is_potential_honeypot': False,
        'has_cloudflare': False,
        'error': None
    }

    try:
        start = time.time()
        r = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        latency = round(time.time() - start, 2)
        result['status_code'] = r.status_code
        result['latency_seconds'] = latency

        data = r.json()
        origin_ip = data.get("origin", "").split(",")[0].strip()
        headers = data.get("headers", {})

        # Leak detection
        if REAL_IP and (REAL_IP == origin_ip or REAL_IP in str(headers)):
            result['leaks_ip'] = 'yes'
            result['anonymity'] = 'transparent'
        elif any(h in headers for h in ['X-Forwarded-For', 'Forwarded', 'Via']):
            result['leaks_ip'] = 'no'
            result['anonymity'] = 'anonymous'
        else:
            result['leaks_ip'] = 'no'
            result['anonymity'] = 'elite'

        # Site access checks
        for site in ['google.com', 'facebook.com', 'amazon.com']:
            try:
                r2 = requests.get(f"https://{site}", proxies=proxies, timeout=5)
                result[f'can_access_{site.split(".")[0]}'] = r2.status_code < 400
                if 'cloudflare' in r2.headers.get('Server', '').lower():
                    result['has_cloudflare'] = True
            except:
                result[f'can_access_{site.split(".")[0]}'] = False

    except Exception as e:
        result['error'] = str(e)
        return None

    return result

# Main function
def run_live_proxy_enrichment():
    df = download_csv("liveproxy.csv")
    if df is None or df.empty:
        print("❌ liveproxy.csv not found or is empty.")
        return

    df['proxy'] = df['proxy'].astype(str)
    proxies = df['proxy'].dropna().unique().tolist()
    print(f"🔍 Checking {len(proxies)} proxies...")

    new_data = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(enrich_and_verify_proxy, proxy): proxy for proxy in proxies}
        for future in as_completed(futures):
            enriched = future.result()
            proxy = futures[future]
            if enriched:
                existing = df[df['proxy'] == proxy].iloc[0].to_dict()
                enriched['firstscanned'] = existing.get('firstscanned', pd.Timestamp.now())
                enriched['lastscanned'] = pd.Timestamp.now()
                enriched['country'] = existing.get('country', 'unknown')
                enriched['city'] = existing.get('city', 'unknown')
                enriched['protocol'] = existing.get('protocol', 'http')
                enriched['speed'] = f"{enriched['latency_seconds']}s"
                new_data.append(enriched)
                print(f"✅ {proxy} OK ({enriched['latency_seconds']}s)")
            else:
                print(f"❌ {proxy} DEAD")

    if new_data:
        cleaned_df = pd.DataFrame(new_data)
        upload_csv(cleaned_df, "liveproxy.csv")
        upload_csv(cleaned_df, "proxydata.csv")
        print(f"✅ Updated liveproxy.csv and proxydata.csv with {len(new_data)} good proxies.")
    else:
        print("⚠️ No working proxies found!")

    # Final integrity check
    final_live = download_csv("liveproxy.csv")
    final_data = download_csv("proxydata.csv")
    if set(final_live['proxy']) == set(final_data['proxy']):
        print("🔁 Integrity check passed: liveproxy.csv matches proxydata.csv")
    else:
        print("❌ Integrity check failed: mismatch between liveproxy and proxydata")

if __name__ == "__main__":
    run_live_proxy_enrichment()
