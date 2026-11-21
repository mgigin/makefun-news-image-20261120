// Entrypoint for the news-image entry.
//
// The finished artwork (entry.png) is committed next to this file. The
// house runs this program in a sandbox and reads the image from the
// output directory it names, so all we do here is copy the PNG there:
// deterministically, with Node built-ins only, and no network access.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  console.error("MAKEFUN_OUTPUT_DIR is not set; nowhere to write entry.png.");
  process.exit(1);
}

if (!existsSync(source)) {
  console.error(`entry.png not found next to main.ts (looked in ${here}).`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
console.log(`entry.png copied to ${outDir}`);
