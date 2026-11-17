---
id: computing-software.cloud-infrastructure-engineering.azure.azure-import-export-jobs-with-own-disks
name: azure-import-export-jobs-with-own-disks
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, import-export-service, waimportexport, offline-transfer, bitlocker, data-migration]
level: practitioner
status: docs-checked
description: "Ship your own disks to Azure with the Import/Export service: drive prep with WAImportExport, dataset and driveset CSVs, job creation, shipping and verifying the import."
sources: ["https://learn.microsoft.com/azure/import-export/storage-import-export-service", "https://learn.microsoft.com/azure/import-export/storage-import-export-data-to-blobs", "https://learn.microsoft.com/azure/import-export/storage-import-export-tool-preparing-hard-drives-import"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Import/Export with your own disks

**Goal:** move tens of TB offline when the network is too slow and Data Box isn't available or suitable.

## When to use
- Data Box devices unavailable in the region/country, or you must use your own encrypted drives.
- Import to Blob or Azure Files; export from Blob only.
- Check the current drive and job limits on the service documentation before ordering.

## Prepare drives (Windows, WAImportExport tool)
`dataset.csv`:
```
BasePath,DstItemPathOrPrefix,ItemType,Disposition,MetadataFile,PropertiesFile
"<SOURCE_DIR>\","exports/",dir,rename,"None",None
```
`driveset.csv`:
```
DriveLetter,FormatOption,SilentOrPromptOnFormat,Encryption,ExistingBitLockerKey
G,Format,SilentMode,Encrypt,
```
```cmd
WAImportExport.exe PrepImport /j:job1.jrn /id:session1 /t:G /bk:<optional> /srcdir:<SOURCE_DIR> /dstdir:exports/ /blobtype:BlockBlob /skipwrite
WAImportExport.exe PrepImport /j:job1.jrn /id:session1 /sk:<storage-key> /InitialDriveSet:driveset.csv /DataSet:dataset.csv /logdir:<LOG_DIR>
```
Drives are BitLocker-encrypted; keep the journal (`.jrn`) files and BitLocker keys - you upload journals when creating the job.

## Create the job
Portal: Import/Export jobs (Data Box family) > Create > Import into Azure > storage account, journal files,
return shipping (carrier account), destination datacenter address shown after creation. Ship the drives, enter the
tracking number.

## Track and verify
- Watch the job status in the portal; review copy logs and errors (name conflicts, skipped files) before drives come back.
- Compare counts/sizes with the source; checksum critical sets.

## Gotchas
- Wrong storage account key or later key rotation before import breaks the job - keep keys stable until completed.
- Invalid blob names and long paths can be skipped or renamed per disposition.
- Turnaround is days to weeks including shipping - plan delta sync over the network afterwards.

## Verify
- [ ] Job Completed with zero errors in the copy log; delta sync brought data current; drives received back and wiped.

## Checked
2026-10-28. Confirmed on the Import/Export Learn pages: the service imports to Blob storage and Azure Files, exports from Blob storage, ships encrypted drives, and Data Box Disk is the Microsoft-supplied alternative. Removed (not on fetched pages): the 10-drive/SATA limits, the job state sequence, the log container name, NTFS-only. WAImportExport csv layouts were not verified against the tool page; the skill stays advisory on them.
Method: documentation only; no commands were run.
