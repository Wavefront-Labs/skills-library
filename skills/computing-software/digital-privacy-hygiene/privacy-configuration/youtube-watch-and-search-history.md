---
id: computing-software.digital-privacy-hygiene.privacy-configuration.youtube-watch-and-search-history
name: youtube-watch-and-search-history
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, youtube-history, google-privacy, auto-delete]
level: practitioner
status: docs-checked
description: "Manage YouTube watch and search history: pause or auto-delete it, remove items, understand the effect on recommendations, and handle history on a TV or signed out."
sources:
  - "https://support.google.com/youtube/answer/95725"
  - "https://support.google.com/accounts/answer/465"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# YouTube watch and search history

**Goal:** control what YouTube (and Google) keeps about what you watch and search for. Menu labels follow Google's
help pages and change; search the page for the key word if one differs.

## Where
- My Activity (myactivity.google.com) > **YouTube History** > **Manage history** lists the videos you watched.
- Signed out of an account, or inside YouTube itself: YouTube > **History**.

## Options
| Action | Path (Google's help page) | Effect |
|---|---|---|
| Pause watch history | My Activity > Controls tab (left sidebar) > Turn off | Videos watched while history is off do not appear in it |
| Choose what is included | Same Controls page: videos you watch, your searches on YouTube, voice and audio activity | Each is a separate option while history is on |
| Auto-delete | My Activity > YouTube History > Manage history > Auto-delete > pick a time range > Next > Confirm | Rolling deletion; the available ranges are shown in the dialog |
| Delete items | Delete next to a video, or DELETE for several | Removes them; YouTube stops basing recommendations on that content |
| Pause or clear without signing in | YouTube > History > Pause watch history or Clear all watch history | Same effect for that history |

Using DELETE on watch history also deletes the search history from the selected time frame.

## TV or game console
In the YouTube app left-hand menu: Settings > **Pause watch history**, or **Clear watch history**, then confirm with
the button.

## Recommendations
If you have no relevant recent watch history and have said you do not want recommendations based on it, features such
as homepage recommendations are removed. Deleting or pausing is therefore a trade of privacy for personalisation.

## Broader My Activity controls
- Delete everything: myactivity.google.com > Delete > All time > Next > Delete.
- Filter by date and product before deleting; some Google products do not save activity in My Activity.
- Account-wide auto-delete: Google Account > Data & privacy > History settings > the setting > Auto-delete. Google
  notes some data goes sooner than the period you choose.
- Turn off a setting in Data & privacy > History settings, optionally with Turn off and delete activity.

## Gotchas
- Pausing history leaves the homepage nearly empty, as above.
- Signing in to your Google Account inside a private (Incognito) window may still store your search activity in that
  account.
- Deleted items can linger on devices that are offline until they reconnect. Browser history is separate from My
  Activity and is deleted in the browser.
- Google says deletion starts by removing data from view, then a process to delete it from storage; some data may be
  retained longer for business or legal requirements.

## Checked
Checked 2026-11-08 against the full text of Google's "View, delete, or turn on or off watch history" (YouTube Help
95725) and "Delete your activity" (Google Account Help 465). Removed what they do not state: the 3, 18 or 36 month
auto-delete choices, separate-account and YouTube Kids advice for shared TVs, the My Ad Center remark, the claim that
subscriptions keep working, and the cookie claim for signed-out viewing; the myactivity.google.com product page is
a login redirect and was dropped from sources.
Method: documentation only; no commands were run.
