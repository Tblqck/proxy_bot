import time
import requests
import pandas as pd
from gogle_Api_Interact import download_csv, upload_csv

proxy_sources = [
    ("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=1000", "Proxyscrape"),
    ("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", "TheSpeedX"),
    ("https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt", "Clarketm"),
    ("https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt", "ShiftyTR"),
    ("https://raw.githubusercontent.com/Mertguvencli/http-proxy-list/main/proxy-list/data.txt", "Mertguvencli"),
    ("https://raw.githubusercontent.com/UserR3X/proxy-list/main/http.txt", "UserR3X"),
    ("https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt", "HideMyName"),
    ("https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt", "Jetkai"),
    ("https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt", "mmpx12"),
    ("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt", "monosans"),
    ("https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt", "sunny9577"),
    ("https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt", "hendrikbgr"),
    ("https://raw.githubusercontent.com/casals-ar/proxy-list/main/proxies.txt", "casals-ar"),
    ("https://raw.githubusercontent.com/tahaluindo/Proxy/main/http.txt", "tahaluindo"),
    ("https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt", "Zaeem20"),
    ("https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt", "roosterkid"),
    ("https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt", "opsxcq"),
    ("https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt", "HyperBeats"),
    ("https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt", "zevtyardt"),
]


def fetch_from_url(url, name):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return [p.strip() for p in r.text.split("\n") if ":" in p]
    except Exception as e:
        print(f"❌ {name}: {e}")
    return []


def run_proxy_collector():
    all_proxies = []
    for url, name in proxy_sources:
        time.sleep(0.5)
        all_proxies += fetch_from_url(url, name)

    unique_proxies = sorted(set(all_proxies))
    print(f"✅ Collected {len(unique_proxies)} proxies.")

    archive_df = download_csv("archive.csv") or pd.DataFrame(columns=["proxy"])
    archived = set(archive_df["proxy"].astype(str))
    new = [p for p in unique_proxies if p not in archived]

    print(f"🆕 {len(new)} new proxies found.")
    if new:
        upload_csv(pd.DataFrame(new, columns=["proxy"]), "proxy.csv")
