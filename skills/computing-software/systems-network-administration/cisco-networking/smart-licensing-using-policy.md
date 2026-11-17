---
id: computing-software.systems-network-administration.cisco-networking.smart-licensing-using-policy
name: smart-licensing-using-policy
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, smart-licensing, slup, license-boot-level, cslu, rum-report, dna-advantage]
level: practitioner
status: draft
description: "Run Cisco Smart Licensing Using Policy on IOS XE: license boot level, CSSM direct/CSLU/offline reporting, RUM reports, trust codes, and clearing not-reported warnings."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lic/b_179_lic_9300_cg.html
  - https://www.cisco.com/c/en/us/support/docs/licensing/enterprise-agreement/217308-smart-licensing-using-policy-on-cisco.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smart Licensing Using Policy (SLUP)

Since IOS XE 17.3.2 licences are not "registered" any more. Features are enabled by the boot level;
usage is recorded as RUM reports which must reach Cisco Smart Software Manager (CSSM) within the
policy's reporting window.

## Set the feature level
```
license boot level network-advantage addon dna-advantage    ! Catalyst 9k
license boot level appxk9                                    ! ISR/Catalyst 8000 (some platforms use throughput levels)
write memory
reload                                                       ! boot level changes need a reload
show license summary
show version | include License Level
```

## Pick a reporting topology
- Direct to CSSM: device reaches smartreceiver.cisco.com over HTTPS.
  ```
  license smart transport smart
  license smart url default
  ip http client source-interface Vlan100
  license smart trust idtoken <token-from-CSSM> all force
  ```
- Via CSLU (Windows/Linux utility on-prem) or SSM On-Prem: `license smart transport cslu`,
  `license smart url cslu http://cslu.example.net:8182/cslu/v1/pi`.
- Air-gapped: save and upload manually.
  ```
  license smart save usage all file bootflash:rum.txt
  ! upload to CSSM, download ACK file
  license smart import bootflash:ack.txt
  ```

## Checking status
```
show license status          ! transport, last report, next ACK due
show license usage
show license tech support    ! for TAC
show license eventlog 2
```
`Trust Code Installed` and a recent `Last ACK received` mean you are compliant.

## Gotchas
- DNS and NTP must work for direct transport; certificate validation fails with a wrong clock.
- Use a source interface in the management VRF if the default VRF has no internet:
  `ip http client source-interface GigabitEthernet0/0` plus `license smart vrf Mgmt-vrf` where
  supported.
- Not reporting does not disable features today, but syslog fills with
  `%SMART_LIC-3-REPORTING_REQUIRED`; set up reporting rather than suppressing it.
- Stacks report per member serial; replacing a member generates new usage.
- Export-controlled features (HSECK9 for high IPsec throughput) still need an authorisation code
  installed before use.

## Verify
- [ ] `show license summary` shows the purchased level IN USE.
- [ ] `show license status` shows a recent ACK and the next report date.
