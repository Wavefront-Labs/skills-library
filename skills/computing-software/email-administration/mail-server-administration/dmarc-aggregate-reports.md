---
id: computing-software.email-administration.mail-server-administration.dmarc-aggregate-reports
name: dmarc-aggregate-reports
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dmarc-aggregate-reports, dmarc-rua, aggregate-reports, dmarc-report-parsing]
level: practitioner
status: docs-checked
description: "Receive and parse DMARC aggregate (rua) XML reports to inventory legitimate and unauthorised senders."
sources:
  - https://www.rfc-editor.org/rfc/rfc7489
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dmarc aggregate reports

**Goal:** use reports to find who sends as you.
## Steps
1. Publish `rua=mailto:...` in the DMARC record and receive reports at a dedicated mailbox. The aggregate data is an XML file that SHOULD be gzip-compressed (media type `application/gzip`, otherwise `text/xml`) inside a MIME email.
2. Parse the XML with a script or a tool of your choice; group by source IP, SPF and DKIM results and the applied disposition.
3. Map each IP to a known service; fix SPF/DKIM for legitimate ones; investigate unknown ones.
4. Keep a running source inventory in version control.
5. When a report contains mail relayed by forwarders, the policy-override reasons in the report schema include `forwarded` and `trusted_forwarder`; read those rows separately.
## Failure modes
- Mailbox quota fills with reports; automate processing. The RFC notes a commonly observed receiver size limit of ten megabytes, which is why compression is recommended.
- If the `rua` address is in a different domain from the policy domain, that domain must publish an authorization TXT record `example.com._report._dmarc.<reporting-domain>` containing at least `v=DMARC1`, or reports are not sent.
## Verify
- After a fix, a previously failing source shows a pass in subsequent reports.

## Checked

2026-11-09. Confirmed on RFC 7489: the aggregate report as XML that SHOULD be gzip compressed, the application/gzip and text/xml media types, the ten megabyte receiver limit remark, the external reporting authorization record under _report._dmarc, and the forwarded and trusted_forwarder override reasons. Removed: the zip attachment claim (the RFC specifies gzip), the parsedmarc name, and the sampling remark; the Postfix/Dovecot notes were boilerplate.

Method: documentation only; no commands were run.
