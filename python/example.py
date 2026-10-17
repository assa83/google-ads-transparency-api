"""Daily monitor: print only the ads a competitor launched since the last run.

Usage: python example.py hellofresh.com --region US
"""
import argparse
import os
import re
import sys

from apify_client import ApifyClient

ACTOR = "lagenuina_agency/google-ads-transparency-scraper"
TOKEN = os.environ.get("APIFY_TOKEN")
if not TOKEN:
    sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("competitor", help="brand name or domain, e.g. hellofresh.com")
    p.add_argument("--region", default="US")
    a = p.parse_args()

    # One memory per competitor, so monitors do not mix their "already seen" lists.
    store = "ads-monitor-" + re.sub(r"[^a-z0-9-]+", "-", a.competitor.lower()).strip("-")
    client = ApifyClient(TOKEN)
    run = client.actor(ACTOR).call(run_input={
        "queries": [a.competitor],
        "region": a.region,
        "maxAdsPerSearch": 200,
        "onlyNewAds": True,
        "monitorStoreName": store,
    })
    ads = client.dataset(run["defaultDatasetId"]).list_items().items
    if not ads:
        print(f"No new ads for {a.competitor}.")
        return
    print(f"{len(ads)} new ads for {a.competitor}:")
    for ad in sorted(ads, key=lambda x: x.get("firstShown") or "", reverse=True):
        print(f"- {ad.get('firstShown', '')[:10]} {ad.get('format')} {ad.get('advertiserName')} {ad.get('adUrl')}")


if __name__ == "__main__":
    main()
