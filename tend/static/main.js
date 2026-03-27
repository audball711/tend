// ── Tend Atmosphere Engine ──
// Reads time of day + weather mood and builds the living environment

(function () {
  // Only run atmosphere on homepage
  if (!document.body.classList.contains("home-page")) {
    return;
  }

  // ── Time of day ──
  function getTimeOfDay() {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 8) return "dawn";
    if (hour >= 8 && hour < 18) return "day";
    if (hour >= 18 && hour < 21) return "dusk";
    return "night";
  }

  // ── Read weather mood from body class ──
  function getWeatherMood() {
    const body = document.body;
    if (body.classList.contains("rainy")) return "rainy";
    if (body.classList.contains("sunny")) return "sunny";
    if (body.classList.contains("cloudy")) return "cloudy";
    return "neutral";
  }

  // ── Build the weather layer ──
  function buildAtmosphere() {
    const timeOfDay = getTimeOfDay();
    const mood = getWeatherMood();

    // add time-of-day class to body
    document.body.classList.add(timeOfDay);

    // reuse existing weather-layer if present in layout.html
    let layer = document.querySelector(".weather-layer");

    if (!layer) {
      layer = document.createElement("div");
      layer.className = "weather-layer";
      document.body.insertBefore(layer, document.body.firstChild);
    }

    // clear anything old before rebuilding
    layer.innerHTML = "";

    if (mood === "rainy") {
      buildRain(layer);
      buildClouds(layer);

      if (timeOfDay === "night") {
        buildStars(layer);
      }
    } else if (mood === "sunny") {
      if (timeOfDay === "day" || timeOfDay === "dawn" || timeOfDay === "dusk") {
        buildSunRays(layer);
      }

      if (timeOfDay === "night") {
        buildStars(layer);
      }
    } else if (mood === "cloudy") {
      buildClouds(layer);

      if (timeOfDay === "night") {
        buildStars(layer);
      }
    } else {
      // neutral
      if (timeOfDay === "night") {
        buildStars(layer);
        buildFireflies(layer);
      } else if (timeOfDay === "dusk" || timeOfDay === "dawn") {
        buildFireflies(layer);
      }
    }
  }

  // ── Rain ──
  function buildRain(layer) {
    for (let i = 0; i < 60; i++) {
      const drop = document.createElement("div");
      drop.className = "drop";
      drop.style.left = `${Math.random() * 100}%`;
      drop.style.height = `${12 + Math.random() * 20}px`;
      drop.style.animationDuration = `${0.5 + Math.random() * 0.8}s`;
      drop.style.animationDelay = `${Math.random() * 2}s`;
      drop.style.opacity = `${0.3 + Math.random() * 0.5}`;
      layer.appendChild(drop);
    }
  }

  // ── Sun rays ──
  function buildSunRays(layer) {
    const angles = [-50, -30, -10, 10, 30, 50, 70];

    angles.forEach((angle, i) => {
      const ray = document.createElement("div");
      ray.className = "ray";
      ray.style.setProperty("--angle", `${angle}deg`);
      ray.style.transform = `rotate(${angle}deg)`;
      ray.style.height = `${50 + Math.random() * 30}vh`;
      ray.style.animationDuration = `${5 + i * 1.2}s`;
      ray.style.animationDelay = `${i * 0.4}s`;
      layer.appendChild(ray);
    });
  }

  // ── Stars ──
  function buildStars(layer) {
    for (let i = 0; i < 80; i++) {
      const star = document.createElement("div");
      star.className = "star";
      const size = 1 + Math.random() * 2;

      star.style.width = `${size}px`;
      star.style.height = `${size}px`;
      star.style.left = `${Math.random() * 100}%`;
      star.style.top = `${Math.random() * 60}%`;
      star.style.animationDuration = `${2 + Math.random() * 3}s`;
      star.style.animationDelay = `${Math.random() * 3}s`;

      layer.appendChild(star);
    }
  }

  // ── Fireflies ──
  function buildFireflies(layer) {
    for (let i = 0; i < 12; i++) {
      const ff = document.createElement("div");
      ff.className = "firefly";
      ff.style.left = `${10 + Math.random() * 80}%`;
      ff.style.top = `${40 + Math.random() * 50}%`;
      ff.style.animationDuration = `${3 + Math.random() * 4}s`;
      ff.style.animationDelay = `${Math.random() * 4}s`;
      layer.appendChild(ff);
    }
  }

  // ── Clouds ──
  function buildClouds(layer) {
    for (let i = 0; i < 5; i++) {
      const cloud = document.createElement("div");
      cloud.className = "cloud";
      const size = 200 + Math.random() * 300;

      cloud.style.width = `${size}px`;
      cloud.style.height = `${size * 0.4}px`;
      cloud.style.top = `${Math.random() * 40}%`;
      cloud.style.animationDuration = `${40 + Math.random() * 40}s`;
      cloud.style.animationDelay = `${Math.random() * 20}s`;

      layer.appendChild(cloud);
    }
  }

  // ── Run ──
  buildAtmosphere();
})();