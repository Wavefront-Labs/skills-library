---
id: computing-software.systems-network-administration.powershell.xml-and-json-parsing
name: xml-and-json-parsing
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-data, powershell-xml, convertfrom-json, select-xml, xpath, xml-namespaces, json, config-files]
level: practitioner
status: verified
description: "Read and modify XML and JSON config files with PowerShell: [xml] casting, XPath with namespaces, Select-Xml, safe saving, ConvertFrom-Json depth, hashtables and edits."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/select-xml
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/convertfrom-json
  - https://learn.microsoft.com/en-us/dotnet/api/system.xml.xmldocument
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XML and JSON parsing

## XML: load, query, edit, save
```powershell
$path = Join-Path $site.PhysicalPath 'web.config'
$xml  = [xml]::new(); $xml.PreserveWhitespace = $true
$xml.Load($path)                                     # Load() respects the file's declared encoding

$xml.configuration.appSettings.add | Where-Object key -eq 'Env' | ForEach-Object { $_.value = 'Prod' }

$node = $xml.CreateElement('add')
$node.SetAttribute('key', 'FeatureX'); $node.SetAttribute('value', 'true')
[void]$xml.configuration.appSettings.AppendChild($node)

Copy-Item $path "$path.bak"
$xml.Save($path)
```
- `[xml](Get-Content $path -Raw)` works, but `Get-Content` may mis-decode the file's encoding;
  `XmlDocument.Load()` honours the XML declaration.
- Dot-notation returns a **string** for elements holding only text and an element for those
  with children; a single child is a scalar, several are an array. Wrap with `@()`.
- `$xml.Save()` needs a full path: relative paths resolve against the process directory
  (`[Environment]::CurrentDirectory`), not `$PWD`.

## XPath, including namespaces
```powershell
Select-Xml -Path .\unattend.xml -XPath '//u:ComputerName' -Namespace @{ u = 'urn:schemas-microsoft-com:unattend' } |
  ForEach-Object { $_.Node.InnerText }

$ns = [System.Xml.XmlNamespaceManager]::new($xml.NameTable)
$ns.AddNamespace('t', 'http://schemas.microsoft.com/windows/2004/02/mit/task')
$xml.SelectNodes('//t:Exec/t:Command', $ns).InnerText
```
A default `xmlns="..."` means `//ComputerName` finds nothing; you must map a prefix even for
the default namespace. Scheduled task XML, unattend.xml, .csproj and GPO reports all do this.

## JSON: read, edit, write
```powershell
$cfg = Get-Content .\appsettings.json -Raw | ConvertFrom-Json
$cfg.Logging.LogLevel.Default = 'Warning'
$cfg | Add-Member -NotePropertyName FeatureFlags -NotePropertyValue @{ NewUi = $true } -Force
$cfg | ConvertTo-Json -Depth 10 | Set-Content .\appsettings.json -Encoding UTF8
```
- Use `-Raw`: `Get-Content f.json | ConvertFrom-Json` works through the pipeline on both versions, but `ConvertFrom-Json $lines` / `-InputObject` with an array of lines fails on 5.1 ("Cannot convert 'System.Object[]' to the type 'System.String'").
- Always pass `-Depth` to `ConvertTo-Json` on write-back (default 2 silently flattens).
- `ConvertFrom-Json -AsHashtable` (PS 6+) for keys with odd characters, keys differing only by
  case, or when you need `ContainsKey`. 5.1 has no `-AsHashtable`.
- PS 7 `ConvertFrom-Json` turns ISO date strings into `[datetime]` (5.1 leaves a string); `-DateKind String` keeps them as text (in the 7.5 and 7.6 references, absent from 7.4).
- 5.1 cannot parse JSON with `//` or `/* */` comments or trailing commas (it throws); 7.6.7 accepted a `//` comment and a trailing comma.
- `Test-Json -Schema` (PS 6.1+) validates against a JSON schema.

Run on 5.1 and 7.6.7: `Load()` keeping a UTF-16 declaration, relative `Save('rel.xml')` landing in `[Environment]::CurrentDirectory` (not `$PWD`), the default-namespace XPath returning 0 nodes until a prefix is mapped, `Select-Xml -Namespace`, `ConvertTo-Json` truncating at depth 2 (a `"@{c=}"` string, plus a warning on 7), and `Test-Json -Schema` returning False/True (cmdlet absent on 5.1).

## Verify
- [ ] A diff of the file before and after shows only the intended change (whitespace preserved).
- [ ] The edited file loads in its application (for IIS, `Get-WebConfiguration` succeeds).
