// precious_cornerstone/UNIVERSITY/static/UNIVERSITY/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    const body = document.body;

    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('is-open');
            menuToggle.classList.toggle('is-open'); // Optional: for animating hamburger lines
            body.classList.toggle('no-scroll'); // Optional: prevent body scrolling when sidebar is open
        });

        // Optional: Close sidebar when clicking outside (on overlay)
        // You might need an overlay div for this or check clicks on body
        body.addEventListener('click', function(event) {
            if (mainNav.classList.contains('is-open') &&
                !mainNav.contains(event.target) &&
                !menuToggle.contains(event.target)) {
                mainNav.classList.remove('is-open');
                menuToggle.classList.remove('is-open');
                body.classList.remove('no-scroll');
            }
        });

        // Optional: Close sidebar on ESC key press
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && mainNav.classList.contains('is-open')) {
                mainNav.classList.remove('is-open');
                menuToggle.classList.remove('is-open');
                body.classList.remove('no-scroll');
            }
        });
    }
});