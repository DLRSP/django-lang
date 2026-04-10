/**
 * Adds class ``display-standalone`` on <html> when the page runs in a standalone
 * display surface (CSS ``display-mode: standalone``) or as an iOS home-screen
 * web app (``navigator.standalone``). Optional hook for future CSS/JS; navbar
 * language placement no longer depends on it (see nav-link-standalone.css).
 */
(function () {
    try {
        var dm = window.matchMedia && window.matchMedia("(display-mode: standalone)");
        var ios = window.navigator.standalone === true;
        if ((dm && dm.matches) || ios) {
            document.documentElement.classList.add("display-standalone");
        }
    } catch (e) {}
})();
