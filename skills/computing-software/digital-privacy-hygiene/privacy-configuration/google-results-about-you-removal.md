---
id: computing-software.digital-privacy-hygiene.privacy-configuration.google-results-about-you-removal
name: google-results-about-you-removal
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, results-about-you, google-removal-request, data-brokers, personal-contact-info, doxxing-response, search-results]
level: intro
status: docs-checked
description: "Use Google's Results about you to find and request removal of search results showing your phone, address or email, and set alerts for new ones."
sources:
  - "https://support.google.com/websearch/answer/12719076"
  - "https://myactivity.google.com/results-about-you"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Google Results about you

**Goal:** remove search results that expose your contact information, so a casual search of your name doesn't reveal
your home address.

## Set up
1. Open the "Results about you" page (in the Google app: profile picture or initial > Menu > Results about you). On
   mobile web or desktop select **Get started** or **Settings**.
2. Enter your name and the personal info to look for: phone numbers, home addresses and email addresses (several of
   each are allowed), plus nickname or maiden name. Google uses these to check search results regularly.
3. Turn on notifications (email or the Google app). You get a first notification within a few hours, then a new one
   when new matching results appear. Some features are rolling out only for users over 18 in certain markets.

## Review and request
- Open the **To review** tab and select a result to see its website and the info it contains.
- Select **Request to remove**, or **Mark as reviewed** to do nothing. You get an email to confirm the request and
  again when it is reviewed.
- Track status under **Removal requests**: In progress, Approved, Denied or Undone. Select **Undo** to reverse a
  request. There may be a delay between approval and the result disappearing.
- Approved removals usually hide the URL for every query; sometimes only for queries containing your name.

## Limits
- Removal affects Google Search only. The page and your info stay on the source site; contact the website owner to
  remove it there.
- Requested info must be personal, and not something you control yourself (a social profile or personal blog you
  own). Google does not remove results on pages owned by educational or government institutions, or newspapers, as
  that info is considered valuable to the public. Those results show no remove option.
- Results for someone else, a person under 18, or professional info posted to harm you go through the detailed removal
  request form. Requests on behalf of others from your own account may be denied.
- Paywalled pages can still be reported: use the notification or the detailed form.
- To stop monitoring, use **Settings > Remove all personal info**.

## Verify
- [ ] Monitoring set for all your addresses, numbers and emails; notifications on.
- [ ] Results found have removal requests submitted and tracked.

## Checked
Date: 2026-11-08.
Confirmed against the Google Search Help article "Find and remove personal info in Google Search results" read in full:
setup, tabs, request statuses, policy limits, URL outcomes, undo, paywall, on-behalf-of, and monitoring removal.
Removed: the Bing removal form, the doxxing/explicit imagery/financial ID form list and the "reason" menu (not on the
page). The myactivity.google.com/results-about-you page needs sign-in and was not read.
Method: documentation only; no commands were run.
