---
id: computing-software.systems-network-administration.dns-dhcp.arc-signing-for-forwarded-mail
name: arc-signing-for-forwarded-mail
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, arc-signing, arc, email-authentication, dkim, mail-forwarding]
level: practitioner
status: verified
description: "Understand and deploy ARC (Authenticated Received Chain) so forwarded and list mail keeps authentication results: header set, DNS keys, sealing and trust."
sources:
  - https://www.rfc-editor.org/rfc/rfc8617
  - https://www.rfc-editor.org/rfc/rfc8601
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARC

Forwarders and mailing lists break SPF (new sending IP) and often DKIM (modified subject/footer), so
DMARC fails at the final receiver. ARC lets each intermediary record the authentication results it
saw and seal them.

## Headers added per hop (instance i=1,2,...)
- `ARC-Authentication-Results: i=1; mx.lists.example; spf=pass ...; dkim=pass ...; dmarc=pass`
- `ARC-Message-Signature: i=1; a=rsa-sha256; d=lists.example; s=arc2026; ...` (DKIM-like signature over the message)
- `ARC-Seal: i=1; a=rsa-sha256; cv=none; d=lists.example; s=arc2026; ...` (signs the ARC headers; `cv=pass` for i>1)

## DNS
ARC uses DKIM-format keys:
```
arc2026._domainkey.lists.example. IN TXT "v=DKIM1; k=rsa; p=MIIBIjANBgkq..."
```
You may reuse your DKIM selector.

## Deploying (intermediary)
- Postfix/Sendmail: OpenARC milter, or rspamd `arc` module (`/etc/rspamd/local.d/arc.conf` with
  domain/selector/path like DKIM signing).
- Exchange Online lets you list trusted ARC sealers; `-Identity` is required and the value you pass replaces the
  list, so append to the existing one:
  `$d = @(Get-ArcConfig | select -Expand ArcTrustedSealers); $d += "lists.example"; Set-ArcConfig -Identity Default -ArcTrustedSealers $d`
  (Microsoft Learn, Set-ArcConfig). Check each provider's documentation for whether it seals its own forwarded mail.

## Receiving
Receivers decide whether to trust a sealer. A valid chain from a trusted sealer can override a
DMARC failure as local policy; RFC 8617 shows the aggregate report carrying a policy override reason
`<type>local_policy</type>` with a comment such as `arc=pass as[2].d=... as[1].d=...` (RFC 9990 also defines
`trusted_forwarder`).

## Check
Read the headers: the ARC-Seal with i=1 has `cv=none`; every later seal should have `cv=pass`. `cv=fail`
anywhere breaks the chain. Tested with dkimpy 1.1.8 `arc_sign` and `arc_verify` over two hops (needs the `authres`
package and an Authentication-Results header whose authserv-id matches the sealing server): the hop-2 seal had
`cv=pass`, the chain verified `pass`, and changing the body afterwards gave `fail` (`Most recent ARC-Message-Signature
did not validate`).

## Verify
- [ ] A message through the list arrives at Gmail/M365 with `arc=pass` in Authentication-Results and DMARC no longer failing.
