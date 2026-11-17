---
id: computing-software.cloud-infrastructure-engineering.graylog.data-node-certificate-policy
name: data-node-certificate-policy
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [certificate-authority, cert-renewal, client-certificate, data-node, tls]
level: practitioner
status: docs-checked
description: "Set Data Node certificate renewal mode and lifetime, renew certificates and issue client certificates for third-party tools."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/manage_certificates_with_data_node.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# data node certificate policy

Use the Configuration tab at **System > Cluster Configuration** (Certificate Management). If you upload your own CA you must configure Data Node certificates in the Data Node config file and manage them externally.

Policy (Edit configuration):
- **Renewal Mode**: Automatic (default) renews expiring certificates without action; Manual raises a system notification when certificates near expiry.
- **Certificate Lifetime**: validity of newly created certificates; default 30 days.

Manual renewal: Data Nodes tab, More menu, Renew certificate.

Third-party tools needing HTTPS access to OpenSearch require a client certificate. Choose Generate Client Certificate and give the Principal, the FQDN of the host you connect to. Generated certificates expire per the policy unless you set a different Certificate Lifetime, so they must be replaced on schedule.

## Checked

2026-11-04. Confirmed against the Manage Certificates with Data Node page (menu paths, renewal modes, 30 day default, manual renewal, client certificate Principal and lifetime). Nothing removed.

Method: documentation only; no commands were run.
