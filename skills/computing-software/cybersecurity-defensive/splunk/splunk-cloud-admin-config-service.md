---
id: computing-software.cybersecurity-defensive.splunk.splunk-cloud-admin-config-service
name: splunk-cloud-admin-config-service
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, admin-config-service, acs, splunk-cloud, infrastructure-as-code, hec, ip-allow-list, terraform]
level: practitioner
status: draft
description: "Administer Splunk Cloud Platform with the Admin Config Service (ACS) API and CLI: indexes, HEC tokens, IP allow lists, app installs and outbound ports as code."
sources: ["https://docs.splunk.com/Documentation/SplunkCloud/latest/Config/ACSIntro", "https://docs.splunk.com/Documentation/SplunkCloud/latest/Config/ACSCLI", "https://registry.terraform.io/providers/splunk/scp/latest/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Splunk Cloud with the Admin Config Service

Splunk Cloud blocks shell access; ACS is the supported API for self-service admin.

## Auth
Create a JWT token in Splunk Web (Settings > Tokens) for a user with `sc_admin`. ACS base URL:
`https://admin.splunk.com/<STACK>/adminconfig/v2/`.

## CLI
```
acs login --token-user <user>                 # stores token per stack
acs config add-stack <STACK>
acs indexes create --name fw_pan --data-type event --searchable-days 90 --max-data-size-mb 0
acs hec-token create --name pan-hec --default-index fw_pan --allowed-indexes fw_pan
acs ip-allowlist create search-api --subnets 198.51.100.0/24
acs outbound-port create --port 8089 --subnets 203.0.113.10/32 --reason "federated search"
acs apps install splunkbase --splunkbase-id 1876 --acs-legal-ack Y
acs apps install private --app-package ./my_ta.tgz --acs-legal-ack Y   # runs AppInspect vetting
acs restarts                                   # restart-required status
```
Raw REST is equivalent: `curl -H "Authorization: Bearer <TOKEN>" .../adminconfig/v2/indexes`.

## As code
The `splunk/scp` Terraform provider manages indexes, HEC tokens, allow lists and roles via ACS.
Keep index definitions and HEC tokens in git; review changes by PR.

## Allow list features
`search-api`, `hec`, `s2s`, `search-ui`, `idm-api`, `idm-ui`, `acs`. Locking `acs` to your
admin network is the first hardening step; do not lock yourself out (keep current IP in the list).

## Gotchas
- Private app installs go through automated AppInspect; failures block install (fix the app).
- Some operations trigger a rolling restart; check `acs restarts` before batching changes.
- Rate limits apply; script retries with backoff.
- Victoria vs Classic experience differ (Classic needs IDM for inputs); check stack type.

## Verify
`acs indexes list` and `acs hec-token list` match the repo; a test HEC event to the new token
lands in the right index.
