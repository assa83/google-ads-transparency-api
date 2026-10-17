# Google Ads Transparency Center API – working example (Python, JS, n8n)

Get every ad a competitor runs on Google Search, YouTube, Shopping, Maps and Play from the public Google Ads Transparency Center as JSON, and get alerts when they launch new ads.

Powered by the [google-ads-transparency-scraper](https://apify.com/lagenuina_agency/google-ads-transparency-scraper) actor on Apify. No browser, no cookies, no account on Google.

## Example output (real result, shortened)

```json
{
  "creativeId": "CR04488592264313962497",
  "advertiserId": "AR00930880903813529601",
  "advertiserName": "Grocery Delivery E-Services USA Inc.",
  "domain": "hellofresh.com",
  "format": "TEXT",
  "firstShown": "2026-04-29T03:41:27.000Z",
  "lastShown": "2026-10-16T17:41:03.000Z",
  "shownForDays": 172,
  "imageUrl": "https://tpc.googlesyndication.com/archive/simgad/11360510690000944312",
  "previewUrl": null,
  "adUrl": "https://adstransparency.google.com/advertiser/AR00930880903813529601/creative/CR04488592264313962497?region=US",
  "region": "US"
}
```

## Quickstart (3 steps)

1. Create a free Apify account and copy your API token from [Settings → Integrations](https://console.apify.com/settings/integrations).
2. Put it in an environment variable (never in code): `export APIFY_TOKEN=your_token`
3. Run the example:

```bash
pip install -r python/requirements.txt
python python/example.py hellofresh.com --region US
```

JavaScript: `cd js && npm install && node example.mjs`

## Examples

**Python** (`pip install "apify-client<2"`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("lagenuina_agency/google-ads-transparency-scraper").call(run_input={
  "queries": [
    "hellofresh.com"
  ],
  "region": "US",
  "maxAdsPerSearch": 50
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

**JavaScript / Node.js** (`npm install apify-client`)

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('lagenuina_agency/google-ads-transparency-scraper').call({"queries": ["hellofresh.com"], "region": "US", "maxAdsPerSearch": 50});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

**cURL / any language** – one HTTP call, results in the response:

```bash
curl -X POST "https://api.apify.com/v2/acts/lagenuina_agency~google-ads-transparency-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"queries": ["Nike"], "resultType": "advertisers", "region": "US"}'
```

All input fields are documented on the [actor page](https://apify.com/lagenuina_agency/google-ads-transparency-scraper) (Input tab).

## Use case: Monitor new competitor ads (onlyNewAds)

`python/example.py` runs the actor with `onlyNewAds: true` and a `monitorStoreName` per competitor: the first run remembers every creative, each later run returns (and bills) only ads launched since. Schedule it daily (cron, GitHub Actions, Apify Schedules or the n8n workflow) and forward the output to Slack or email.

## n8n workflow

[`n8n/workflow.json`](n8n/workflow.json): every day 09:00 → run the actor with `onlyNewAds` → keep the useful fields with a Set node (connect Slack/Gmail after it).

1. In n8n: **Workflows → Import from File** and pick `n8n/workflow.json`.
2. Create a **Header Auth** credential named `Apify API token` with name `Authorization` and value `Bearer <your token>`, and select it in the *Run Apify actor* node.
3. Edit the JSON body (your keywords/targets) and activate.

The `run-sync-get-dataset-items` endpoint waits up to 300 s; for bigger runs use `/runs` plus a webhook.

## Use with AI agents (MCP)

Give Claude, ChatGPT, Cursor or any MCP client this actor as a tool:

```
https://mcp.apify.com/?actors=lagenuina_agency/google-ads-transparency-scraper
```

Example config (Claude Desktop, Cursor, VS Code):

```json
{
  "mcpServers": {
    "google-ads-transparency-scraper": {
      "url": "https://mcp.apify.com/?actors=lagenuina_agency/google-ads-transparency-scraper"
    }
  }
}
```

Sign in with Apify OAuth when asked, or send `Authorization: Bearer <APIFY_TOKEN>`.

## Pricing

$1.60 per 1,000 ads ($0.0016 per ad creative), no start fee, pay only for results – see [lagenuina_agency/google-ads-transparency-scraper](https://apify.com/lagenuina_agency/google-ads-transparency-scraper).

## Disclaimer

Independent, not affiliated with Google (not endorsed by Google LLC). It reads only publicly available data. Use it in line with the applicable terms and laws.

## License

[MIT](LICENSE) © Quelli di Carne Genuina
