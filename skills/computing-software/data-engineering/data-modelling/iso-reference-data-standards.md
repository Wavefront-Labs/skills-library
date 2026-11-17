---
id: computing-software.data-engineering.data-modelling.iso-reference-data-standards
name: iso-reference-data-standards
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, iso-code-standards, iso-3166, iso-4217, reference-data, code-lists, bcp-47]
level: practitioner
status: draft
description: "Manage reference data with international standards: ISO 3166 countries, ISO 4217 currencies, BCP 47 languages; sourcing, versioning, legacy code mapping and tests."
sources:
  - https://www.iso.org/iso-3166-country-codes.html
  - https://www.iso.org/iso-4217-currency-codes.html
  - https://www.six-group.com/en/products-services/financial-information/data-standards.html
  - https://www.rfc-editor.org/info/bcp47
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Reference data standards (ISO country / currency codes)

Reference data is the small, slowly changing set of codes everything else uses. Use published standards instead of home-grown lists: they're unambiguous, stable and understood by partners.

## Standards to adopt
| Domain | Standard | Notes |
|---|---|---|
| Countries | ISO 3166-1 alpha-2 (`GB`), alpha-3 (`GBR`), numeric (`826`) | pick alpha-2 as the key; numeric survives renames |
| Subdivisions | ISO 3166-2 (`GB-SCT`, `US-CA`) | states, provinces |
| Currencies | ISO 4217 (`GBP`, numeric `826`, minor units `2`) | minor units drive rounding: JPY 0, KWD 3 |
| Languages/locales | BCP 47 (`en-GB`, `pt-BR`, `zh-Hant-TW`) built on ISO 639 / 15924 | |
| Locations/ports | UN/LOCODE (`GBLON`) | logistics |
| Units | UN/CEFACT Rec 20, UCUM | |
| Industry | NAICS, NACE, ISIC; ISO 10383 MIC for exchanges; ISO 17442 LEI for legal entities | |

## Sourcing and versioning
- Official maintenance: ISO 4217 lists are published by SIX on behalf of ISO (free XML), ISO 3166 by ISO (Online Browsing Platform; machine-readable data is licensed). Many teams use open mirrors (e.g. Unicode CLDR, `pycountry`, `iso4217` packages) - record which source and version.
- Load into a governed reference table with `valid_from/valid_to`, never hard-code in application code:
```sql
CREATE TABLE ref_currency (
  code CHAR(3) PRIMARY KEY, numeric_code CHAR(3), name TEXT, minor_units SMALLINT,
  valid_from DATE, valid_to DATE, source_version TEXT
);
```
- Codes get withdrawn and reassigned (ISO 4217: HRK withdrawn 2023 when Croatia adopted EUR; country renames like `TR` "Türkiye" keep the code). Keep withdrawn codes with `valid_to` so historical data still joins.

## Mapping legacy and partner codes
- Crosswalk tables: `source_system`, `source_code`, `standard_code`, effective dates.
- Common traps: `UK` vs `GB`, `EL` (EU usage for Greece) vs `GR`, `XK` (Kosovo, user-assigned, not official ISO), `EU` (reserved), free-text country names in various languages.
- Pseudo-currencies: `XAU` (gold), `XXX` (no currency), `XTS` (testing).

## Distribution
- Publish reference tables to every consumer from one place (warehouse shared schema, MDM reference data hub, or package with versioned releases).
- dbt: seeds for small lists (`seeds/ref_country.csv`) with tests; larger lists via ingestion.

## Tests
```yaml
# dbt
- name: orders
  columns:
    - name: currency_code
      tests:
        - relationships: { to: ref('ref_currency'), field: code }
    - name: country_code
      tests:
        - accepted_values: { values: "{{ var('active_country_codes') }}" }
```
Also test amounts respect `minor_units` (no fractional JPY).

## Verify
- [ ] All country/currency columns use standard codes and FK-test against governed reference tables.
- [ ] Reference tables record source and version; withdrawn codes retained with validity dates.
