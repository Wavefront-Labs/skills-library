---
id: computing-software.software-engineering.mobile-development.store-listings-and-app-store-optimization
name: store-listings-and-app-store-optimization
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, app-store-optimization, store-listing, aso, product-page, custom-product-pages, store-listing-experiments, screenshots, keywords]
level: practitioner
status: docs-checked
description: "Write and optimise App Store and Google Play listings: App Store metadata limits, keyword rules, localisation, custom product pages and store listing experiments."
sources: ["https://developer.apple.com/app-store/product-page/", "https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information", "https://support.google.com/googleplay/android-developer/answer/9898842", "https://support.google.com/googleplay/android-developer/answer/6227309", "https://developer.apple.com/app-store/custom-product-pages/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Store listings and app store optimisation (ASO)

**Goal:** a product page that ranks for the searches your users make and converts visitors into
installs, maintained like any other release artefact.

## App Store metadata limits (Apple docs)
| Field | Limit / rule |
|---|---|
| App name | up to 30 characters |
| Keywords | 100 characters total, terms separated by commas with no spaces (spaces allowed inside a phrase) |
| Promotional text | up to 170 characters; can be updated without submitting a new version |
| Description | up to 4000 characters, plain text, no HTML |
| What's New | up to 4000 characters, required for every version after the first |
Limits for Google Play fields and for the subtitle: read them in the consoles; they change.

## Keywords and copy
- Research what users type (Apple Search Ads, Play Console search terms report, ASO tools). Aim for
  relevant mid-volume terms, not only the most competitive.
- Apple's page lists what to avoid in the keyword field to save characters; read it before filling it.
- Google Play policy: do not use special characters or all caps to manipulate search ranking, and do
  not use a celebrity name or brand logo without permission.
- Screenshots and videos must reflect the app's actual experience (Play policy). Show real UI.

## Localisation
Localise description, keywords, previews and screenshots for each market you ship in; Apple also
lets you translate the app name and tailor keywords per market.

## Experiments and custom pages
- **App Store product page optimisation**: test alternate icons, screenshots and app previews against
  the default; each version is shown to a share of randomly selected eligible users and results appear
  in App Analytics.
- **Custom product pages**: extra versions of the page with different screenshots, previews and
  promotional text, reached through unique URLs; deep links per page need iOS/iPadOS 18 or later.
  Their metadata goes through review independently of an app update.
- **Google Play store listing experiments**: default graphics experiments (icon, feature graphic,
  screenshots in the default language) and localized experiments (icon, feature graphic, screenshots,
  descriptions in up to five languages). Users who see a localized graphic asset are excluded from
  default graphics experiments.
- Change one variable at a time; seasonal effects confound short tests.

## Workflow
Keep metadata in the repo so changes are reviewed and uploaded with the release; track conversion in
App Store Connect analytics and Play Console acquisition reports.

## Verify
- [ ] Metadata within limits for every locale; no keyword-stuffing issues.
- [ ] Screenshots current with the shipping UI.
- [ ] At least one experiment running or recently concluded with a recorded result.

## Checked
2026-11-01. Confirmed on the Apple product-page and App Store Connect platform-version pages (name, keywords,
promotional text, description, What's New limits, localisation, product page optimisation, custom product pages),
the Apple custom-product-pages page (deep links iOS 18, separate review), and the Play help pages (listing policy
examples, experiment types and language limit). Removed as unconfirmed: subtitle, Play field limits, screenshot and
preview counts and sizes, the 35-page custom page cap, review-prompt frequency, fastlane tooling, per-locale indexing
detail, and which fields are indexed.
Method: documentation only; no commands were run.
