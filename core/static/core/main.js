//bagian halaman home
(function () {
    var reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    document.querySelectorAll("[data-slider-btn]").forEach(function (btn) {
        var track = document.querySelector(btn.dataset.target);
        if (!track) return;

        var group = document.querySelectorAll(
            '[data-slider-btn][data-target="' + btn.dataset.target + '"]'
        );

        function updateButtons() {
            var atStart = track.scrollLeft <= 1;
            var atEnd =
                track.scrollLeft + track.clientWidth >= track.scrollWidth - 1;

            group.forEach(function (button) {
                button.disabled =
                    Number(button.dataset.dir) < 0 ? atStart : atEnd;
            });
        }

        btn.addEventListener("click", function () {
            var card = track.querySelector(".person-card");
            if (!card) return;

            var gap = parseFloat(getComputedStyle(track).gap) || 0;
            var cardWidth = card.getBoundingClientRect().width + gap;

            track.scrollBy({
                left: Number(btn.dataset.dir) * cardWidth,
                behavior: reduceMotion ? "auto" : "smooth"
            });
        });

        track.addEventListener("scroll", updateButtons, { passive: true });
        window.addEventListener("resize", updateButtons);

        updateButtons();
    });
})();

//fungsi play button video
(function () {
    const panel = document.querySelector(".video-panel");
    const video = document.getElementById("videoProfil");
    const playButton = document.getElementById("videoPlayBtn");

    if (!panel || !video || !playButton) {
        return;
    }

    playButton.addEventListener("click", function () {
        video.setAttribute("controls", "controls");

        video.play()
            .then(function () {
                panel.classList.add("is-playing");
            })
            .catch(function (error) {
                video.removeAttribute("controls");
                console.error("Video tidak dapat diputar:", error);
            });
    });

    video.addEventListener("ended", function () {
        panel.classList.remove("is-playing");
        video.removeAttribute("controls");
        video.currentTime = 0;
    });
})();

// Scroll reveal animation
(function () {
    const elements = document.querySelectorAll(
        ".section, .video-section, .stat-card, .news-card, " +
        ".agenda-card, .person-card, .galeri-item, " +
        ".profile-card, .ketua-figure, .sambutan"
    );

    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if (reduceMotion) return;

    elements.forEach(function (element) {
        element.classList.add("reveal");
    });

    const observer = new IntersectionObserver(function (entries, observer) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.12
    });

    elements.forEach(function (element) {
        observer.observe(element);
    });
})();

//agar web tidak bisa di zoom dengan touchpad
document.addEventListener("wheel", function (event) {
if (
    event.ctrlKey &&
    window.matchMedia("(hover: hover) and (pointer: fine)").matches
) {
    event.preventDefault();
}}, { passive: false });

//fungsi dropdown organisasi visual
document.addEventListener("DOMContentLoaded", function () {
    const masthead = document.querySelector(".masthead");
    const slider = document.querySelector(".masthead-slides");
    const slides = document.querySelectorAll(".masthead-slide");

    if (!masthead || !slider || slides.length <= 1) return;

    let currentIndex = 0;
    let startX = 0;
    let startY = 0;
    let isDragging = false;
    let hasMoved = false;
    let autoSlide;

    const interval = 5000;
    const swipeThreshold = 50;

    // Pindahkan slider
    function goToSlide(index, animate = true) {
        currentIndex = (index + slides.length) % slides.length;

        slider.style.transition = animate
            ? "transform 1s cubic-bezier(0.65, 0, 0.35, 1)"
            : "none";

        slider.style.transform =
            `translateX(-${currentIndex * 100}%)`;
    }

    // Timer otomatis
    function startAutoSlide() {
        clearInterval(autoSlide);

        autoSlide = setInterval(() => {
            goToSlide(currentIndex + 1);
        }, interval);
    }

    // Reset timer setelah interaksi
    function resetAutoSlide() {
        startAutoSlide();
    }

    // Mulai drag / swipe
    masthead.addEventListener("pointerdown", function (event) {
        // Jangan mengganggu tombol dan tautan navbar
        if (event.target.closest("a, button, input, select, textarea")) {
            return;
        }

        if (event.pointerType === "mouse" && event.button !== 0) {
            return;
        }

        startX = event.clientX;
        startY = event.clientY;
        isDragging = true;
        hasMoved = false;

        masthead.classList.add("is-dragging");
        slider.style.transition = "none";
    });

    // Gerakan mouse / jari
    masthead.addEventListener("pointermove", function (event) {
        if (!isDragging) return;

        const diffX = event.clientX - startX;
        const diffY = event.clientY - startY;

        // Biarkan scroll vertikal berjalan normal
        if (Math.abs(diffY) > Math.abs(diffX) + 5) {
            isDragging = false;
            masthead.classList.remove("is-dragging");
            slider.style.transition =
                "transform 1s cubic-bezier(0.65, 0, 0.35, 1)";
            return;
        }

        if (Math.abs(diffX) > 5) {
            hasMoved = true;
        }

        // Geser mengikuti posisi jari / mouse
        const offset = (diffX / masthead.offsetWidth) * 100;

        slider.style.transform =
            `translateX(-${currentIndex * 100 - offset}%)`;
    });

    // Selesai drag / swipe
    function endDrag(event) {
        if (!isDragging) return;

        const diffX = event.clientX - startX;

        isDragging = false;
        masthead.classList.remove("is-dragging");

        if (Math.abs(diffX) >= swipeThreshold) {
            if (diffX < 0) {
                // Usap ke kiri: gambar berikutnya
                goToSlide(currentIndex + 1);
            } else {
                // Usap ke kanan: gambar sebelumnya
                goToSlide(currentIndex - 1);
            }
        } else {
            // Kembali ke posisi semula
            goToSlide(currentIndex);
        }

        resetAutoSlide();
    }

    masthead.addEventListener("pointerup", endDrag);

    masthead.addEventListener("pointercancel", function () {
        if (!isDragging) return;

        isDragging = false;
        masthead.classList.remove("is-dragging");
        goToSlide(currentIndex);
        resetAutoSlide();
    });

    // Mulai otomatis
    startAutoSlide();
});