---
id: computing-software.cloud-infrastructure-engineering.graylog.inputs-types-and-launch
name: inputs-types-and-launch
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [input-types, input-setup, listener-input, pull-input, setup-wizard]
level: intro
status: docs-checked
description: "Pick and launch a Graylog input: listener versus pull inputs, TLS support, Illuminate packs and the Input Setup Wizard."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/inputs.htm
  - https://go2docs.graylog.org/current/getting_in_log_data/setup_an_input.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# inputs types and launch

Two kinds of input: **listener** (Graylog listens for sent data, for example Syslog, GELF, Beats) and **pull** (Graylog fetches from a service, for example AWS CloudTrail, AWS S3, Azure Event Hubs, GCP, Okta).

The inputs table lists type, TLS capability and any Illuminate pack. Examples: GELF supports TLS for HTTP and TCP only; CEF only for TCP; IPFIX has no TLS. If an Illuminate pack exists for the source, enable it before configuring the input to avoid duplicate entities.

Launch: **System > Inputs**, choose the type in Select input, Launch new input, enter settings, Launch input, then complete the **Input Setup Wizard**. Until the wizard is done the input is not running and logs do not flow; the Inputs page warns about inputs in setup mode, and you can restart the wizard with Set-up Input.

Use several inputs of one type to segment traffic, ideally with a load balancer and TCP.

## Checked

2026-11-04. Confirmed against the cited page. Nothing removed.

Method: documentation only; no commands were run.
