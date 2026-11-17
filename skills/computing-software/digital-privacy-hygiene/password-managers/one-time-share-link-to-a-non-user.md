---
id: computing-software.digital-privacy-hygiene.password-managers.one-time-share-link-to-a-non-user
name: one-time-share-link-to-a-non-user
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, one-time-share-link, password-sharing, 1password-item-sharing, bitwarden-send, expiring-link, max-access-count]
level: intro
status: docs-checked
description: "Send a credential to someone without a password manager via a 1Password share link or Bitwarden Send, with expiry, access limits and recipient restrictions."
sources:
  - "https://support.1password.com/share-items/"
  - "https://bitwarden.com/help/about-send/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharing a secret with a non-user by link

**Goal:** give a contractor or visitor a credential once, with an expiry, instead of leaving a
permanent copy in their inbox.

## 1Password item sharing
1. Select the item, then Share (on 1Password.com: the Share arrow; in the browser extension:
   ellipsis > Share, which opens 1Password.com).
2. Choose when the link expires and who can open it: anyone with the link, or only specific email
   addresses (add each address; a business account can also enter a whole domain such as
   acme.com). Your choices are saved as the defaults for next time.
3. Copy Link and send it by email, text or another route. Recipients open it in a browser; if you
   entered their email address they must verify it first. They can view and copy the details until
   the link expires.
4. To change an item after sharing, update it and share a new link; the old copy does not change.
5. To stop sharing early: item > View history (or View Sharing History) > select the link >
   Delete Link. This lists active and expired links. Business admins can also delete links from
   the audit log.
- Items with individual files over 250 MB cannot be shared. Shared items containing files cannot
  be saved to a recipient's 1Password account. Business accounts need the "Copy and Share Items"
  and "View and Copy Passwords" vault permissions.

## Bitwarden Send
- Send carries text up to 1,000 encrypted characters, or files up to 500 MB (100 MB on mobile);
  file Sends need premium. Create it in the Send view of any app, then share the link by any
  channel.
- Lifespan: every Send has a deletion date, maximum 31 days, after which the Send and contents are
  purged. You can also set an expiration date and a maximum access count.
- Privacy options: a password, email-verified access for specific recipients, hiding your email
  address; text Sends can require the recipient to toggle visibility.
- The link holds no data about the contents, so the page says it is safe over intermediary
  communication services; content is decrypted only when a recipient opens it.
- Status icons in your list show password protected, disabled, expired, reached max access count,
  and pending deletion. An organisation's Manage Send and share policy can restrict Send.

## Verify
- [ ] After the expiry or access limit, the link no longer opens.
- [ ] For an email-restricted link, the intended recipient could verify and view it.

## Checked

Date 2026-11-08. Pages read in full: 1Password "Securely share 1Password items with anyone" and Bitwarden "About Send". Removed as not on those pages: the specific 1Password expiry presets and "View once", the claim that the key sits in the URL fragment, the separate-channel password advice, link-preview consumption, and the credential-rotation advice. Bitwarden's page names max access count but not example values.

Method: docs-only read of cited pages, 2026-11-08
