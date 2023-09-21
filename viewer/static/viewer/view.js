// On page render, check session storage and set styles accordingly
var sidebarState = window.sessionStorage.getItem('sidebarState');
if (sidebarState === 'collapsed') {
    document.documentElement.style.setProperty('--sidebar-display', 'none');
    document.documentElement.style.setProperty('--main-col-size', 'col-md-12 col-lg-12');
} else {
    document.documentElement.style.setProperty('--sidebar-display', 'block');
    document.documentElement.style.setProperty('--main-col-size', 'col-md-9 ml-sm-auto col-lg-10');
}
$(function () {
    var slideUrl = document.getElementById('view').getAttribute('data-slide-url');
    var prefixUrl = document.getElementById('view').getAttribute('data-prefix-url');

    var viewer = new OpenSeadragon({
        id: "view",
        tileSources: slideUrl,
        prefixUrl: prefixUrl,
        showNavigator: true,
        showRotationControl: true,
        animationTime: 0.5,
        blendTime: 0.1,
        constrainDuringPan: true,
        maxZoomPixelRatio: 2,
        minZoomImageRatio: 1,
        visibilityRatio: 1,
        zoomPerScroll: 2,
        timeout: 120000,
    });
});
// Check the initial state on page load
document.addEventListener("DOMContentLoaded", function () {
    var menu = document.getElementById('sidebarMenu');
    var mainContent = document.getElementById('mainContent');
    var toggleButton = document.getElementById('menuToggle');

    var sidebarState = sessionStorage.getItem('sidebarState');

    if (sidebarState === 'collapsed') {
        menu.classList.add('collapsed');
        mainContent.classList.remove('with-sidebar');
        mainContent.classList.remove('col-md-9', 'ml-sm-auto', 'col-lg-10');
        mainContent.classList.add('col-md-12', 'col-lg-12');
        toggleButton.innerText = "Show Files";
    } else {
        toggleButton.innerText = "Hide Files";
    }
});

var menu = document.getElementById('sidebarMenu');
var mainContent = document.getElementById('mainContent');
var toggleButton = document.getElementById('menuToggle');

toggleButton.addEventListener('click', function () {
    if (menu.classList.contains('collapsed')) {
        // If menu is currently collapsed, uncollapse it immediately
        menu.classList.remove('collapsed');
        toggleButton.innerText = "Hide Files";
        sessionStorage.setItem('sidebarState', 'expanded');

        // Then update the main content after the transition has completed
        menu.addEventListener('transitionend', function () {
            mainContent.classList.remove('col-md-12', 'col-lg-12');
            mainContent.classList.add('col-md-9', 'ml-sm-auto', 'col-lg-10');
        }, {once: true});

    } else {
        // If menu is currently expanded, collapse it
        menu.classList.add('collapsed');
        toggleButton.innerText = "Show Files";
        sessionStorage.setItem('sidebarState', 'collapsed');

        // Then update the main content after the transition has completed
        menu.addEventListener('transitionend', function () {
            mainContent.classList.remove('col-md-9', 'ml-sm-auto', 'col-lg-10');
            mainContent.classList.add('col-md-12', 'col-lg-12');
        }, {once: true});
    }
});