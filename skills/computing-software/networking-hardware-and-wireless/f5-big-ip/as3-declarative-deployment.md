---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.as3-declarative-deployment
name: as3-declarative-deployment
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, as3, declarative-deployment, application-services]
level: practitioner
status: draft
description: "Deploy BIG-IP configuration declaratively with AS3: post a declaration to /mgmt/shared/appsvcs/declare and manage tenants."
sources:
  - https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/latest/userguide/composing-a-declaration.html
  - https://clouddocs.f5.com/api/icontrol-rest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AS3 declarative application deployment

```
curl -sku admin:$PW https://bigip/mgmt/shared/appsvcs/info
curl -sku admin:$PW -H 'Content-Type: application/json' -X POST https://bigip/mgmt/shared/appsvcs/declare -d @decl.json
curl -sku admin:$PW https://bigip/mgmt/shared/appsvcs/declare/Tenant1
curl -sku admin:$PW -X DELETE https://bigip/mgmt/shared/appsvcs/declare/Tenant1
```
```
{
 "class": "AS3", "action": "deploy", "persist": true,
 "declaration": { "class": "ADC", "schemaVersion": "3.45.0", "id": "demo-1",
  "Tenant1": { "class": "Tenant",
   "App1": { "class": "Application", "template": "http",
     "serviceMain": { "class": "Service_HTTP", "virtualAddresses": ["10.1.10.100"], "pool": "web_pool" },
     "web_pool": { "class": "Pool", "monitors": ["http"], "members": [{ "servicePort": 80, "serverAddresses": ["10.1.20.11","10.1.20.12"] }] } } } } }
```
- AS3 is an iControl LX extension, installed as an RPM through the GUI (iApps > Package Management LX) or REST. The `schemaVersion` must not exceed the installed AS3 version.
- A tenant becomes a BIG-IP partition; AS3 owns everything in it. POSTing a declaration replaces the whole tenant: omitted apps are deleted. Do not edit AS3-owned objects by hand, as the next declare reverts them.
- Add `?show=full`, or `controls: { dryRun: true }`, to preview. Use `/declare?async=true` for large declarations and poll `/mgmt/shared/appsvcs/task/<id>`.
- Gotcha: GET `/declare` returns the stored declaration without secrets; keep your own copy in source control.

Verify: response `"results":[{"code":200,"message":"success"}]`, then `tmsh list ltm virtual /Tenant1/App1/serviceMain` shows the object.
