---
id: computing-software.computer-graphics-engineering.directx.d3d12-video-decode-and-encode
name: d3d12-video-decode-and-encode
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-advanced, d3d12-video, hardware-video-decode, nv12-d3d12]
level: sme
status: docs-checked
description: "Decode/encode video with D3D12 Video (ID3D12VideoDevice): capability checks, decoder heaps, NV12 output textures, sync with graphics, and when to use Media Foundation."
sources: ["https://github.com/microsoft/DirectX-Headers/blob/main/include/directx/d3d12video.h", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/D3D12VideoEncoding.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 video decode and encode

D3D12 Video exposes the GPU's fixed-function codecs (decode profiles in `d3d12video.h` include
H.264, HEVC, VP8, VP9 and AV1; encoder codecs include H.264, HEVC and AV1) as video queues and
command lists; support is queried per device. You supply **compressed bitstream +
parsed picture parameters**; the API does not parse containers or bitstreams for you.

## When to use what
- **A media framework** (for example Media Foundation) that does demux and parsing for you. Use
  one unless you need full control.
- **Raw D3D12 Video**: game engines with custom streaming, low-latency cloud streaming encoders,
  where you already have a parser (e.g. from vendor SDKs or your own).

## Decode outline
```cpp
ComPtr<ID3D12VideoDevice> vdev; device.As(&vdev);
D3D12_FEATURE_DATA_VIDEO_DECODE_SUPPORT sup = {};
sup.Configuration = { D3D12_VIDEO_DECODE_PROFILE_HEVC_MAIN, D3D12_BITSTREAM_ENCRYPTION_TYPE_NONE,
                      D3D12_VIDEO_FRAME_CODED_INTERLACE_TYPE_NONE };
sup.Width = 3840; sup.Height = 2160; sup.DecodeFormat = DXGI_FORMAT_NV12; sup.FrameRate = {60, 1};
vdev->CheckFeatureSupport(D3D12_FEATURE_VIDEO_DECODE_SUPPORT, &sup, sizeof(sup));
// sup.SupportFlags & D3D12_VIDEO_DECODE_SUPPORT_FLAG_SUPPORTED
// create: ID3D12VideoDecoder (per profile), ID3D12VideoDecoderHeap (per resolution/DPB size)
// queue: D3D12_COMMAND_LIST_TYPE_VIDEO_DECODE; list: ID3D12VideoDecodeCommandList
// per frame: DecodeFrame(decoder, &outputArgs{NV12 texture}, &inputArgs{bitstream buffer, picture params, refs})
```
Reference frames (DPB) are textures (or a texture array if `ReferenceOnly`/array-of-textures
requirements say so); output may need a separate non-reference texture plus conversion.

## Using frames in graphics
- Sync the video queue and direct queue with a fence (`Signal` on video queue, `Wait` on direct).
- Sample NV12 with two SRVs (one per plane, with plane-specific formats), then convert the YUV
  colour space with the correct range in the shader.
- Resource states for video: `VIDEO_DECODE_WRITE`/`READ`; transition to `PIXEL_SHADER_RESOURCE` for sampling.

## Encode
`ID3D12VideoEncoder` + `ID3D12VideoEncoderHeap`, `D3D12_FEATURE_VIDEO_ENCODER_*` caps (rate
control modes CBR/VBR/QVBR, GOP, slices). Output is a raw bitstream + metadata you resolve
(`ResolveEncoderOutputMetadata`) and then write headers (SPS/PPS/VPS) yourself or via vendor helpers.

## Gotchas
- `D3D12_VIDEO_DECODE_CONFIGURATION_FLAG_HEIGHT_ALIGNMENT_MULTIPLE_32_REQUIRED` in the support
  result means the textures need height aligned to a multiple of 32.
- Protected (DRM) content needs the protected resource session path; not covered here.

## Verify
- [ ] Decoded frames match a reference software decode of the same stream.

## Checked

2026-10-26. Checked against the d3d12video.h and d3d12.h headers in microsoft/DirectX-Headers and the DirectX-Specs video encoding
documents (commits to 2026-10). Confirmed: D3D12_VIDEO_DECODE_PROFILE_* names (HEVC_MAIN, VP9, AV1_PROFILE0),
D3D12_FEATURE_VIDEO_DECODE_SUPPORT and its Configuration field, D3D12_VIDEO_DECODE_SUPPORT_FLAG_SUPPORTED, the
height-alignment configuration flag, command list types VIDEO_DECODE/ENCODE, VIDEO_DECODE_WRITE/READ resource states,
ResolveEncoderOutputMetadata, rate control modes CBR/VBR/QVBR. Removed the FFmpeg d3d12va flag, PSNR threshold,
decoder-heap-recreation and plane-format specifics that no fetched document covers.
Method: documentation only; no commands were run.
