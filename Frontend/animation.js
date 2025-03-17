console.log("animations.js Loaded Successfully!");

document.addEventListener("DOMContentLoaded", function() {
    console.log("Checking jQuery & Owl Carousel...");

    function initializeCarousel() {
        if (typeof jQuery === "undefined" || typeof $.fn.owlCarousel === "undefined") {
            console.log("Waiting for jQuery/OwlCarousel...");
            setTimeout(initializeCarousel, 500);
        } else {
            console.log("jQuery and Owl Carousel detected! Initializing...");

            $(".testimonial_slider").owlCarousel({
                loop: true, // Ensures seamless looping
                margin: 20,
                nav: false, // Removes manual navigation
                dots: false, // Removes dot indicators
                autoplay: true, // Enables automatic movement
                autoplayTimeout: 2200, // Adjust time interval
                autoplayHoverPause: false, // Ensures continuous movement
                smartSpeed: 1000, // Smooth transition speed
                responsive: {
                    0: { items: 1 },
                    768: { items: 2 }
                }
            });

            console.log("Owl Carousel Initialized Successfully!");
        }
    }

    initializeCarousel();
});
