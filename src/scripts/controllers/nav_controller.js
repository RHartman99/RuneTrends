import { Controller } from "stimulus";
import Cookies from "js-cookie";

const COOKIE_NAME = "runetrends_navbarcollapsed";

export default class extends Controller {
  connect() {
    if (!Cookies.get(COOKIE_NAME)) {
      Cookies.set(COOKIE_NAME, false);
    } else if (Cookies.get(COOKIE_NAME) === "true") {
      this.element.classList.add("collapsed");
      document.querySelector("main").classList.add("large");
    }
  }

  toggleCollapse(e) {
    const button = e.srcElement.closest(".navbar__collapse");
    this.element.classList.toggle("collapsed");
    document.querySelector("main").classList.toggle("large");
    console.log(this.element.classList.contains("collapsed"));
    Cookies.set(COOKIE_NAME, this.element.classList.contains("collapsed"));
  }
}
