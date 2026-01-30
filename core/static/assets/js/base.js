document.addEventListener("DOMContentLoaded", function () {

    // Initialize GLightbox if the library is available
    if (window.GLightbox) {
        GLightbox({
            touchNavigation: true,
            loop: true,
            zoomable: true,
        });
    }

    // Apply staggered fade-in animation for images in rich galleries
    const galleryImages = document.querySelectorAll(".rich-gallery img");
    galleryImages.forEach((img, index) => {
        const delay = index * 120;

        if (img.complete) {
            setTimeout(() => img.classList.add("loaded"), delay);
        } else {
            img.addEventListener("load", () => {
                setTimeout(() => img.classList.add("loaded"), delay);
            });
        }
    });

    // Toggle contact icons on mobile devices only
    const contactToggles = document.querySelectorAll(".toggle-contact");
    contactToggles.forEach(link => {
        link.addEventListener("click", function (e) {
            if (window.innerWidth > 768) return;

            e.preventDefault();
            e.stopPropagation();

            // Close other open contact toggles
            contactToggles.forEach(l => {
                if (l !== link) l.classList.remove("active");
            });

            link.classList.toggle("active");
        });
    });

    // Close contact toggles when clicking outside
    document.addEventListener("click", function () {
        contactToggles.forEach(l => l.classList.remove("active"));
    });

    // Handle dropdown navigation for touch devices
    const dropdownItems = document.querySelectorAll(".has-dropdown");
    const isTouchDevice = window.matchMedia("(hover: none)").matches;

    let justToggled = false;

    dropdownItems.forEach(item => {
        const link = item.querySelector(":scope > a");
        if (!link) return;

        link.addEventListener("click", function (e) {
            if (!isTouchDevice) return;

            e.preventDefault();
            e.stopPropagation();

            justToggled = true;
            setTimeout(() => { justToggled = false; }, 0);

            const isOpen = item.classList.contains("open");

            // Close all dropdowns before opening a new one
            dropdownItems.forEach(other => other.classList.remove("open"));

            if (!isOpen) {
                item.classList.add("open");
            }
        });
    });

    // Close dropdowns when clicking outside the navigation
    document.addEventListener("click", function (e) {
        if (justToggled) return;

        if (!e.target.closest(".main-nav")) {
            dropdownItems.forEach(item => item.classList.remove("open"));
        }
    });

    // Mobile navigation burger toggle
    const nav = document.querySelector(".main-nav");
    const toggle = document.querySelector(".mobile-nav-toggle");

    if (nav && toggle) {
        toggle.addEventListener("click", function (e) {
            e.stopPropagation();

            nav.classList.toggle("mobile-open");
            toggle.classList.toggle("is-open");

            const expanded = toggle.classList.contains("is-open");
            toggle.setAttribute("aria-expanded", expanded);
        });

        // Close mobile navigation when clicking outside
        document.addEventListener("click", function (e) {
            if (!e.target.closest(".main-nav")) {
                nav.classList.remove("mobile-open");
                toggle.classList.remove("is-open");
                toggle.setAttribute("aria-expanded", "false");
            }
        });
    }

});
