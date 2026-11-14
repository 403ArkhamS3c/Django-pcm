
document.addEventListener("DOMContentLoaded", () => {
    const arena = document.getElementById("arena");
    const target = document.getElementById("target");

    const scoreElement = document.getElementById("score");
    const timeElement = document.getElementById("time");
    const bestElement = document.getElementById("best");

    const startButton = document.getElementById("start-game");
    const instruction = document.getElementById("game-instruction");
    const previousButton = document.getElementById("previous-page");

    if (
        !arena ||
        !target ||
        !scoreElement ||
        !timeElement ||
        !bestElement ||
        !startButton
    ) {
        return;
    }

    const GAME_DURATION = 20;

    let score = 0;
    let timeLeft = GAME_DURATION;
    let timer = null;
    let isPlaying = false;

    // Membaca skor terbaik.
    function getBestScore() {
        try {
            return Number(localStorage.getItem("pcm404Best")) || 0;
        } catch {
            return 0;
        }
    }

    let bestScore = getBestScore();

    bestElement.textContent = bestScore;

    // Memindahkan target ke posisi acak.
    function moveTarget() {
        const arenaWidth = arena.clientWidth;
        const arenaHeight = arena.clientHeight;

        const targetWidth = target.offsetWidth;
        const targetHeight = target.offsetHeight;

        const padding = 12;

        const maxX = arenaWidth - targetWidth - padding * 2;
        const maxY = arenaHeight - targetHeight - padding * 2;

        const x = padding + Math.random() * Math.max(0, maxX);
        const y = padding + Math.random() * Math.max(0, maxY);

        target.style.left = `${x + targetWidth / 2}px`;
        target.style.top = `${y + targetHeight / 2}px`;
        target.style.transform = "translate(-50%, -50%)";
    }

    // Memulai permainan.
    function startGame() {
        if (isPlaying) return;

        score = 0;
        timeLeft = GAME_DURATION;
        isPlaying = true;

        scoreElement.textContent = score;
        timeElement.textContent = `${timeLeft}s`;

        target.disabled = false;

        startButton.disabled = true;
        startButton.textContent = "Permainan Berlangsung";

        instruction.textContent = "Tangkap angka nol sebanyak mungkin!";

        moveTarget();

        timer = window.setInterval(() => {
            timeLeft--;

            timeElement.textContent = `${timeLeft}s`;

            if (timeLeft <= 0) {
                endGame();
            }
        }, 1000);
    }

    // Menangkap angka nol.
    target.addEventListener("click", () => {
        if (!isPlaying) return;

        score++;

        scoreElement.textContent = score;

        moveTarget();
    });

    // Mengakhiri permainan.
    function endGame() {
        isPlaying = false;

        window.clearInterval(timer);
        timer = null;

        target.disabled = true;

        startButton.disabled = false;
        startButton.textContent = "Main Lagi";

        instruction.textContent = `Waktu habis! Skor Anda: ${score}`;

        if (score > bestScore) {
            bestScore = score;

            bestElement.textContent = bestScore;

            try {
                localStorage.setItem("pcm404Best", bestScore);
            } catch {
                // Permainan tetap berjalan jika penyimpanan tidak tersedia.
            }

            instruction.textContent =
                `Rekor baru! Anda mendapatkan ${score} poin.`;
        }
    }

    // Tombol mulai dan main lagi.
    startButton.addEventListener("click", startGame);

    // Kembali ke halaman sebelumnya.
    previousButton?.addEventListener("click", () => {
        if (window.history.length > 1) {
            window.history.back();
        } else {
            window.location.href = "/";
        }
    });

    // Posisi target awal.
    moveTarget();
});
