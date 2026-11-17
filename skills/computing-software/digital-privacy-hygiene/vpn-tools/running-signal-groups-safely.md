---
id: computing-software.digital-privacy-hygiene.vpn-tools.running-signal-groups-safely
name: running-signal-groups-safely
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, signal-groups, signal, signal-messenger, group-admin, group-links, approve-new-members, disappearing-messages, organizing]
level: practitioner
status: docs-checked
description: "Create and administer a Signal group for organising: permissions, admins, group-link approval, disappearing timers, and what members can see."
sources:
  - "https://ssd.eff.org/module/creating-and-managing-signal-groups"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Signal groups safely

**Goal:** a group where unknown people can't quietly join, settings can't be changed by anyone, and members' exposure is limited.

## Create
Create the group, optionally skipping member selection if you will share a link or invite later. Name it and set
the disappearing-messages length at creation. Then tap the group name and scroll to Permissions: you can control
who can add members, who can edit group info (name, photo, disappearing timer) and who can send messages. Set to
"Only admins" for a managed group; "send messages: only admins" gives an announcement chat.

## Disappearing messages
Admins can set or change the timer via the group name, then Disappearing Messages. Set it when creating the group.
For sensitive chats a short period such as a day or a week protects members' privacy and leaves fewer messages if
someone's device is compromised.

## Group links
Group links (URLs starting with signal.group) are off by default and only admins can turn them on, off or change
the URL. They make it harder to know who joins over time; consider disabling after the first wave of invites. For
higher-risk contexts use invite-only or short-lived links and turn links off or reset them between events. If you
turn on a link, enable "Require Admin Approval"; pending requests appear under Requests & Invites. Signal has no
real-name requirement, so vet requesters, for example by asking where they heard of the group or having members
vouch. Tell members before first sharing a link so they can review their profile settings.

## Admins
For anything beyond a handful of friends, designate at least one or two admins; even in small groups consider two
trusted admins, rotate roles to prevent burnout, and agree when to hand over. Admins can approve or add members,
change group info, pin messages and remove people, so choose them carefully. Make someone an admin from the member
list (Make Admin, confirm); admin status can be revoked there too.

## Member exposure
- Everyone in your groups can see your display name and profile photo. In large groups with people you do not
  know, consider a name and photo that do not identify you.
- Check Privacy, Phone Number: "Who Can See My Number" and "Who Can Find Me By Number". If you set the latter to
  Nobody, you may want a username as a discovery handle; usernames are not display names.
- For small and medium groups, check the member list occasionally; for large groups this is often impractical
  because members are pseudonymous.

## Gotchas
- Removing someone does not delete old messages from their phone, and neither does setting a new timer. Deleting
  your own message within 24 hours removes it from everyone's phones in the group.
- If a member is under criminal investigation or their phone was seized, consult a lawyer before changing admin
  settings.

## Verify
- [ ] Permissions set to Only Admins where intended; link approval on, or link off.
- [ ] Disappearing timer set.

## Checked
Method: docs-checked 2026-11-09 against the EFF Surveillance Self-Defense page "Creating and managing Signal groups" (full page read, including the admin example). Dropped as unconfirmed: "reset link" as a Signal control by that name, "2-3 admins" figure, "split by purpose" advice, screenshot assumption for large groups, and the public link-preview gotcha. The support.signal.org source was removed because it could not be read.
