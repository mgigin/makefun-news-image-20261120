// Hand-in entrypoint for the News Image 2026-11-20 bounty.
// The graded artefact is the broadsheet image rendered by build_image.py and
// committed beside this file as entry.png. The house runs this program in a
// sandbox and collects whatever lands in MAKEFUN_OUTPUT_DIR, so all this
// program has to do is deliver that image, byte for byte, to the output
// directory. It uses Node built-ins only, reads nothing from the network,
// and produces the same result on every run.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(here, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR;

if (!outputDir) {
  console.error("MAKEFUN_OUTPUT_DIR is not set; nowhere to deliver entry.png.");
  process.exit(1);
}

if (!existsSync(sourceImage)) {
  console.error(`entry.png is missing next to main.ts (looked in ${here}).`);
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(sourceImage, join(outputDir, "entry.png"));
console.log(`entry.png delivered to ${outputDir}`);
