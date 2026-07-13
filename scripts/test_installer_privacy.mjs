#!/usr/bin/env node
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const temp = fs.mkdtempSync(path.join(os.tmpdir(), "heituzmpw-installer-privacy-"));

function run(command, args, options = {}) {
  const result = spawnSync(command, args, { cwd: root, encoding: "utf8", ...options });
  assert.equal(result.status, 0, `${command} failed: ${result.stderr || result.stdout}`);
  return result.stdout;
}

function hasExcludedPath(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const name = entry.name;
    if ([".omx", ".gjc", "docs-internal", "__pycache__"].includes(name) || name.endsWith(".pyc")) return true;
    if (entry.isDirectory() && hasExcludedPath(path.join(dir, name))) return true;
  }
  return false;
}

try {
  const installDest = path.join(temp, "installed");
  run(process.execPath, ["scripts/install.mjs", "--dest", installDest, "--force", "--quiet"]);
  assert.equal(hasExcludedPath(installDest), false, "installer copied excluded local state");

  const packed = JSON.parse(run("npm", ["pack", "--dry-run", "--json"]));
  const names = packed[0].files.map((file) => file.path);
  assert.equal(names.some((name) => /(^|\/)(?:\.omx|\.gjc|docs-internal|__pycache__)(?:\/|$)|\.pyc$/u.test(name)), false,
    "npm package includes excluded local state");
  console.log("installer/package privacy allowlist: OK");
} finally {
  fs.rmSync(temp, { recursive: true, force: true });
}
