---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dlp-image-redaction
name: dlp-image-redaction
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sensitive-data-protection, image-redaction, dlp-images, ocr, pii]
level: practitioner
status: docs-checked
description: "Redact sensitive text from images with Sensitive Data Protection's image:redact: OCR infoType detection, redaction colours, redact-all-text, supported types and checking results."
sources: ["https://docs.cloud.google.com/sensitive-data-protection/docs/redacting-sensitive-data-images", "https://docs.cloud.google.com/sensitive-data-protection/docs/reference/rest/v2/projects.image/redact", "https://dlp.googleapis.com/$discovery/rest?version=v2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DLP image redaction

`projects.locations.image:redact` runs OCR on an image, finds infoTypes and returns the image with boxes drawn over matches.

## 1. Request
```bash
IMG=$(base64 -w0 id-card.png)
cat > req.json <<EOF
{
  "byteItem": {"type": "IMAGE_PNG", "data": "$IMG"},
  "inspectConfig": {"infoTypes": [{"name":"PERSON_NAME"},{"name":"DATE_OF_BIRTH"},{"name":"US_SOCIAL_SECURITY_NUMBER"},{"name":"EMAIL_ADDRESS"}],
                    "minLikelihood": "POSSIBLE"},
  "imageRedactionConfigs": [
    {"infoType": {"name":"PERSON_NAME"}, "redactionColor": {"red":0,"green":0,"blue":0}},
    {"infoType": {"name":"EMAIL_ADDRESS"}}],
  "includeFindings": true
}
EOF
curl -s -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" \
  "https://dlp.googleapis.com/v2/projects/<P>/locations/global/image:redact" -d @req.json \
  | jq -r .redactedImage | base64 -d > id-card.redacted.png
```
- `{"redactAllText": true}` as an `imageRedactionConfigs` entry redacts all text found in the image whether or not it matches an infoType; give only one such entry.
- `redactionColor` defaults to black when omitted.
- `inspectResult` (the findings) is populated in the response only when `includeFindings` is true.
- Content type: the how-to page lists JPEG, BMP and PNG as redactable and says content redaction is not supported for SVG, PDF, XLSX, PPTX or DOCX. The REST reference says the byte item "must be PNG, JPEG, SVG or BMP"; test SVG before relying on it.
- The method has limits on input size, processing time and output size: read the method reference for the current limits.

## 2. At scale
For buckets of images, use an inspection or de-identification job over Cloud Storage, or batch calls from Cloud Run with concurrency limits. Check the Sensitive Data Protection docs for which file types each job type supports.

## Gotchas
- OCR drives recall: low-resolution or rotated images can miss text. Pre-process (deskew, upscale).
- Keep humans in the loop for high-risk documents; detection is probabilistic.
- Only the first frame of a multiframe image is redacted; metadata and other frames are omitted in the response.
- Large images are slower to process; see the vendor's pricing page for how inspection is billed.

## Verify
- [ ] `includeFindings` lists the expected findings; visual check of a sample set; re-inspecting the redacted image finds nothing above the threshold.

## Checked
2026-10-31. Confirmed in the Sensitive Data Protection "Redacting sensitive data in images" page, the projects.image.redact reference and the DLP v2 discovery document: the `image:redact` path, `byteItem`, `imageRedactionConfigs`, `redactAllText`, `redactionColor` (default black), `includeFindings`, `redactedImage`, `inspectResult`, supported and unsupported types, first-frame-only behaviour. Removed: the ~4 MB request limit, the PASSPORT infoType example, the EXIF claim (the reference says metadata is omitted), the handwriting claim (the page shows a handwritten number masked), the inspection-job OCR claim and the per-byte billing claim, none of which the pages support.
Method: documentation only; no commands were run.
