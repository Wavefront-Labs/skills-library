---
id: computing-software.it-support-helpdesk.servicenow.service-status-page-and-portal-announcements
name: service-status-page-and-portal-announcements
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, service-status-page, portal-announcements, outage-banner, service-portal, deflection, major-incident-communication]
level: practitioner
status: gated
description: "Publish outages on the self-service portal: ServiceNow announcements and banners, a service status page fed by outage records, wording, and taking notices down on time."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-platform-user-interface/page/build/service-portal/concept/announcements.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/incident-management/concept/outage-records.html"
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/product/service-status/concept/service-status-overview.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# service-status-page-and-portal-announcements

During an outage, the portal banner is the cheapest call deflection you have: every user
who reads "Email is down, fix expected 11:00" is a call not taken.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Announcements (Service Portal)
- Service Portal > Announcements (`announcement` table): title, summary, details link,
  display style (banner or widget), **From/To dates**, portals, and audience by user
  criteria (e.g. only EMEA, only one company).
- Types control colour/icon (e.g. Outage, Maintenance, Information). Users can dismiss
  dismissible ones; outage banners should not be dismissible.
- Employee Center uses the same records through its announcement/banner widgets.

## Status page fed by outage records
- Outage records (`cmdb_ci_outage`) created from the major incident (Related links >
  Create outage) with type (Outage, Degradation, Planned), CI/business service, begin and
  end times.
- A status widget (the base Service Status / "System status" page, or a custom widget
  reading `cmdb_ci_outage` for business services marked Show on portal) displays current
  state per service. Planned maintenance comes from change records with outage type
  Planned.
- Benefit: the end time you set when restoring closes the banner automatically, and
  availability reports use the same records.

## Writing the notice
- Service name users recognise ("Email and calendar"), not CI names ("EXO-PRD-01").
- Impact: who and what ("Outlook on Windows cannot send; phones are fine").
- Workaround if any ("use Outlook on the web").
- Next update time, even if no fix ETA. Update the banner at that time regardless.
- No speculation about cause until confirmed.

## Run it with the major incident
1. Communications lead posts within 15 minutes of declaring P1.
2. Phone IVR message and the portal say the same thing (copy the same text).
3. On restoration: change the banner to "Resolved, monitoring" for 1-2 hours, then expire.
4. Link the announcement in the major incident's communication tasks so it is reviewed.

## Gotchas
- Forgotten banners with a To date far in the future train users to ignore banners.
  Always set a To date; extend if needed.
- Audience filters that rely on location fields fail for users with blank location; test
  with an affected user via impersonation.

## Verify
Impersonate an affected user and a non-affected user; the right one sees the banner, the
status page shows the service degraded, and the banner disappears at its end time.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
