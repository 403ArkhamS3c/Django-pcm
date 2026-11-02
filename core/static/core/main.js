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

