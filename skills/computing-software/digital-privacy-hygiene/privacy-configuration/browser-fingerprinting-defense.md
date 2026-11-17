---
id: computing-software.digital-privacy-hygiene.privacy-configuration.browser-fingerprinting-defense
name: browser-fingerprinting-defense
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, browser-fingerprinting, canvas-fingerprinting, font-fingerprinting, letterboxing, resist-fingerprinting, multi-account-containers, tor-browser, mullvad-browser, user-agent, screen-resolution, webgl, cover-traffic, panopticlick, coveryourtracks]
level: advanced
status: draft
description: "Reduce browser fingerprinting without stacking extensions that make you more unique: letterboxing, font/canvas protections, containers, and when adding another tool backfires."
sources:
  - "https://coveryourtracks.eff.org/"
  - "https://support.mozilla.org/kb/firefox-protection-against-fingerprinting"
  - "https://www.torproject.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Browser fingerprinting defense

**Goal:** reduce how uniquely identifiable your browser is across sites — a
tracking method that works even with cookies blocked — without the common
mistake of adding "privacy" extensions that each make the combination *more*
distinctive, the opposite of the goal.

## 1. What fingerprinting actually measures
A site combines many small, individually unremarkable signals — screen
resolution, installed fonts, GPU/WebGL renderer string, timezone, language,
canvas rendering output (subtle anti-aliasing differences reveal OS/GPU/driver),
audio-stack rendering, number of CPU cores, battery API (largely removed from
browsers now), and the exact list of browser extensions/plugins — into a
combined fingerprint. Cookies aren't involved at all; this works even in a fresh
private window with every cookie blocked, and is why "I block cookies" is not
"I'm not tracked."

## 2. The core paradox: most defenses make you stand out more, not less
Blocking one signal, or adding an extension, changes your fingerprint from
"blends into the large crowd of default-configured browsers" to "has this
unusual combination of signal X blocked plus extensions Y and Z installed" —
which can be *more* identifying than doing nothing, because few other users have
that exact combination. The actual goal is to look like the **largest possible
group of other people**, not to individually minimise each signal.
- **Don't stack multiple "anti-fingerprinting" or "privacy" extensions.** Each
  one is itself a detectable signal (and often injects a slightly different,
  individually detectable script). One well-built browser-level protection beats
  three extensions layered on top of each other.

## 3. What to actually use, by threat level
- **Ordinary use (most people)**: Firefox's built-in **Resist Fingerprinting**
  mode (`privacy.resistFingerprinting` in `about:config`, or enabled by
  "Strict" Enhanced Tracking Protection in recent versions) applies
  **letterboxing** — rounding the reported window size to common buckets with
  grey bars added, so your window dimensions match a large group of other users
  instead of your exact pixel count — plus spoofed timezone (UTC) and reduced
  precision on several APIs. This alone, with no added extensions, is the
  better trade for daily browsing: real fingerprinting resistance from blending
  in, not from a custom, rarer configuration.
- **Higher sensitivity**: **Tor Browser** is built specifically so every
  instance presents an (as close as achievable) identical fingerprint to every
  other Tor Browser user — the strongest anti-fingerprinting posture that
  exists, at the cost of speed and some site breakage, and it's paired with
  Tor's network-level anonymity (see
  `computing-software.digital-privacy-hygiene.vpn-tools.vpn-dns-and-tracker-blocking-setup`).
  Don't log into personally identifying accounts through it, which would
  re-link the "anonymous" identity anyway.
- **Mullvad Browser**: the same anti-fingerprinting engineering as Tor Browser
  (built with the Tor Project), without routing through the Tor network —
  intended to be paired with a trusted VPN instead, for people who want Tor's
  fingerprint resistance with a faster/different network layer.

## 4. Containers for separating identities without separate browsers
Firefox **Multi-Account Containers**: tabs in different coloured containers get
separate cookie/storage jars within the same browser — logging into the same
site in two containers gives two unrelated sessions. This stops cross-site
*cookie* tracking and keeps "work Google" separate from "personal Google," but
does **not** change the underlying device fingerprint, which is shared across
all containers in the same browser — containers solve a different problem
(identity separation) than fingerprinting resistance does.

## 5. Checking where you actually stand
Use **Cover Your Tracks** (coveryourtracks.eff.org, EFF's successor to
Panopticlick) to see your current fingerprint's uniqueness and which specific
signals are most revealing for your setup — re-test after any browser or
extension change, since the result shifts as your configuration (and the rest
of the population's) changes.

## Gotchas
- Spoofing a single signal (e.g. a fake user-agent string) while every other
  signal stays default-revealing often creates an internally inconsistent,
  easily flagged fingerprint — partial, piecemeal spoofing can be worse than
  none.
- Private/incognito windows have zero effect on fingerprinting; they only avoid
  saving local history and cookies to your own disk.
- Uncertain: exact letterboxing bucket sizes and which signals Resist
  Fingerprinting currently covers change between Firefox releases — re-check
  Mozilla's current documentation rather than assuming last year's behaviour.

## Verify
- [ ] You can explain why cookies being blocked doesn't mean fingerprinting is
      blocked.
- [ ] No more than one browser-level anti-fingerprinting mechanism is active at
      once (built-in Resist Fingerprinting, or Tor/Mullvad Browser — not several
      stacked extensions).
- [ ] You've checked your actual fingerprint uniqueness at coveryourtracks.eff.org.
- [ ] You know the difference between what containers solve (identity
      separation) and what they don't (device fingerprinting).
