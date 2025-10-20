# ------------------ MAIN PIPELINE RUNNER ------------------
import time
from proxy_collector import run_proxy_collector
from test_and_upload_proxies import run_proxy_tester
from proxy_checker_sync import run_live_proxy_enrichment

def main():
    print("\n🚀 STARTING PROXY DATA PIPELINE\n")
    run_proxy_collector()
    time.sleep(2)

    run_proxy_tester()
    time.sleep(2)

    run_live_proxy_enrichment()
    print("\n✅ PIPELINE COMPLETE.\n")

if __name__ == "__main__":
    main()
