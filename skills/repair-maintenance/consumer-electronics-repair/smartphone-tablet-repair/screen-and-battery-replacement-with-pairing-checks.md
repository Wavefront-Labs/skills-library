---
id: repair-maintenance.consumer-electronics-repair.smartphone-tablet-repair.screen-and-battery-replacement-with-pairing-checks
name: screen-and-battery-replacement-with-pairing-checks
category: repair-maintenance
field: consumer-electronics-repair
product: smartphone-tablet-repair
tags: [smartphone-tablet-repair, phone-repair, tablet-repair, iphone, ipad, android, samsung-galaxy, screen-replacement, oled, lcd, digitizer, battery-replacement, li-ion, lithium-polymer, swollen-battery, adhesive-pull-tabs, ifixit, ifixit-opener, heat-pad, suction-cup, opening-pick, parts-pairing, true-tone, face-id, charge-port, water-damage, ip68-seal]
level: practitioner
status: draft
description: "Open phones and tablets safely, replace screens, batteries and charge ports, handle swollen Li-ion cells, treat liquid damage and check part pairing, True Tone and seal before return."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Phone and tablet screens, batteries and ports — with pairing checks

**Goal:** replace the common wear parts on a phone or tablet without puncturing the
battery, tearing a flex cable or losing functions to parts pairing, and hand it back
sealed and tested.

## 1. Intake (before touching it)
- Test and write down what works: touch, Face ID/fingerprint, cameras, mics, speakers,
  Wi-Fi, charging, buttons. A phone with a smashed screen may already have a dead
  proximity sensor — you need the record.
- Check for **swelling** (screen lifting, back bulging) and liquid indicators.
- Drain the battery below ~25 % before opening; a less-charged cell is far less
  violent if punctured.

## 2. Opening
1. Heat the adhesive edge to ~70–80 °C (heat pad, iOpener-style bag, or hot air on
   low) for 1–2 minutes. Glass edges crack when cold.
2. Suction cup near the edge, lift a small gap, insert a thin plastic pick no deeper
   than ~3 mm on screen-opening phones (deeper cuts the display flex or the OLED).
   Back-opening Androids: work through the rear glass instead; screens come out
   last, often by destroying them.
3. Slide picks round, leave them in to stop the glue resealing. Isopropyl alcohol
   (99 %) dripped into the seam softens stubborn adhesive.
4. **Disconnect the battery first** after removing the bracket — before any other
   connector. Use a plastic spudger on connectors; metal tools short to ground.

## 3. Battery
- Pull-tab adhesive: pull slowly at a low angle, around corners without twisting;
  stretch, don't snap. If tabs break, IPA under the cell and a plastic card — never a
  metal lever, never bend the cell.
- Swollen cell: no heat, no prying from the middle. Lift from the edges with IPA and
  patience, and drop it in a fire-safe container / sand bucket immediately. A cell
  that hisses, smokes or heats: put the device in the bucket, outdoors if possible.
- Store old cells with taped terminals for proper Li-ion recycling.

## 4. Screen and charge port
- Transfer earpiece speaker, sensor flex, brackets and screws to the new screen
  exactly; screws of different lengths in the wrong hole can pierce the board (long-
  screw damage).
- Test fit the new screen connected but unsealed: touch every corner, check
  brightness, dead pixels, True Tone and proximity sensor.
- Charge port: on many phones it is a flex (swap); on cheaper Androids and many
  tablets it is soldered to a daughterboard or the mainboard. First try cleaning lint
  from the port with a wooden or plastic pick — it fixes many "won't charge" jobs.

## 5. Parts pairing
Recent iPhones and some Android models tie batteries, screens, cameras and biometric
sensors to the logic board serial. Unpaired parts can show "Unknown part" messages,
disable True Tone or battery health, or (for Face ID / Touch ID) stop working.
- Use genuine parts and the maker's calibration tool where offered (Apple's
  self-service repair system diagnostics, Samsung service tools).
- Programmer boxes can copy True Tone data from the original screen; battery health
  data is held on a small board on the cell, which some shops transfer.
- **Biometric sensors cannot be swapped** without the original paired module.
(Draft note: pairing rules change per model and OS update — check before quoting.)

## 6. Liquid damage
Disconnect battery, remove the board, scrub corrosion with 99 % IPA and a soft
brush (ultrasonic bath on bare boards only, no screens, speakers or mics), dry fully,
inspect under magnification for eaten components. Rice does nothing useful.

## Gotchas
- Apply the battery connector last on reassembly; the screen connector plugged in
  with power on can kill the backlight circuit.
- Replacement adhesive gaskets restore shape, not certified water resistance — tell
  the customer.
- Do not trust aftermarket screen brightness or touch as equal to OEM; quote both.

## Verify
- [ ] Every intake function retested and working (or pre-existing fault noted).
- [ ] No "unknown part" or pairing warnings, or customer told of them.
- [ ] Charges at expected rate on a USB meter; battery not warm after 15 min.
- [ ] Screen seated flush with new adhesive; no lifted edges or pressure marks.
- [ ] All screws in original holes; no rattles.
