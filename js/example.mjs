// Competitor ads that keep running longest (usually the ones that work).
// Usage: node example.mjs hellofresh.com
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set APIFY_TOKEN first: https://console.apify.com/settings/integrations');
    process.exit(1);
}

const competitor = process.argv[2] ?? 'hellofresh.com';
const client = new ApifyClient({ token });
const run = await client.actor('lagenuina_agency/google-ads-transparency-scraper').call({
    queries: [competitor],
    region: 'US',
    maxAdsPerSearch: 100,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
items.sort((a, b) => (b.shownForDays ?? 0) - (a.shownForDays ?? 0));
for (const ad of items.slice(0, 10)) {
    console.log(`${ad.shownForDays} days  ${ad.format}  ${ad.advertiserName}  ${ad.adUrl}`);
}
