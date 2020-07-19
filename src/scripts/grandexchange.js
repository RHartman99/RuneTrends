import { Application } from "stimulus";
import { definitionsFromContext } from "stimulus/webpack-helpers";
import { library, dom } from "@fortawesome/fontawesome-svg-core";
import { faQuestionCircle } from "@fortawesome/free-regular-svg-icons";
import LazyLoad from "vanilla-lazyload";
const application = Application.start();
const context = require.context("./controllers", true, /\.js$/);
application.load(definitionsFromContext(context));

library.add(faQuestionCircle);

const CLOUDINARY_URL = "https://res.cloudinary.com/rhartman99/image/fetch/";

function isLocal() {
  return location.hostname === "localhost" || location.hostname === "127.0.0.1";
}

function prependCloudinary(el) {
  if (!isLocal()) el.dataset.src = CLOUDINARY_URL + el.dataset.src;
}

function unknownImage(el) {
  const wrapper = el.parentElement;
  const placeholder = document.createElement("div");
  placeholder.className = "placeholder";
  placeholder.innerHTML = `<i class="far fa-question-circle"></i>`;
  wrapper.insertBefore(placeholder, wrapper.childNodes[0]);
  wrapper.removeChild(el);
}

window.addEventListener("DOMContentLoaded", () => {
  dom.watch();
  new LazyLoad({
    elements_selector: ".lazy",
    callback_enter: prependCloudinary,
    callback_error: unknownImage,
  });
});
