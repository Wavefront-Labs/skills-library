---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.site-creation-hub-sites
name: site-creation-hub-sites
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [site-creation-hub-sites, tso-sharepoint-sites]
level: practitioner
status: draft
description: Create sites, register hubs and manage active sites.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Site creation and hub sites
**Goal:** Create sites, register hubs and manage active sites.

- SharePoint admin center > Sites > Active sites > Create (team site or communication site).
- Register hub: `Register-SPOHubSite -Site https://contoso.sharepoint.com/sites/hub`.
- Associate sites with `Add-SPOHubSiteAssociation`.
- Self-service site creation setting under Settings.

## Gotchas
- Hub association doesn't change permissions.
- Deleted sites sit in the deleted sites list for 93 days (confirm).

## Self-check
Child site shows the hub navigation.
