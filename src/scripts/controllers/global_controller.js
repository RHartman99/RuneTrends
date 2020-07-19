import { Controller } from "stimulus";
import Cookies from "js-cookie";

const COOKIE_NAME = "runetrends_darkmodeennabled";

export default class extends Controller {
  connect() {
    if (!Cookies.get(COOKIE_NAME)) Cookies.set(COOKIE_NAME, false);
    else if (Cookies.get(COOKIE_NAME) === "true")
      this.element.classList.add("dark");
  }

  toggleDark(e) {}
}
