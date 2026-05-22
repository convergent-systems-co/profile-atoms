import { defineConfig } from "astro/config";
import react from "@astrojs/react";

export default defineConfig({
  site: "https://profile-atoms.com",
  integrations: [react()],
  output: "static",
});
