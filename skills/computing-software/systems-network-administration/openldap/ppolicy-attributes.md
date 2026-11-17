---
id: computing-software.systems-network-administration.openldap.ppolicy-attributes
name: ppolicy-attributes
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, pwdpolicy, pwdlockout, pwdmaxage, password-policy, pwdcheckquality, ppolicy]
level: advanced
status: docs-checked
description: "Set OpenLDAP pwdPolicy attributes: age, history, quality, length, lockout, grace logins, must-change and delays, with the meaning of zero or absent values."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-ppolicy&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pwdPolicy attributes
Set on a policy entry used by the ppolicy overlay (values in seconds unless noted):
- `pwdMinAge` (0: change any time); `pwdMaxAge` (absent or 0: never expires).
- `pwdInHistory`: old passwords kept in `pwdHistory` (absent or 0: no reuse check).
- `pwdCheckQuality`: 0 no check; 1 check and accept if unable; 2 check and refuse if unable.
- `pwdMinLength`, `pwdMaxLength`: bytes, need quality checking on.
- `pwdExpireWarning`: warn this long before expiry.
- `pwdGraceAuthnLimit`: logins allowed with an expired password; `pwdGraceExpiry` limits how long.
- `pwdLockout` TRUE enables lockout; `pwdMaxFailure` consecutive failures (0: unlimited); `pwdLockoutDuration` (0: until an admin resets); `pwdFailureCountInterval` (0: reset only on success); `pwdMaxRecordedFailure` (falls back to pwdMaxFailure, then 5).
- `pwdMustChange` TRUE forces a change after an admin sets or resets the password.
- `pwdAllowUserChange` (default TRUE; prefer ACLs); `pwdSafeModify` requires the old password.
- `pwdMinDelay` / `pwdMaxDelay` must be paired; implemented as variable lockout, not delayed responses.
- `pwdMaxIdle` locks unused accounts; needs `olcLastBind` TRUE.
- `pwdUseCheckModule`, `pwdCheckModuleArg` for `ppolicy_check_module`.

Operational state: `pwdChangedTime`, `pwdAccountLockedTime`, `pwdFailureTime`, `pwdHistory`, `pwdGraceUseTime`, `pwdReset`, `pwdStartTime`, `pwdEndTime`, `pwdPolicySubentry`.

Gotchas: lockout works only with `pwdLockout TRUE`; length limits count bytes; a `pwdStartTime` at or after `pwdEndTime` disables the account.

## Checked

2026-11-04. Confirmed against slapo-ppolicy(5): pwdMinAge, pwdMaxAge, pwdInHistory (rootdn exempt from history check), pwdCheckQuality 0/1/2 semantics, pwdMinLength and pwdMaxLength in bytes, pwdExpireWarning, pwdGraceAuthnLimit and pwdGraceExpiry, pwdLockout, pwdLockoutDuration, pwdMaxFailure, pwdMaxRecordedFailure fallback to pwdMaxFailure then 5, pwdFailureCountInterval, pwdMustChange, pwdAllowUserChange (ACLs preferred), pwdSafeModify, pwdMinDelay and pwdMaxDelay pairing with variable lockout, pwdMaxIdle needing olcLastBind TRUE, pwdUseCheckModule and pwdCheckModuleArg, the operational attributes and the pwdStartTime at or after pwdEndTime note.

Method: documentation only; no commands were run.
