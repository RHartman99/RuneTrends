let mix = require("laravel-mix");
const glob = require("glob");
const ImageminPlugin = require("imagemin-webpack-plugin").default;
const imageminMozjpeg = require("imagemin-mozjpeg");

const files = [
  "GrandExchange/static/*.*",
  "GrandExchange/static/images/*.*",
  "GrandExchange/static/styles/*.*",
  "GrandExchange/static/scripts/*.*",
  "GrandExchange/templates/*.*",
  "GrandExchange/templates/global/*.*",
  "GrandExchange/templates/partials/*.*",
];

mix
  .options({ processCssUrls: false })
  .js("src/scripts/grandexchange.js", "GrandExchange/static/scripts/")
  .postCss("src/styles/app.pcss", "GrandExchange/static/", [
    require("postcss-import")(),
    require("precss")(),
    require("tailwindcss")(),
  ])
  .webpackConfig({
    plugins: [
      new ImageminPlugin({
        externalImages: {
          context: ".",
          sources: glob.sync("./src/images/**/*.{jpg,png}"),
          destination: "GrandExchange/static/images/",
          fileName: "[name].[ext]",
        },
        test: /\.(jpe?g|png|gif|svg)$/i,
        cacheFolder: "./.cache",
        plugins: [
          imageminMozjpeg({
            quality: 80,
          }),
        ],
      }),
    ],
  })
  .browserSync({
    ui: false,
    injectChanges: true,
    files: files,
    proxy: "localhost:8000",
    watch: true,
    logChanges: false,
  });
