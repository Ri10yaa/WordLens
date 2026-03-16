import { build } from "esbuild";
import { cp, mkdir } from "node:fs/promises";
import { resolve } from "node:path";

const root = process.cwd();
const outdir = resolve(root, "dist");

const define = {
  "process.env.BACKEND_URL": JSON.stringify(
    process.env.BACKEND_URL ?? "http://localhost:8000"
  ),
};

await build({
  entryPoints: {
    background: "src/background/index.ts",
    content: "src/content/index.ts",
    "floating-dialog": "src/ui/floatingDialog.ts"
  },
  bundle: true,
  outdir,
  minify: false,
  sourcemap: true,
  format: "esm",
  target: ["chrome110"],
  define,
});

await mkdir(outdir, { recursive: true });
await cp("public", outdir, { recursive: true });
console.log("✓ Extension build complete");
