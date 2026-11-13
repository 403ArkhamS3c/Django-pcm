(function () {
    var loading = document.getElementById("page-loading");

    if (!loading) return;

    function showLoading() {
        loading.classList.add("active");
        loading.setAttribute("aria-hidden", "false");
    }

    function hideLoading() {
        loading.classList.remove("active");
        loading.setAttribute("aria-hidden", "true");
    }

    // Navigasi antarhalaman
    document.addEventListener("click", function (event) {
        var link = event.target.closest("a");

        if (!link) return;

        // Abaikan klik yang membuka tab baru atau bukan klik kiri
        if (
            event.button !== 0 ||
            event.ctrlKey ||
            event.shiftKey ||
            event.altKey ||
            event.metaKey
        ) return;

        // Abaikan link khusus
        if (
            link.target === "_blank" ||
            link.hasAttribute("download") ||
            link.hasAttribute("data-bs-toggle") ||
            link.getAttribute("href") === "#" ||
            link.getAttribute("href")?.startsWith("#")
        ) return;

        var url = new URL(link.href, window.location.href);

        // Hanya navigasi dalam website
        if (url.origin !== window.location.origin) return;

        // Abaikan jika hanya berpindah posisi halaman
        if (
            url.pathname === window.location.pathname &&
            url.search === window.location.search &&
            url.hash
        ) return;

        showLoading();
    });

    // Pengiriman form
    document.addEventListener("submit", function (event) {
        if (event.defaultPrevented) return;

        var form = event.target;

        if (
            form.target === "_blank" ||
            form.hasAttribute("data-no-loading")
        ) return;

        showLoading();
    });

    // Sembunyikan loading setelah halaman selesai dimuat
    window.addEventListener("pageshow", hideLoading);

    // Sembunyikan ketika halaman tidak jadi ditinggalkan
    window.addEventListener("pagehide", hideLoading);

})();
