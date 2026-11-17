---
id: computing-software.it-support-helpdesk.servicenow.knowledge-base-authoring-and-maintenance
name: knowledge-base-authoring-and-maintenance
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, knowledge-base, kb-article, knowledge-centered-service, kcs, article-structure, deflection-rate, review-cycle, article-retirement, self-service-portal, search-ranking, tagging, knowledge-lifecycle, knowledge-review-cycle, knowledge-search]
level: practitioner
status: draft
description: "Write and maintain helpdesk KB articles that actually get used: structure, tagging for search, review/retirement cycles, and deflection as the metric that matters."
sources:
  - "https://www.serviceinnovation.org/kcs/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# knowledge-base-authoring-and-maintenance

Goal: turn repeat tickets into articles that actually get found and
followed — most KBs fail not from lack of articles but from articles
nobody can find or trust, which is a different problem than writing them.

## Structure that gets used, not just published
- Lead with the **symptom exactly as a user or L1 agent would type it**
  ("VPN disconnects every 10 minutes," not "Intermittent connectivity
  loss in remote access infrastructure") — search match on the article
  title/summary is usually the first filter, and jargon titles lose to
  plain-language ones even when the content is identical.
- A usable troubleshooting article has, in order: symptom, scope (who/
  what this applies to — a fix for Windows 11 that doesn't apply to
  Windows 10 needs that said up front, not discovered after step 4),
  numbered steps in the order to actually try them, and an escalation
  path if the steps don't resolve it. Skipping scope is the single most
  common cause of an agent following the wrong article on a similar-
  looking but different issue.
- Separate **customer-facing** articles (self-service portal, plain
  language, safe steps only) from **internal-only** ones (agent
  procedures that touch admin tools, or that reveal information not
  meant for end users) — publishing an internal-only article to the
  public portal by mistake is a recurring, embarrassing failure mode;
  check the article's audience/visibility field before publishing, every
  time, not just on creation.

## Knowledge-Centered Service (KCS) habit: write while you solve, not after
- The KCS methodology's core practice is capturing the article *during*
  ticket resolution, not as a separate task done later "when there's
  time" — articles written from memory after the fact lose the exact
  error text/steps that made the original resolution work, and "later"
  tends to mean "never" under ticket-volume pressure.
- Reuse existing articles via **link, then improve in place**, rather
  than creating a near-duplicate for a slightly different symptom of the
  same root cause — duplicate articles are the main way a KB stops being
  trustworthy; before authoring, search for the issue using at least two
  different phrasings a user might search, not just the exact words you'd
  use.

## Tagging and search ranking
- Tag with the error message text verbatim (if there's a specific error
  code/string), not just the general topic — a user pasting an exact
  error code into search needs it to match something; a vague "network
  issue" tag doesn't surface for `0x80070005`.
- Most ITSM KB search ranks by a mix of recency, view count, and
  "helpful" votes — an old, un-rated article can outrank a better newer
  one purely on age/view count; periodically check which articles
  surface first for common search terms and re-tag or merge rather than
  assuming the ranking reflects quality.

## Review cycles and retirement
- Set an explicit review interval per article (commonly tied to product
  version lifecycle — review when the underlying app/OS gets a major
  update, or at a fixed interval like 6–12 months for anything without a
  clear trigger) — an article with no review date just accumulates
  staleness silently; most ITSM tools support a "review date" field, use
  it.
- Retire (don't delete outright if audit history matters) articles for
  decommissioned systems/apps promptly — a stale article still showing
  up in search for software nobody uses anymore erodes trust in every
  other search result, not just that one hit.
- When an article is superseded by a better one, mark the old one
  retired with a pointer to the replacement, rather than leaving both
  live — agents and users will otherwise find either one at random.

## Deflection and quality metrics
- **Deflection rate** (self-service portal views that close a ticket
  without agent involvement) is the metric that actually matters for
  customer-facing KB ROI — view count alone doesn't tell you whether the
  article worked, people may view it and still open a ticket because it
  didn't help.
- Agent-side, track **KB usage per ticket resolution** (was an article
  linked/followed to close this ticket) — a KB with high authoring volume
  but low usage-at-resolution signals a findability problem (bad
  tagging/titles), not a content-volume problem; don't respond to that
  signal by writing more articles before fixing search/tagging.

## Gotchas
- Screenshots go stale fast when the UI changes (a vendor UI refresh
  breaks every "click here" screenshot at once) — where possible,
  describe the path by menu labels/settings names in addition to images,
  so the text instructions still work when the screenshot doesn't match.
- An article "fixed" for one OS/app version that silently gets applied to
  a newer version with different steps is worse than no article — this
  is why scope (see Structure above) isn't optional detail, it's the
  difference between helpful and actively harmful.

## Verify
- A newly authored article is findable by at least two realistic search
  phrasings a user/agent would actually type, has a scope statement, a
  review date set, and (for customer-facing articles) shows the correct
  portal visibility. Check deflection or usage-at-resolution after a
  few weeks to confirm it's actually being used, not just published.
