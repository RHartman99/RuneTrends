let mix = require("laravel-mix");
mix
  .js("src/scripts/grandexchange.js", "GrandExchange/static/scripts/")
  .postCss("src/styles/grandexchange.pcss", "GrandExchange/static/styles/", [
    require("postcss-easy-import")(),
    require("precss")(),
    require("tailwindcss")(),
  ]);

mix.browserSync({
  watch: true,
  proxy: "localhost:8000",
  files: "./GrandExchange/dist/styles/*.css",
  watchEvents: ["change", "add"],
  logConnections: true,
});
