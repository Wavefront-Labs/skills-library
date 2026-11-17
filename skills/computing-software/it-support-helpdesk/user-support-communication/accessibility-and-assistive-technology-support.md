---
id: computing-software.it-support-helpdesk.user-support-communication.accessibility-and-assistive-technology-support
name: accessibility-and-assistive-technology-support
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, accessibility, assistive-technology, screen-reader, narrator, jaws, nvda, voiceover, closed-captioning, ada, wcag, reasonable-accommodation, magnifier, switch-access]
level: practitioner
status: draft
description: "Support users with disabilities over the helpdesk: screen readers, OS accessibility settings, captioning, assistive hardware, and reasonable-accommodation process awareness."
sources:
  - "https://www.w3.org/WAI/fundamentals/accessibility-principles/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# accessibility-and-assistive-technology-support

Goal: provide effective remote/phone support to a user relying on
assistive technology — this requires adjusting both the technical
approach (don't assume mouse/visual interaction) and the communication
approach from `ticket-communication-and-escalation`'s general guidance.

## Screen readers: the basics a sighted agent needs
- **Windows**: built-in **Narrator** (Win+Ctrl+Enter to toggle) plus
  third-party **JAWS** and **NVDA** (free, open source) are the common
  ones — know that a user's muscle memory and keyboard shortcuts differ
  *between* screen readers, so "press Tab then Enter" guidance that
  works for an NVDA user may not map directly to a JAWS user's
  configured shortcuts; ask which screen reader and, if unsure,
  describe the goal ("move focus to the Submit button") rather than a
  specific keystroke you're assuming applies.
- **macOS**: **VoiceOver** (Cmd+F5 to toggle) has its own gesture/keyboard
  command set (VO modifier key combos) distinct from standard macOS
  shortcuts — don't give standard mouse-click instructions ("click the
  X in the corner") to a VoiceOver user; describe it in terms of
  navigating to and activating the element.
- Remote-support implication: a screen-reader user's screen may be
  visually blank or scrambled-looking to a sighted agent even when the
  user is actively and correctly using it — don't assume something is
  broken because the screen "looks wrong"; ask what the screen reader is
  announcing before concluding there's a fault.

## OS accessibility settings a helpdesk tech should know how to find
- **Windows**: Settings → Accessibility (Narrator, Magnifier, high
  contrast/color filters, closed captions, sticky keys, eye control if
  supported hardware is present).
- **macOS**: System Settings → Accessibility (VoiceOver, Zoom, Display
  accommodations, Switch Control).
- A ticket like "text is too small" or "I can't see the cursor" is
  often solved entirely in these panels (Magnifier, pointer size/color,
  high contrast themes) rather than a hardware or app-level fix — check
  here before escalating.

## Captioning and communication accommodations
- Live captions (Windows: Settings → Accessibility → Captions; many
  conferencing tools have built-in live captioning) help users who are
  deaf/hard of hearing or who have auditory processing differences —
  know how to turn this on quickly during a support call/meeting rather
  than relying on the user to already have it configured.
- For a user who communicates via chat/text by preference or necessity,
  default to chat-based support rather than insisting on a phone call —
  forcing a channel switch to one that doesn't work for the user is
  itself a service failure, not a minor inconvenience.

## Assistive hardware
- Switch access devices, eye-tracking input, adaptive keyboards/mice,
  and specialized input devices connect like any peripheral but may need
  specific driver/software (vendor-provided control panels) — check for
  a vendor app/driver before assuming a standard peripheral
  troubleshooting approach applies; see
  `peripheral-and-display-troubleshooting` for the general USB/Bluetooth
  mechanics, which still apply underneath the specialized software.
- Sip-and-puff, head-tracking, and other low-incidence assistive devices
  are rare enough that most helpdesk staff won't have hands-on
  experience — for these, lean on the vendor's own support line/
  documentation rather than guessing, and loop in whoever in the org
  owns accommodations/disability services for configuration specifics.

## Reasonable accommodation process awareness
- A request for an accessibility accommodation (specific software,
  hardware, or a workflow change) may be a formal HR/legal process in
  many jurisdictions (e.g. under the ADA in the US, or equivalent
  frameworks elsewhere), not just a helpdesk ticket — **status: draft,
  verify against current law and your org's specific policy**: this
  note is a general pattern, not legal advice, and requirements vary
  significantly by jurisdiction and employer size.
- Helpdesk's role is typically to implement the accommodation once
  approved, and to flag to the accommodation/HR process when a request
  comes in through a support channel instead of the formal one — closing
  it as a routine ticket without that handoff can leave a legitimate
  accommodation request undocumented in the system meant to track it.

## Gotchas
- Don't default to assuming a disability from a ticket's content — ask
  what would help rather than guessing (e.g. a user asking for larger
  text may simply prefer it, not have a vision impairment; the fix is
  the same either way, but the framing of the conversation shouldn't
  presume).
- Remote-control tools that take over mouse/keyboard can actively
  conflict with a screen reader or switch-access setup mid-session —
  warn the user before taking control, and prefer guiding them to
  perform the action themselves when their assistive setup makes a
  takeover disruptive.

## Verify
- The user confirms (in their own words, via their preferred
  communication channel) that the configured setting/software behaves
  as expected with their specific assistive technology — a sighted
  agent's visual confirmation that "it looks right" is not sufficient
  verification for an accessibility fix.
