---
id: computing-software.computer-graphics-engineering.opencv.opencv-filestorage-yaml-json
name: opencv-filestorage-yaml-json
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-core, filestorage, yaml, json, calibration-persistence]
level: practitioner
status: docs-checked
description: "Persist OpenCV matrices, calibration and config with cv::FileStorage in YAML/JSON/XML, including nodes, sequences and Python access."
sources: ["https://docs.opencv.org/4.x/da/d56/classcv_1_1FileStorage.html", "https://docs.opencv.org/4.x/dd/d74/tutorial_file_input_output_with_xml_yml.html", "https://github.com/opencv/opencv/blob/4.x/modules/core/include/opencv2/core/persistence.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cv::FileStorage persistence

**Goal:** save and reload `Mat`s and parameters (camera intrinsics, thresholds) in a
human-editable file that both C++ and Python read.

## 1. Write
```cpp
cv::FileStorage fs("calib.yaml", cv::FileStorage::WRITE);   // .yml/.yaml, .json, .xml by extension
fs << "image_width" << 1920 << "image_height" << 1080;
fs << "camera_matrix" << K << "dist_coeffs" << D;            // Mats as !!opencv-matrix
fs << "frames" << "[";                                       // sequence
for (auto& f : names) fs << f;
fs << "]";
fs << "board" << "{" << "cols" << 9 << "rows" << 6 << "}";   // mapping
fs.release();
```
Append `.gz` to the filename to work with compressed files (for example `myHugeMatrix.xml.gz`; `.gz0` to `.gz9` select the compression level).
With `FileStorage::WRITE | FileStorage::MEMORY` the data goes to an internal buffer and `fs.releaseAndGetString()` returns it.
Format is chosen by extension (`.xml`, `.yml` or `.yaml`, `.json`) or by the `FORMAT_*` flags.

## 2. Read
```cpp
cv::FileStorage fs("calib.yaml", cv::FileStorage::READ);
CV_Assert(fs.isOpened());
cv::Mat K; fs["camera_matrix"] >> K;
int w = (int)fs["image_width"];
for (auto n : fs["frames"]) names.push_back((std::string)n);
cv::FileNode b = fs["board"]; int cols = (int)b["cols"];
```
Check `fs["x"].empty()` (`FileNode::empty`) before reading a key that may be absent. `FileNode` also has `isSeq()` and `isMap()`.
The 4.0.0 notes say random access to a sequence in a `FileNode` is O(N), so iterate sequences.

## 3. Python
```python
fs = cv2.FileStorage("calib.yaml", cv2.FILE_STORAGE_READ)
K = fs.getNode("camera_matrix").mat()
w = int(fs.getNode("image_width").real())
fs.release()
```

## Gotchas
- OpenCV YAML output starts with a `%YAML:1.0` header and tags matrices `!!opencv-matrix`; other YAML parsers may need custom tag handling.
  Use FileStorage on both ends, or write JSON.
- Top-level data is a mapping; mappings are written between `{` and `}` and sequences between `[` and `]`. YAML and JSON (not XML) also support a compact inline form.
- For custom structs, follow the OpenCV file input and output tutorial (read and write overloads).

## Verify
- [ ] Round-trip test: write, read back, `cv::norm(K, K2) == 0`.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25) and the OpenCV wiki change logs (4.0.0 to 4.14.0 and the 5.0-alpha release notes). modules/core/include/opencv2/core/persistence.hpp. Confirmed: format by extension, .gz handling and compression levels, WRITE|MEMORY with releaseAndGetString, FileNode::empty/isSeq/isMap/real/mat in the API, YAML header and !!opencv-matrix, mapping and sequence syntax, 4.0.0 persistence rewrite. Removed the unconfirmed key-name rule, PyYAML failure claim and silent-empty-Mat claim.
Method: documentation only; no commands were run.
