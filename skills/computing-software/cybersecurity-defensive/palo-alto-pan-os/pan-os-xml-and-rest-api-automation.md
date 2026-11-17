---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-xml-and-rest-api-automation
name: pan-os-xml-and-rest-api-automation
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [pan-os-xml-api, pan-os, rest-api, api-key, keygen, xpath, op-command, commit-api]
level: practitioner
status: draft
description: "Automate PAN-OS with the XML API and REST API - keygen, xpath get and set, operational commands, commit and job polling."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-panorama-api"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: scriptable, auditable changes without clicking.

Get a key (a role-limited service account, TLS verified):
```
curl --cacert ca.pem "https://fw.example.com/api/?type=keygen" --data-urlencode "user=api-svc" --data-urlencode "password=$PW"
export KEY=<value from response>
```
Operational command:
```
curl --cacert ca.pem -H "X-PAN-KEY: $KEY" "https://fw.example.com/api/?type=op&cmd=<show><system><info></info></system></show>"
```
Config set at an xpath (then commit):
```
curl --cacert ca.pem -H "X-PAN-KEY: $KEY" "https://fw.example.com/api/" \
  --data-urlencode "type=config" --data-urlencode "action=set" \
  --data-urlencode "xpath=/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/address" \
  --data-urlencode "element=<entry name='web01'><ip-netmask>10.1.1.10/32</ip-netmask></entry>"
curl --cacert ca.pem -H "X-PAN-KEY: $KEY" "https://fw.example.com/api/?type=commit&cmd=<commit></commit>"
```
Tip: run the setting in the GUI with `debug cli on` (CLI) or enable "Preview Changes"/"Show XML API" to obtain the xpath.

REST (v10.2+; confirm path version): `GET https://fw.example.com/restapi/v10.2/Objects/Addresses?location=vsys&vsys=vsys1` with the same header.

Gotchas
- Never use `-k` (insecure) beyond a lab; the key then travels unauthenticated.
- Commit returns a job id: poll with `type=op&cmd=<show><jobs><id>N</id></jobs></show>`; do not assume success.
- API keys act with the account's role; give the service account only the needed XML API sections.
- Concurrent API commits conflict with admins' commit locks.

## Verify
`show system info` through the API returns the version; after a commit the job result is `OK` and `type=config&action=get` returns the new element.
