---
id: transportation-logistics.postal-courier-delivery.parcel-courier-work.multi-drop-parcel-day
name: multi-drop-parcel-day
category: transportation-logistics
field: postal-courier-delivery
product: parcel-courier-work
tags: [parcel-courier-work, courier, parcel-delivery, multi-drop, van-loading, load-order, stop-sequencing, proof-of-delivery, pod, photo-pod, signature-capture, safe-place, neighbour-delivery, failed-delivery, carded, return-to-depot, collections, handheld-scanner, delivery-driver, last-mile, amazon-flex, dpd, evri, ups, fedex]
level: practitioner
status: draft
description: "Load a courier van in reverse-stop order, run 100+ drops efficiently, capture proof of delivery that stands up to a dispute, and handle failed deliveries and collections cleanly."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# A multi-drop parcel day

**Goal:** get every parcel delivered (or correctly failed) with defensible proof of
delivery (POD), in the fewest minutes per stop, without searching the van.

Carrier apps (and their exact POD rules) differ; this is the cross-carrier method.
*Draft: confirm safe-place and age-restricted rules in your carrier's handbook.*

## 1. Load the van for the route, not for speed of loading
1. Get the route/stop order **before** loading (from the app or manifest).
2. **Last stop goes in first.** Load front-to-back, deep to shallow, in reverse stop
   order. Use shelf zones: e.g. split the route into 4–6 blocks, each block a shelf
   section, labelled with the stop range (1–25, 26–50 …).
3. Within a block, label-out and readable: you should read the address without moving
   the parcel.
4. Heavies low and against the bulkhead; never stack heavy on fragile; keep the
   side-door area clear for the first block.
5. **Scan to van** every parcel. Missing-on-manifest or extra parcels get resolved at
   the depot, not at stop 37.

## 2. Running the stops
- Follow the app sequence unless you know a local constraint (school run, one-way
  loop, market day); re-order whole blocks, not single stops.
- **Stop routine:** park legally and safely → select parcels for this stop (check
  number of pieces!) → scan → deliver → POD → back in. Multi-piece consignments are the
  most common "partial delivery" complaint.
- Group stops: same building or terrace — park once, walk several.
- Hazard-lights parking in a live lane is not "legal and safe".

## 3. Proof of delivery that survives a dispute
- **Signature/name:** capture the recipient's printed name, not "OK" or a scribble alone.
- **Photo POD:** show the parcel *and* the location context — house number, door
  colour, or the safe place — in one frame. A close-up of a box on a doormat proves
  nothing. Avoid photographing people's faces or the inside of homes.
- **Neighbour delivery:** record house number and name, leave a card at the original
  address stating where it is.
- **Safe place:** only where the customer nominated one or carrier rules allow;
  out of sight from the street.
- **Age-restricted / ID-required:** check ID per the service rules; if the recipient
  can't show it, it's a failed delivery — never leave it.

## 4. Failed deliveries and collections
- Before failing, try: ring/knock and wait ~30–60 s, call or message through the app
  if allowed, nominated neighbour or safe place.
- Fail with the **correct reason code** (no access, nobody home, refused, address not
  found, damaged). Wrong codes create re-delivery loops and complaints.
- Collections: check the label/QR matches the booking, check the packaging is sealed
  and not damaged, scan it as collected, keep it separate from outbound deliveries.

## 5. End of day
Return failed parcels and collections to depot and **scan them back in**; reconcile:
loaded = delivered + failed + collections handed in. Report vehicle defects.

## Gotchas
- Leaving the engine running and doors open "for a second" is how vans and parcels
  get stolen; lock every stop.
- The app's time-per-stop targets assume you never search the van — load order is
  where time is saved.
- Dogs and parcels on porches: a POD photo of a parcel left where a dog can reach it
  is not a successful delivery.

## Verify
- [ ] Van loaded in reverse stop order with labelled block zones.
- [ ] Every POD photo shows parcel + identifiable location.
- [ ] Every multi-piece consignment delivered with all pieces counted.
- [ ] Failures carry the right reason code and a card where required.
- [ ] End-of-day count reconciles with nothing unaccounted for.
