---
id: computing-software.qa-testing-engineering.selenium.screenshots-and-print-to-pdf
name: screenshots-and-print-to-pdf
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [print-page, screenshots, selenium-interactions, element-screenshot, pdf-generation]
level: practitioner
status: docs-checked
description: "Capture evidence in Selenium: full-window and element screenshots, Firefox full-page screenshots, print page to PDF with PrintOptions, and attaching them on failure."
sources:
  - https://www.selenium.dev/documentation/webdriver/interactions/print_page/
  - https://www.selenium.dev/documentation/webdriver/browsers/firefox/
  - https://github.com/SeleniumHQ/selenium/tree/trunk/py/selenium/webdriver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Screenshots and print-to-PDF (Selenium)

## Screenshots
```java
File shot = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);          // viewport
Files.copy(shot.toPath(), Path.of("target/screens/checkout.png"), REPLACE_EXISTING);

byte[] el = driver.findElement(By.id("invoice")).getScreenshotAs(OutputType.BYTES); // element only

// Firefox full page
File full = ((FirefoxDriver) driver).getFullPageScreenshotAs(OutputType.FILE);
```
Python: `driver.save_screenshot("out.png")`, `element.screenshot("el.png")`, `driver.get_full_page_screenshot_as_file("full.png")` (Firefox).

## Print page to PDF (W3C Print, Selenium 4)
```java
PrintOptions opts = new PrintOptions();
opts.setPageRanges("1-2");
opts.setOrientation(PrintOptions.Orientation.PORTRAIT);
opts.setBackground(true);
Pdf pdf = ((PrintsPage) driver).print(opts);
Files.write(Path.of("target/invoice.pdf"), Base64.getDecoder().decode(pdf.getContent()));
```
```python
from selenium.webdriver.common.print_page_options import PrintOptions
opts = PrintOptions(); opts.page_ranges = ["1-2"]; opts.background = True
pdf_b64 = driver.print_page(opts)
```

## Attach on failure
- Hook your test framework's failure callback to save a screenshot and page source, named by test id and timestamp.

## Gotchas
- Screenshots and PDFs may contain personal data; store artifacts with retention limits.

## Verify
Failed tests in CI have a screenshot and page source attached, and printed PDFs open and contain expected text.

## Checked

Checked 2026-10-25 against the Selenium documentation source and the Selenium Python source (trunk, pushed 2026-10-23). Confirmed: `PrintOptions` orientation (PORTRAIT/LANDSCAPE), page ranges, background; `PrintsPage` and Python `print_page`; Firefox `getFullPageScreenshotAs` and `get_full_page_screenshot_as_file`; Python `save_screenshot` and `WebElement.screenshot`. Removed as undocumented: the Chromium CDP full-page recipe, the Chromium-headless-only printing claim, framework hook names, the visual-testing tool mentions and the sticky-header gotcha.

Method: documentation only; no commands were run.
