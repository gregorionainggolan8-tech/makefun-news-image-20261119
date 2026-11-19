// Entry point for the news-image-20261119 competition.
//
// The front page (entry.png) is drawn from scratch by make_image.py and
// shipped in this repository. This program only copies it into the output
// directory the grader provides, so both runs write identical bytes.
// Standard library only, no network, no randomness.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));

const outputDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outputDir) {
  throw new Error("MAKEFUN_OUTPUT_DIR is not set");
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(join(repoDir, "entry.png"), join(outputDir, "entry.png"));
