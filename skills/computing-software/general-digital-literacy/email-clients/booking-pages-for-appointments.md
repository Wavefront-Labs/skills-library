---
id: computing-software.general-digital-literacy.email-clients.booking-pages-for-appointments
name: booking-pages-for-appointments
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, calendar, booking-page, appointment-schedules, microsoft-bookings, calendly, scheduling]
level: intro
status: docs-checked
description: "Publish a Google Calendar appointment schedule so people book their own slot, with duration, buffers, daily limits, email verification and reminders."
sources:
  - https://support.google.com/calendar/answer/10729749
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Booking pages for appointments (Google Calendar)

**Goal:** people book a free slot themselves; no back-and-forth email.

## Create one
You need a computer with a supported web browser: appointment schedules cannot be created in the Calendar app for Android, iPhone or iPad. Some features need an eligible Google Workspace or Google One subscription.
1. Google Calendar > **Create** > **Appointment schedule**.
2. Set title, appointment duration (or Custom), general availability (dates, times, time zone), and **Scheduling window**: how far ahead people can book and the minimum lead time. The default minimum lead time is 4 hours, so a new page may show no slots for today.
3. Under booked appointment settings: **Buffer time**, **Maximum bookings per day**, **Guest permissions**.
4. **Calendars**: pick the calendar for bookings and tick **Check calendars for availability** to avoid conflicts. Co-hosts are not checked unless you include their calendars.
5. Booking page: location and conferencing (Google Meet, in-person, phone call, or none / to be specified later), description, booking form (first name, last name, email are required; add items for more).
6. Tick **Require email verification** to curb spam bookings; it sends a code to people not signed in to a Google Account.
7. Confirmations and reminders: up to 5 reminders; reminder email text cannot be edited. Payments need a connected Stripe account.

## Gotchas
- For a third-party conferencing tool choose None / to be specified later, then add the link to each booked event.
- Resource calendars cannot receive appointments.

## Verify
- [ ] Book a test slot while signed out: the event lands on your calendar, the confirmation arrives and the buffer is respected.

## Checked
2026-10-27. Google Calendar Help "Create an appointment schedule" (current page). Confirmed every setting named above, the 4-hour default lead time, 5 reminders, web-only creation and the subscription note. Removed Microsoft Bookings and Calendly claims and booker time-zone behaviour, which were not confirmed.
Method: documentation only; no commands were run.
