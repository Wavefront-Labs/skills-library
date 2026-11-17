---
id: computing-software.computer-graphics-engineering.computer-vision.image-colorization
name: image-colorization
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, comp-photo-cv, image-colorization, lab-color-space, opencv-dnn, ddcolor, photo-restoration]
level: practitioner
status: draft
description: "Colourise greyscale images: Lab-space formulation, Zhang et al. model in OpenCV DNN, modern diffusion/DDColor models, user hints, and keeping the original luminance."
sources: ["https://richzhang.github.io/colorization/", "https://github.com/opencv/opencv/blob/4.x/samples/dnn/colorization.py", "https://github.com/piddnad/DDColor"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Colourisation

## Formulation
Predict chrominance (a, b in Lab) from luminance L, then recombine with the **original full-resolution L**.
This keeps all the detail of the input and lets the network run at low resolution (224 to 512 px).

## OpenCV DNN (Zhang et al. 2016)
```python
net = cv2.dnn.readNetFromCaffe("colorization_deploy_v2.prototxt", "colorization_release_v2.caffemodel")
pts = np.load("pts_in_hull.npy").transpose().reshape(2, 313, 1, 1)
net.getLayer(net.getLayerId("class8_ab")).blobs = [pts.astype(np.float32)]
net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full((1, 313), 2.606, np.float32)]
lab = cv2.cvtColor(img.astype(np.float32) / 255, cv2.COLOR_BGR2Lab)
L = cv2.resize(lab[..., 0], (224, 224)) - 50
net.setInput(cv2.dnn.blobFromImage(L))
ab = cv2.resize(net.forward()[0].transpose(1, 2, 0), img.shape[1::-1])
out = cv2.cvtColor(np.dstack([lab[..., 0], ab]), cv2.COLOR_Lab2BGR)
```
Use float32 images in [0,1] for `cvtColor` so L is in [0,100] and ab in about [-128,127].

## Better models
DDColor, BigColor and diffusion-based colourisers give more vivid and plausible colours; DeOldify
remains popular for photos and film. Expect hallucinated colours: there is no single correct answer.

## Hints and control
User colour scribbles or reference images (exemplar-based colourisation) fix wrong colours for
known objects (uniforms, logos). Restoration workflows: denoise, deblur, fix scratches **before**
colourising.

## Video
Per-frame colourisation flickers; propagate colour from keyframes with optical flow or use video
models.

## Verify
On colour photos converted to grey: colourfulness metric and FID/LPIPS vs originals, but mainly human
review; check skin tones and sky.
