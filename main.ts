// Entry for make.fun bounty news-image-20261120: "Sum up 20 November's world news in one image".
//
// The artwork lives beside this file as entry.png (1024x1024, generated offline from the
// day's headlines). This program validates that file against the bounty gate and copies
// its bytes, unchanged, to the grader's output directory. It uses only the Node standard
// library, touches no network, and is deterministic: every run writes identical bytes.
//
// Local test (outside the grader container):
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1024 * 1024; // 1 MiB gate
const MAX_DIMENSION = 1024; // pixels, either axis
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

const source = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(source);

if (bytes.length === 0 || bytes.length > MAX_BYTES) {
  throw new Error(`entry.png must be 1..${MAX_BYTES} bytes, got ${bytes.length}`);
}
for (let i = 0; i < PNG_SIGNATURE.length; i += 1) {
  if (bytes[i] !== PNG_SIGNATURE[i]) {
    throw new Error('entry.png does not start with the PNG signature');
  }
}
// PNG IHDR: width and height are big-endian uint32 at offsets 16 and 20.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width === 0 || height === 0 || width > MAX_DIMENSION || height > MAX_DIMENSION) {
  throw new Error(`entry.png must be within ${MAX_DIMENSION}x${MAX_DIMENSION}, got ${width}x${height}`);
}
if (statSync(source).size !== bytes.length) {
  throw new Error('entry.png changed while being read');
}

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outputDir, { recursive: true });
copyFileSync(source, join(outputDir, 'entry.png'));
