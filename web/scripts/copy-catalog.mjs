import { cp, mkdir, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const WEB_DIR = dirname(fileURLToPath(import.meta.url)) + "/..";
const REPO_DIR = resolve(WEB_DIR, "..");
const PUBLIC = join(WEB_DIR, "public");

const SOURCES = ["profiles", "schemas", "exports"];

for (const src of SOURCES) {
  const from = join(REPO_DIR, src);
  const to = join(PUBLIC, src);
  if (!existsSync(from)) {
    console.warn(`skipping ${src}: ${from} does not exist`);
    continue;
  }
  await rm(to, { recursive: true, force: true });
  await mkdir(to, { recursive: true });
  await cp(from, to, { recursive: true });
  console.log(`copied ${src}/ → public/${src}/`);
}

// Special-case: docs/design.md is loaded by design.astro at build time via fs read of public/docs/design.md.
const docsFrom = join(REPO_DIR, "docs");
const docsTo = join(PUBLIC, "docs");
if (existsSync(docsFrom)) {
  await rm(docsTo, { recursive: true, force: true });
  await mkdir(docsTo, { recursive: true });
  await cp(docsFrom, docsTo, { recursive: true });
  console.log(`copied docs/ → public/docs/`);
}
