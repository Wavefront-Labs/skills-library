---
id: computing-software.digital-privacy-hygiene.privacy-configuration.removing-outdated-content-from-search
name: removing-outdated-content-from-search
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, outdated-content-removal, results-about-you, digital-footprint]
level: practitioner
status: docs-checked
description: "Get changed or deleted pages about you out of Google results: refresh outdated content, private-info and doxxing removal requests, and the limits of removal."
sources:
  - "https://support.google.com/websearch/answer/6349986"
  - "https://support.google.com/websearch/answer/9673730"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Removing outdated content from search results

**Goal:** Google stops showing old snippets or cached versions of pages that changed or were deleted, and pages exposing your private information are removed from Search.

## First: the source
Google can only remove things from Google Search results, not from the site hosting them. Ask the site owner to remove or update the page, then use the tools below.

## Outdated snippets and cache (Google's "Refresh outdated content")
- Use when content was deleted from a site but still comes up in Search, so the description or cache is outdated.
- If you already updated a live page you don't have to fill in the form.
- Select Request refresh, enter the page URL on the Page tab, Submit.
- For images: copy the image link address from images.google.com results, then Request refresh > New request > Image, paste it and Submit.
- Check status under Refresh outdated content in Google Search Console.

## Private information (Remove my private info from Google Search)
Eligible: your address, phone number or email; confidential government IDs (such as social security or tax ID numbers, resident ID card number); bank account or credit card number; pictures of your signature or ID; private records such as medical records; confidential usernames and passwords. For contact details, the "Results about you" feature finds and requests removal and can notify you of new results.
- Doxxing: needs a URL carrying your personal info with explicit or implicit threats or calls for others to harm or harass you, or a significant amount of aggregated personal info with no legitimate purpose.
- You or a representative submit the request with the URLs of the pages; only those URLs are reviewed. A screenshot is requested to help Google find the content; never take or share screenshots of sexual imagery of anyone under 18.
- Public interest counts: newsworthy content may stay up.
- Outcomes (you get an email): full removal (page gone from Search) or partial removal (page hidden for searches containing your name or identifier but may show for other queries).
- Content outside Google's policies may be covered by local law: use the Legal Help Center.

## Gotchas
- Removal from Search does not remove the content from the web; it can still be found through links, social media or other search engines.
- Track each request and its outcome so you can follow up.

## Checked
Method: documentation only; no commands were run. Checked 2026-11-08 against both Google Search Help pages (read in full). Removed because the pages do not support them: the Bing content removal tool (page is a stub), Wayback Machine exclusion, the 2-4 week recheck and the claim that the tool rejects requests when the live page is unchanged (Google says only that you need not file if you already updated the page).
