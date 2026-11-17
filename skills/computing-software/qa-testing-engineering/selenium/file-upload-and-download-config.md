---
id: computing-software.qa-testing-engineering.selenium.file-upload-and-download-config
name: file-upload-and-download-config
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [selenium-file-upload, file-download, download-directory, local-file-detector, chrome-prefs]
level: practitioner
status: gated
description: "Upload files with Selenium (send_keys, LocalFileDetector on Grid) and handle downloads via browser prefs, Grid managed downloads and verifying file contents."
sources:
  - https://www.selenium.dev/documentation/webdriver/elements/file_upload/
  - https://www.selenium.dev/documentation/webdriver/drivers/remote_webdriver/#managed-downloads
  - https://www.selenium.dev/documentation/test_practices/discouraged/file_downloads/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File upload and download configuration

## Upload
```python
inp = driver.find_element(By.CSS_SELECTOR, "input[type=file]")
inp.send_keys(str(Path("fixtures/invoice.pdf").resolve()))
inp.send_keys(f"{a}\n{b}")    # multiple files when input has 'multiple'
```
Hidden inputs (styled button triggers a hidden `<input type=file>`) still accepted `send_keys` on Chrome 156 (a `display:none` input fired `change`); if a driver refuses, make it visible via JS for the test. Paths must be absolute (a relative one raised `InvalidArgumentException: path is not absolute`); two paths joined by `\n` filled a `multiple` input with 2 files (ran).
Remote: `driver.file_detector = LocalFileDetector()` streams the local file to the node (gated: unconfirmed, source is paywalled or blocked) (no Grid here; the class imports from `selenium.webdriver.remote.file_detector`).

## Download (local)
```python
prefs = {"download.default_directory": str(tmp_dir), "download.prompt_for_download": False,
         "safebrowsing.enabled": True}
options.add_experimental_option("prefs", prefs)
```
Ran on Chrome 156: with these prefs a clicked `<a download>` landed in `tmp_dir` as `file.csv`. Firefox:
```python
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", str(tmp_dir))
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/pdf")
```
Ran on Firefox with `folderList=2`, `browser.download.dir` and `neverAsk.saveToDisk=text/csv`: the file was saved in the chosen folder. Wait for completion: poll for the file and absence of `.crdownload` / `.part`.

## Download (Grid managed downloads)
```python
options.enable_downloads = True
driver = webdriver.Remote("http://grid:4444", options=options)
# ... trigger download
names = driver.get_downloadable_files()
driver.download_file(names[0], str(tmp_dir))
driver.delete_downloadable_files()
```
The methods `get_downloadable_files`, `download_file` and `delete_downloadable_files` exist on `webdriver.Remote` in Selenium 4.51 and the Selenium docs describe enabling downloads in the Grid and the client, but the flow itself was not run (gated: unconfirmed, source is paywalled or blocked).

## Selenium's advice
The docs list file downloads as discouraged: the browser download isn't the app's logic. Often better: read the link `href` and fetch it with an HTTP client using the session cookies, then assert headers (`Content-Type`, `Content-Disposition`) and content.

## Gotchas
- Without the prefs, headless Chrome (`--headless=new`) saved the file to the user's default Downloads folder (ran), so set the prefs (or CDP `Browser.setDownloadBehavior`) to keep test output in a known directory.
- Use a unique download dir per test for parallel runs.

## Verify
Downloaded file exists, has expected size/headers and parses (CSV header, PDF magic bytes `%PDF`).
