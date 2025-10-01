    // File input
    const fileInput = document.getElementById("file");
    const fileName = document.getElementById("fileName");
    fileInput.addEventListener("change", () => {
      fileName.textContent = fileInput.files.length ? fileInput.files[0].name : "No file chosen";
    });

    // Fake upload status
    const form = document.getElementById("uploadForm");
    const status = document.getElementById("status");
    form.addEventListener("submit", (e) => {
      status.style.color = "var(--unsw-yellow)";
      status.textContent = "⏳ Analyzing your resume...";
      setTimeout(() => {
        status.style.color = "lightgreen";
        status.textContent = "✅ Done! Your resume has been analyzed.";
      }, 2000);
    });

    // Smooth parallax tilt on scroll
    const gridPlane = document.getElementById("gridPlane");
    window.addEventListener("scroll", () => {
      const scrolled = window.scrollY * 0.1;
      gridPlane.style.transform =
        `translate(-50%, -50%) perspective(600px) rotateX(70deg) translateY(${scrolled}px)`;
    });

    // --- Typing effect ---
    function typeWriter(elementId, text, speed = 50, delay = 0) {
      let i = 0;
      setTimeout(() => {
        function type() {
          if (i < text.length) {
            document.getElementById(elementId).innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
          }
        }
        type();
      }, delay);
    }

    // Run typing animations
    typeWriter("typingHero", "Analyze your resume, discover your strengths, and get personalized UNSW elective suggestions.", 40, 500);
    typeWriter("typingUpload", "Our AI securely processes your file in seconds.", 40, 2500);