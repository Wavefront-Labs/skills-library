---
id: computing-software.it-support-helpdesk.servicenow.field-dispatch-for-desk-side-visits
name: field-dispatch-for-desk-side-visits
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, field-dispatch, desk-side-support, dispatch, field-service, site-visit]
level: practitioner
status: draft
description: "Dispatch desk-side and field visits: deciding when a visit is needed, booking and routing technicians, parts and access prep, and closing the loop in the ticket."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-field-service-management/page/product/field-service-management/concept/c_FieldServiceManagement.html"
  - "https://www.comptia.org/en/certifications/a/"
  - "https://www.thinkhdi.com/certification/support-center-analyst"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# field-dispatch-for-desk-side-visits

Visits are expensive (travel, idle time). Dispatch only when remote work genuinely can't
fix it, and make the first visit the last.

## When to dispatch
- Hardware fault needing hands: no power, broken screen, physical cabling, printer jam
  the user can't clear, peripheral swaps.
- Device can't get online at all, so remote tools are out.
- Accessibility or VIP model requires in-person.
- Not for: anything fixable via remote control or a user following three steps.

## Before the visit
1. Confirm location (building, floor, desk), user availability window and a phone number.
2. Diagnose remotely as far as possible; record what has been ruled out.
3. Pull likely parts or a swap unit (loaner laptop, toner, dock, cable) so the visit fixes
   it first time. Note asset tags of parts taken.
4. Arrange access: badge, escort, after-hours permission, secure areas.
5. Create a visit task: in ServiceNow FSM a work order with tasks scheduled via the
   dispatcher workspace; otherwise a child task assigned to the field tech with the slot.

## Routing visits
- Batch visits by building/floor; a tech doing 6 visits on one floor beats 6 trips.
- Priority still wins: a P2 outage on site goes first.
- Remote sites without staff: a smart-hands contract with a vendor, with the ticket
  carrying exact instructions and photos expected back.

## During and after
- Tech updates the ticket from mobile: arrival, work done, parts used, asset swaps
  (update CMDB/asset records for serials).
- Leave the user with a confirmation and, if follow-up is needed, a booked time.
- Returned faulty parts are tagged with the ticket number for RMA.

## Verify
Visit rate per 100 tickets is tracked; repeat visits for the same issue within 14 days
are under target; asset records match what is physically at the desk.
