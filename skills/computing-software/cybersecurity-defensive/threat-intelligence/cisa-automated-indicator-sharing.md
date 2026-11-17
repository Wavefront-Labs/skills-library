---
id: computing-software.cybersecurity-defensive.threat-intelligence.cisa-automated-indicator-sharing
name: cisa-automated-indicator-sharing
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [automated-indicator-sharing, information-sharing, cisa-ais, taxii, threat-intel-feeds]
level: practitioner
status: docs-checked
description: "Participate in CISA Automated Indicator Sharing (AIS): onboarding steps, TAXII 2.1 client connection, ISAC relay, and handling feed confidence and noise in your own platform."
sources: ["https://www.cisa.gov/topics/cyber-threats-and-advisories/information-sharing/automated-indicator-sharing-ais"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CISA Automated Indicator Sharing (AIS)

AIS is CISA's no-cost service for exchanging cyber threat indicators and defensive measures,
using TAXII 2.1.

## Onboarding (per the CISA page)
1. Contact CISA for engagement and technical help.
2. Agree to the Terms of Use (non-federal organisations) or the MISA (federal organisations).
3. Obtain a STIX/TAXII capability: the page asks for an open-source TAXII 2.1 client.
4. Obtain a PKI certificate from a Federal Bridge Certificate Authority (the page notes it may need purchasing).
5. Sign an Interconnection Agreement and provide your IP address.

Alternative: share through a participating ISAC or ISAO, or through an AIS-integrated commercial product or service.
Use the contact details on the CISA page for onboarding questions.

## Consuming
Volume is high and confidence variable (your platform's responsibility, not a CISA guarantee):
ingest into your threat intelligence platform, apply decay, export to controls only above a confidence
threshold, preferably as detection (alert) rather than block.

## Submitting
Remove personal information from indicators before sharing. Liability, privacy and other protections
under the Cybersecurity Information Sharing Act apply to sharing through AIS only if the Act's requirements
are followed; have counsel confirm.

## Gotchas
- Certificate expiry silently stops the feed; monitor last successful poll.
- Raw volume overwhelms SIEM IOC matching; curate.

## Verify
Your platform shows collection polls succeeding on schedule; sample of AIS-derived detections reviewed for false positives.

## Checked
2026-11-01. Confirmed on the CISA AIS page: no-cost service, TAXII 2.1 client, Terms of Use vs MISA, PKI certificate from a Federal Bridge CA, Interconnection Agreement and IP address, ISAC/ISAO and commercial relay, CISA 2015 protections conditional on the Act's requirements. Removed: STIX 2.1 and AIS scoring framework claims, TLP and AIS STIX profile, submitter anonymisation, web form, PKI-via-commercial wording, named platforms, daily poll; the page does not state them.
Method: documentation only; no commands were run.
