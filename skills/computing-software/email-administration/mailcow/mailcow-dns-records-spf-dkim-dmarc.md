---
id: computing-software.email-administration.mailcow.mailcow-dns-records-spf-dkim-dmarc
name: mailcow-dns-records-spf-dkim-dmarc
category: computing-software
field: email-administration
product: mailcow
tags: [dns, mx-record, ptr-record, spf, dkim, dmarc, srv-records, autodiscover]
level: practitioner
status: docs-checked
description: "Publish the A, MX, autodiscover, SPF, DKIM, DMARC and SRV records and matching reverse DNS that each mailcow-managed domain needs."
sources: ["https://docs.mailcow.email/getstarted/prerequisite-dns/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mailcow DNS records: SPF, DKIM, DMARC

The PTR (reverse DNS) record of the server IP must match `MAILCOW_HOSTNAME`, for IPv4 and IPv6 alike; it is set at the provider that leases the IP.

Minimal set for each domain (shown with a host named `mail`):
- `mail` A record to the server IP (only on the domain that hosts the web interface)
- `autodiscover` and `autoconfig` CNAME to the mailcow hostname
- `@` MX 10 to the mailcow hostname

Authentication records:
- SPF: `"v=spf1 mx a -all"` allows only this MX to send for the domain.
- DKIM: generate the key in the mailcow UI, then publish the TXT record at `dkim._domainkey` (`v=DKIM1; k=rsa; t=s; s=email; p=...`).
- DMARC: a TXT at `_dmarc` such as `"v=DMARC1; p=reject; rua=mailto:mailauth-reports@example.org"`.

Advanced: SRV records announce services for client auto-configuration (`_autodiscover._tcp` 443, `_imaps._tcp` 993, `_submissions._tcp` 465, `_sieve._tcp` 4190, `_caldavs._tcp` and `_carddavs._tcp` with a TXT `path=/SOGo/dav/`). A target of `.` announces a service as not provided.

Verify with MX Toolbox, mail-tester or similar, or send a message to `check-auth at verifier.port25.com` for an SPF, DKIM and iprev report. If you ask for DMARC reports to a mailcow mailbox that is not set up to receive them, results will be incomplete; consider a separate domain for reports.

## Checked

2026-11-04. Confirmed on the DNS setup page: PTR matching MAILCOW_HOSTNAME for IPv4 and IPv6, the minimal A, CNAME and MX set and the note that the A record belongs only on the web-interface domain, the SPF, DKIM and DMARC example values, the SRV and TXT path records, the "." target for unprovided services, the testing tools, the DMARC report caveat and the port25 verifier address. No changes needed.

Method: documentation only; no commands were run.
