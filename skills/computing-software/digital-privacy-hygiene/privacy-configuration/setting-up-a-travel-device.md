---
id: computing-software.digital-privacy-hygiene.privacy-configuration.setting-up-a-travel-device
name: setting-up-a-travel-device
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, travel-device, travel, high-risk-users, burner-phone, border-device-search, data-minimization]
level: practitioner
status: draft
description: "Prepare a clean travel phone or laptop for high-risk trips: minimal accounts, separate credentials, tamper checks, safe charging, and wiping it on return."
sources:
  - "https://ssd.eff.org/module/things-consider-when-crossing-us-border"
  - "https://www.privacyguides.org/en/basics/threat-modeling/"
  - "https://www.cisa.gov/topics/cybersecurity-best-practices"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Setting up a travel device

**Goal:** travel to countries with intrusive border regimes or targeted surveillance carrying a device that
holds as little as possible and can be discarded or wiped.

## Build it
- Phone: a supported device, factory reset, latest OS. iPhone with Lockdown Mode, or Pixel with Android Advanced
  Protection/GrapheneOS for higher risk.
- Laptop: a Chromebook (Powerwash before and after) or a freshly installed laptop with full-disk encryption.
- Accounts: travel-only email and messaging accounts where possible; if you need work email, use web access with a
  security key and log out when done. No password manager vault with everything: carry a travel vault with only the
  needed logins.
- Data: nothing local you cannot afford to have copied; fetch documents on demand and delete after.

## On the trip
- Keep devices on your person; hotel safes and rooms are not secure. Power off when leaving them.
- Charge with your own plug; use a USB data blocker or charge-only cable for public ports and rental cars.
- Use a trusted VPN on hotel/public Wi-Fi; expect it to be blocked in some countries.
- Tamper evidence for laptops: photograph screws coated with glitter nail polish; check on return to the room.
- Turn off Bluetooth and Wi-Fi when not needed; do not accept unexpected pairing or AirDrop.

## Return
- Do not connect the travel device to home or work networks before reset.
- Wipe/reflash phone and laptop; change passwords used on the trip; revoke sessions for travel accounts.
- Review logins for unusual activity in the following weeks.

## Verify
- [ ] Travel device holds only travel accounts/vault; main devices stay home; reset scheduled on return.
