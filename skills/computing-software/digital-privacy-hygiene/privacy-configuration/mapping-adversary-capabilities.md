---
id: computing-software.digital-privacy-hygiene.privacy-configuration.mapping-adversary-capabilities
name: mapping-adversary-capabilities
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, adversary-capabilities, threat-model, security-plan]
level: practitioner
status: docs-checked
description: "Map each realistic adversary's capabilities (access, legal power, money, skill, proximity) to the specific defences that actually stop them."
sources:
  - "https://ssd.eff.org/module/your-security-plan"
  - "https://www.privacyguides.org/en/basics/threat-modeling/"
  - "https://www.privacyguides.org/en/basics/common-threats/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mapping adversary capabilities

**Goal:** spend effort on defences that match who might come after you, not on generic fear.

## Questions per adversary (from EFF's "Your Security Plan")
- Who is the adversary, and what might they want to do with your data?
- What can they do? EFF's examples: your mobile phone provider has access to all your phone records; a government may
  have stronger capabilities. Privacy Guides adds that a hacker on an open Wi-Fi network can read unencrypted traffic.
- How likely is it (risk goes hand-in-hand with capability) and how bad are the consequences if they succeed?

## Capability map (Privacy Guides "Common Threats" categories)
| Threat | What it looks like | Defences the page names |
|---|---|---|
| Passive attacks | Malware, data breaches and other attacks made against many people at once | Security first: privacy tools are futile if easily exploited; compartmentalisation limits damage from malicious software |
| Targeted attacks | Malicious documents by email, exploited browser/OS vulnerabilities, physical attacks | Virtual machines (for example Qubes OS) to isolate browsers, mail and office apps; for physical attacks, an OS with verified boot, an encrypted drive, a TPM or Secure Enclave that rate-limits passphrase attempts, and not sharing your computer with people you do not trust |
| Supply chain attacks | Malicious code added to otherwise good software or a dependency | Software with a good reputation and long history, public trusted build infrastructure, signed commits and releases, several maintainers |
| Service providers | Provider (or someone who breaches it) can read what is stored on its servers | End-to-end encryption, preferring native apps to web clients; metadata (who, how often, when) is still visible |
| Mass surveillance | Government or corporate monitoring of a large part of a population; tracking via IP address, cookies, submitted data, fingerprints and payment correlation | Compartmentalise online identities, blend in with other users, avoid giving identifying information |
| Surveillance capitalism | Ad networks and data brokers | Content blockers and reading privacy policies (reduces but cannot fully prevent tracking); encrypt or obfuscate data |
| Public exposure | Information about you findable by search engines or the public | Delete unwanted information, use private mode and privacy settings, avoid publishing in the first place |
| Censorship | Governments, network administrators or providers blocking access or speech | Tor, censorship-resistant platforms such as Matrix; note a VPN or Tor cannot hide that you are using them |

## Use it
Pick your top 2-3 adversaries, list the defences in their row, compare to what you have. Everything else is
lower priority. For adversaries not on the table (an abusive partner, an employer, a thief), apply the same
questions: what access and knowledge do they have, and which controls remove it.

## Gotchas
- EFF notes trusted people can compromise your assets by being careless with their own security.
- Privacy Guides: anonymity and privacy are different; most people do not need total anonymity.
- A security plan changes as your situation changes; revisit it on a schedule.

## Checked
Checked 2026-11-08 against the full text of the three cited pages (EFF "Your Security Plan"; Privacy Guides "Threat
Modeling" and "Common Threats"). Rebuilt the capability table on the categories and defences those pages state.
Removed claims they do not support: Safety Check, carrier locks, SIM swap, credit freeze, stalkerware check, stolen
device protection, Lockdown Mode, zero-click exploits and the abusive-partner, employer and thief rows.
Method: documentation only; no commands were run.
