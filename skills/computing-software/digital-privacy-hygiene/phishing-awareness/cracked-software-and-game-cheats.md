---
id: computing-software.digital-privacy-hygiene.phishing-awareness.cracked-software-and-game-cheats
name: cracked-software-and-game-cheats
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, cracked-software, infostealers, game-cheats, malware]
level: practitioner
status: draft
description: "Explain why cracked apps, keygens, game cheats and mod loaders are a main route for infostealer malware, and what to do if one was run."
sources:
  - "https://www.cisa.gov/news-events/news/understanding-and-protecting-against-malware"
  - "https://www.microsoft.com/en-us/security/blog/2025/05/21/lumma-stealer-breaking-down-the-delivery-techniques-and-capabilities-of-a-prolific-infostealer/"
  - "https://haveibeenpwned.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Cracked software and game cheats

**Goal:** stop free software from costing every account you own.

## Why it's dangerous
Pirated software, keygens, "free Photoshop", game cheats, aimbots, executors and Discord-shared mods are a top
distribution channel for infostealers (Lumma, RedLine, Vidar and similar). They:
- Steal browser passwords, **session cookies** (bypassing 2FA), crypto wallets, Discord and Steam tokens.
- Run once, upload everything in seconds, and may delete themselves.
- Often tell you to disable antivirus first: that instruction is the attack.
YouTube "tutorial" videos with download links in the description and password-protected archives are common lures.

## Safer alternatives
Free and open-source equivalents (GIMP, Krita, LibreOffice, Kdenlive, Blender), vendor free tiers and student
licences, official game mod stores (Steam Workshop, Nexus Mods with scanning).

## If you ran one
1. Disconnect the machine. Assume everything it stored is stolen.
2. From a **different, clean device**: change passwords for email, password manager, banking, then everything else;
   sign out all sessions; revoke Discord/Steam/Google tokens.
3. Move crypto to a new wallet created on a clean device.
4. Reinstall the operating system from scratch; antivirus cleanups can miss persistence.
5. Watch for account recovery emails and new-device logins for weeks.

## Gotchas
- Cheats run with admin or kernel drivers by design; anti-cheat bans are the least of the risks.
- Your stolen logs may be sold for months; reset sessions again if odd logins appear later.
