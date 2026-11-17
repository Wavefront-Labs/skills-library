---
id: computing-software.general-digital-literacy.basic-troubleshooting.surge-protectors-and-ups
name: surge-protectors-and-ups
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-device-lifecycle, surge-protector, ups, power-protection]
level: intro
status: draft
description: "Protect computers and routers from surges and outages with a proper surge protector or UPS, read joule and VA ratings, and avoid overloaded extension leads."
sources:
  - https://www.electricalsafetyfirst.org.uk/
  - https://www.apc.com/
  - https://www.esfi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Surge protectors and UPS

## Surge protector vs extension lead
- An ordinary extension lead gives more sockets, no protection. A **surge protector** diverts voltage spikes; look for a rating in **joules** (higher absorbs more; 1000+ for computers) and a *protected* indicator light.
- UK: BS 5732 or BS EN 61643; US: UL 1449 listing.
- Protection wears out with each surge; replace after a big event or when the *protected* light goes out (many units keep supplying power with no protection).
- Lightning: unplug equipment, including the router's phone/coax line, during storms; nothing plug-in fully stops a direct strike.

## UPS (uninterruptible power supply)
- Battery that keeps a PC, router or NAS running through brief cuts and gives time to shut down.
- Size by **VA/watts**: add up equipment wattage, choose a UPS with 25-50% headroom. A router plus modem needs very little; a desktop plus monitor ~300-500 W.
- *Line-interactive* handles brownouts; *online* gives cleanest power for sensitive gear.
- Connect the USB cable and install the maker's software so the PC shuts down cleanly before the battery runs out.
- Batteries last 3-5 years; the unit beeps or self-test fails when due.

## Safety
- Don't daisy-chain extension leads or plug a surge protector into a UPS's battery outlets (unless the maker allows).
- Don't exceed the lead's rating (UK 13 A total); heaters and kettles don't belong on extension leads.

## Verify
- [ ] Surge protector shows protected status; UPS self-test passes and the PC shuts down automatically on a pulled-plug test.
