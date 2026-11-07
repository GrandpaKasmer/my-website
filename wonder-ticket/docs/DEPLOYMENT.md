# Website and domain handoff

## Proposed deployment

Create a NEW hosting project. Do not overwrite another application's deployment or change domain records until the preview works. This session has not changed DNS, nameservers, email, or the live website.

For the isolated branch in the existing original Grandpa Kasmer repository:

| Setting | Value |
|---|---|
| GitHub repository | GrandpaKasmer/my-website |
| App branch | wonder-ticket-v0-1 |
| Root directory | wonder-ticket |
| Framework preset | Other |
| Node version | 22.x |
| Build command | npm run build |
| Output directory | dist |
| Environment variables | None |

IMPORTANT: main still contains the original website. Choose the app branch explicitly. In Vercel, configure this new project's production branch as `wonder-ticket-v0-1` before production deployment, or review/merge the isolated app changes first and deliberately select main. Do not silently replace an existing project or merge unrelated work.

If you create a dedicated repository using only the contents of this package, the root directory is the repository root instead, not `wonder-ticket`.

The supplied vercel.json sets the build/output and security headers. No external scripts are used; inline script/style are explicitly allowed by this version's policy. Keep the root directory correct so this configuration is picked up.

## Domain connection

1. Deploy and verify the provider's preview URL: complete a reading, save/reopen/delete a ticket, export a PNG, and inspect privacy/terms.
2. In the new project's Settings → Domains, add `grandpakasmer.com` and `www.grandpakasmer.com`.
3. Choose one canonical hostname and redirect the other. The proposed brand uses the apex hostname.
4. At the CURRENT authoritative DNS provider, use the EXACT A/CNAME/TXT values displayed for this project. Do not assume the historical domain registrar still hosts its DNS, and do not copy another project's IP or CNAME.
5. Preserve all email MX, SPF/DKIM/DMARC, other TXT records, and unrelated subdomains. Prefer changing only the relevant website records. Do not change nameservers for this simple deployment.
6. Verify both hostnames, the redirect, HTTPS, and mail delivery before calling the domain connected.

The domain's current website and DNS provider were not verified in this session. Export/screenshot current records first so you can restore them if necessary.

## Final phone checks

Open the live HTTPS site in Safari and Chrome, not just an embedded preview. Test small text/large text, landscape, reduced motion, sharing (including cancel), PNG saving, local storage after a full reload, deletion, and refresh after a new deployment. Open once online, then test the offline cache. Install/Add to Home Screen and repeat. Do not describe offline operation as verified before this test.

No payment flow is included. Before commercial use, verify that the hosting plan permits the intended use and review privacy/support obligations. A one-time app purchase would not eliminate ongoing hosting/platform upkeep.

Official reference checked November 7, 2026:
https://vercel.com/docs/domains/working-with-domains/add-a-domain
