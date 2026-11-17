---
id: computing-software.systems-network-administration.active-directory.ldap-filters-and-get-adobject
name: ldap-filters-and-get-adobject
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-users-and-groups, ldap-filter, get-adobject, ldapfilter, bitwise-filter, useraccountcontrol, in-chain-matching-rule, ranged-retrieval, searchbase, resultpagesize, activedirectory-module]
level: practitioner
status: docs-checked
description: "Write fast, correct AD queries: -Filter vs -LDAPFilter, bitwise userAccountControl matching, LDAP_MATCHING_RULE_IN_CHAIN for nested groups, paging and indexed attributes."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/adsi/search-filter-syntax
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-adobject
  - https://learn.microsoft.com/en-us/windows/win32/adschema/a-useraccountcontrol
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP filters and Get-ADObject

## Two filter syntaxes
- `-Filter` (PowerShell expression language, converted to LDAP): `Get-ADUser -Filter "Department -eq 'Finance' -and Enabled -eq 'True'"`
- `-LDAPFilter` (raw LDAP query string): `Get-ADUser -LDAPFilter '(&(department=Finance)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))'`
Use LDAP for matching rules and anything the converter mishandles.

## Useful patterns
```text
(&(objectCategory=person)(objectClass=user))           real users
(userAccountControl:1.2.840.113556.1.4.803:=2)          disabled (bitwise AND, ACCOUNTDISABLE 0x2)
(userAccountControl:1.2.840.113556.1.4.803:=65536)      password never expires (DONT_EXPIRE_PASSWD 0x10000)
(userAccountControl:1.2.840.113556.1.4.803:=524288)     trusted for (unconstrained) delegation (0x80000)
(servicePrincipalName=*)                                has an SPN
(memberOf:1.2.840.113556.1.4.1941:=CN=GG-Finance,OU=Groups,DC=ad,DC=example,DC=com)  nested membership
(pwdLastSet=0)                                           must change password at next logon
```
`1.2.840.113556.1.4.803` is LDAP_MATCHING_RULE_BIT_AND, `.804` is BIT_OR, and `.1941` is LDAP_MATCHING_RULE_IN_CHAIN,
which walks the chain of ancestry and is limited to DN-valued attributes such as `memberOf`.
`pwdLastSet=0` forces a change unless the account has the never-expires flag.

## Scope and paging
```powershell
Get-ADObject -LDAPFilter '(objectClass=computer)' -SearchBase 'OU=Servers,DC=ad,DC=example,DC=com' `
  -SearchScope Subtree -Properties operatingSystem -ResultPageSize 1000 -Server dc01
```
- `-SearchBase`, `-SearchScope`, `-ResultPageSize`, `-ResultSetSize` and `-Properties` are standard Get-ADObject
  parameters; ask only for the properties you need.
- Deleted objects: add `-IncludeDeletedObjects`.
- Forest-wide search: connect to a global catalog port (`-Server <gc>:3268`). With an empty `-SearchBase` on a GC port
  all partitions are searched; on a non-GC port that raises an error. A GC holds only a partial attribute set.

## Verify
- [ ] Compare result counts between `-Filter` and `-LDAPFilter` versions on a known set.
- [ ] Expensive queries are absent from DC event 1644 logs (see LDAP performance skill).

## Checked
2026-10-27. Documentation: Microsoft Learn LDAP search filter syntax, `Get-ADObject` reference and the
userAccountControl schema page. Confirmed: matching-rule OIDs .803 (BIT_AND), .804 (BIT_OR) and .1941 (IN_CHAIN) and the
DN-only limit for in-chain; flag values 0x2, 0x10000 and 0x80000; `pwdLastSet` 0 behaviour; Get-ADObject parameters
(`-LDAPFilter`, `-SearchBase`, `-SearchScope`, `-ResultPageSize`, `-IncludeDeletedObjects`, `-Properties`); GC port 3268
and the empty-search-base behaviour. Removed as unconfirmed: the objectCategory-is-indexed and leading-wildcard remarks,
the adminCount and generalized-time examples, ranged-retrieval details, and the `-Filter` script-block and `$null` gotchas.
Method: documentation only; no commands were run.
