---
id: computing-software.systems-network-administration.active-directory.token-bloat-and-nested-groups
name: token-bloat-and-nested-groups
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-users-and-groups, token-bloat, nested-group-membership, maxtokensize, kerberos]
level: advanced
status: docs-checked
description: "Diagnose Kerberos token bloat from deep nesting and SID history: count token SIDs, MaxTokenSize limits, HTTP 400 header errors and group cleanup."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/kerberos-authentication-problems-if-user-belongs-to-groups
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/group-policy-add-maxtokensize-registry-entry
  - https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/iis/www-authentication-authorization/http-bad-request-response-kerberos
  - https://learn.microsoft.com/en-us/windows/win32/adschema/a-tokengroups
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Token bloat and nested group membership

Every group a user is in (directly, nested, and via SID history) becomes a SID in the Kerberos ticket's
authorization data. Too many and logons, IIS and SMB start failing.

## Symptoms
- Users in many groups cannot sign in or get `HTTP 400 Bad Request - Request Header Too Long` from IIS sites
  using Kerberos.
- On Windows Server 2012 and later, event ID 31 can be logged when the token size passes a threshold; enable it
  with the Group Policy setting described in the Microsoft article.

## Measure
```powershell
$u = Get-ADUser jdoe -Properties tokenGroups, sIDHistory
$u.tokenGroups.Count                 # transitive group SIDs (a computed attribute; needs a global catalog)
```
Microsoft's estimate for Windows Server 2012 and later: `TokenSize = 1200 + 40d + 8s` bytes, where `1200` is the
estimated ticket overhead, `d` = universal group memberships outside the user's account domain plus SIDs in
`sIDHistory`, and `s` = universal groups inside the account domain plus
domain-local and global group memberships. The default `MaxTokenSize` is 48,000 bytes on Windows Server 2012 and
later.
For HTTP, `http.sys` limits each header with `MaxFieldLength` (default 16,384 bytes) and the whole request line and
headers with `MaxRequestBytes` (default 16 KB).

Recursive membership report:
```powershell
Get-ADGroupMember 'App-Finance-RW' -Recursive | Measure-Object
Get-ADPrincipalGroupMembership jdoe | Select Name,GroupScope
```

## Fix (in order)
1. Remove stale SID history after migrations.
2. Flatten deep nesting; remove groups nobody uses (no ACL references) and duplicate role groups.
3. Use domain-local groups for resource permissions (AGDLP) and do not nest domain-local groups cross-domain
   needlessly.
4. Only then raise limits: `HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Kerberos\Parameters\MaxTokenSize`
   (REG_DWORD, maximum allowed 65535, but Microsoft does not recommend more than 48000 because of HTTP base64
   encoding) via the GPO "Set maximum Kerberos SSPI context token buffer size" (Computer Configuration > Policies >
   Administrative Templates > System > Kerberos; restart affected computers), and on IIS the `MaxFieldLength` /
   `MaxRequestBytes` values under `HKLM\SYSTEM\CurrentControlSet\Services\HTTP\Parameters`.

## Verify
- [ ] Problem users' tokenGroups count reduced; `klist` shows tickets; IIS 400 errors gone.

## Checked
2026-10-27. Documentation: Microsoft Learn Kerberos token-size article (Windows Server 2012-era formula),
MaxTokenSize Group Policy article, IIS HTTP 400 Kerberos article, Http.sys registry settings and the Token-Groups schema
page. Confirmed: formula `1200 + 40d + 8s` and the definitions of d and s for Windows Server 2012 and later; default
MaxTokenSize 48,000 bytes, registry path under Control\Lsa\Kerberos\Parameters, maximum 65535 with the 48000 caution; GPO
name and path; event ID 31; `MaxFieldLength` 16,384 and `MaxRequestBytes` 16 KB defaults; tokenGroups is a computed attribute
that needs a global catalog. Corrected: the draft put domain-local groups in `d`; for Windows Server 2012 and later they are
in `s`. The 16 KB-per-header wording was split into the two separate limits.
Method: documentation only; no commands were run.
