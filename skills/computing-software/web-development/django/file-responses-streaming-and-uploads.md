---
id: computing-software.web-development.django.file-responses-streaming-and-uploads
name: file-responses-streaming-and-uploads
category: computing-software
field: web-development
product: django
tags: [django, fileresponse, django-file-uploads, streaminghttpresponse, x-accel-redirect, media-files, storages, python, web-development]
level: practitioner
status: docs-checked
description: "Serving and receiving files in Django: FileResponse and streaming CSV, protected downloads via X-Accel-Redirect, upload handling, validation and storage backends."
sources:
  - https://docs.djangoproject.com/en/stable/ref/request-response/#fileresponse-objects
  - https://docs.djangoproject.com/en/stable/topics/http/file-uploads/
  - https://docs.djangoproject.com/en/stable/howto/outputting-csv/
  - https://django-storages.readthedocs.io/
  - https://nginx.org/en/docs/http/ngx_http_core_module.html#internal
  - https://docs.djangoproject.com/en/stable/topics/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File responses, streaming and uploads

**Goal:** large downloads without buffering, protected files served efficiently, uploads validated and stored outside the code tree.

## 1. FileResponse
```python
from django.http import FileResponse, Http404
def invoice_pdf(request, pk):
    inv = get_object_or_404(Invoice, pk=pk, owner=request.user)
    return FileResponse(inv.pdf.open("rb"), as_attachment=True, filename=f"invoice-{inv.number}.pdf")
```
Streams the file in chunks; `Content-Length` and `Content-Type` are set automatically when they can be guessed, and `as_attachment=True` sets `Content-Disposition: attachment`.

## 2. Streaming generated data
```python
import csv
class Echo:
    def write(self, value): return value
def export(request):
    writer = csv.writer(Echo())
    rows = Order.objects.filter(owner=request.user).values_list("id", "total").iterator(chunk_size=2000)
    resp = StreamingHttpResponse((writer.writerow(r) for r in rows), content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="orders.csv"'
    return resp
```
`.iterator()` avoids loading the queryset into memory. Long streams tie up a worker - consider async generation + emailed link for very large exports.

## 3. Protected files via the web server
Let Django authorise, nginx send:
```python
resp = HttpResponse()
resp["X-Accel-Redirect"] = f"/protected/{inv.pdf.name}"     # nginx: location /protected/ { internal; alias /srv/media/; }
return resp
```
For S3: return a short-lived presigned URL (`storage.url(name)` with `querystring_auth=True`, `AWS_QUERYSTRING_EXPIRE`).

## 4. Uploads
```python
class DocumentForm(forms.ModelForm):
    class Meta: model = Document; fields = ["file"]
    def clean_file(self):
        f = self.cleaned_data["file"]
        if f.size > 10 * 1024 * 1024: raise forms.ValidationError("Max 10 MB.")
        if not f.name.lower().endswith((".pdf", ".png", ".jpg")): raise forms.ValidationError("Unsupported type.")
        return f
# view: form = DocumentForm(request.POST, request.FILES)
```
- Template form needs `enctype="multipart/form-data"`.
- Files > `FILE_UPLOAD_MAX_MEMORY_SIZE` (2.5 MB) go to a temp file. `DATA_UPLOAD_MAX_MEMORY_SIZE` limits non-file body size. Also cap at the proxy (`client_max_body_size`).
- `FileExtensionValidator` plus a check of the file content; Django's docs say not to trust the client-supplied `content_type`, and the extension is user-controlled too.
- `upload_to` callable generating random names; never trust the original filename for paths.

## 5. Storage
`MEDIA_ROOT` outside the repo; never serve user uploads from the same origin without `Content-Disposition: attachment` or a separate domain (stored XSS via HTML/SVG). Django 4.2+ `STORAGES = {"default": {"BACKEND": "storages.backends.s3.S3Storage"}, "staticfiles": {...}}`.

## Verify
- [ ] A 1 GB download keeps worker memory flat.
- [ ] Another user's file URL returns 404; direct `/protected/` access is blocked by nginx `internal`.
- [ ] Uploading an `.html`/`.svg` disguised as an image is rejected or served as attachment.

## Checked
Date: 2026-10-25. Documentation: Django documentation source (django/django main branch, 6.2 in development, commit of 2026-10-23; release notes 4.0 to 6.0) (ref/request-response FileResponse and StreamingHttpResponse, topics/http/file-uploads, howto/outputting-csv, topics/security user-uploaded content, ref/validators, ref/settings), nginx documentation source (nginx/nginx.org: internal, X-Accel-Redirect), django-storages docs source.
Confirmed: `FileResponse(open_file, as_attachment, filename)` header behaviour, the `Echo` CSV streaming pattern, `FILE_UPLOAD_MAX_MEMORY_SIZE` 2.5 MB default, `DATA_UPLOAD_MAX_MEMORY_SIZE` excludes file data, nginx `internal` locations return 404 to external requests and `X-Accel-Redirect` performs an internal redirect, `client_max_body_size`, `FileExtensionValidator`, S3Storage `querystring_auth` and `AWS_QUERYSTRING_EXPIRE`, Django 4.2+ `STORAGES`, the stored HTML-as-image risk and distinct-domain advice.
Corrected or removed: the claim that FileResponse always sets Content-Disposition, the empty Content-Type line, the unconfirmed Apache `X-Sendfile` note and the python-magic recommendation.
Method: documentation only; no commands were run.
