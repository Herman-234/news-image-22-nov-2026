// news-image-20261122 entry (Node 22, standard library only).
// The image beside this file is the entry: copy it to the output dir.
// The grader runs this twice with no network; both runs must write the
// same bytes, so this does a plain byte copy and nothing else.
//
// Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, statSync } from "node:fs";
import { join } from "node:path";

const here = new URL("./entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL(here).pathname;

if (!existsSync(src)) {
  throw new Error("entry.png is missing next to main.ts");
}
if (statSync(src).size > 1048576) {
  throw new Error("entry.png is over the 1 MiB gate limit");
}
copyFileSync(src, join(outDir, "entry.png"));
