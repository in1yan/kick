// script.js
// Simple particle animation for the hero section canvas

const canvas = document.getElementById('hero-canvas');
const ctx = canvas.getContext('2d');
let particles = [];
const particleCount = 100;
const maxVelocity = 0.5;
const maxSize = 3;

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

function initParticles() {
  particles = [];
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * maxVelocity,
      vy: (Math.random() - 0.5) * maxVelocity,
      size: Math.random() * maxSize + 1,
      opacity: Math.random() * 0.5 + 0.3,
    });
  }
}

initParticles();

function update() {
  for (let p of particles) {
    p.x += p.vx;
    p.y += p.vy;
    // wrap around edges
    if (p.x < 0) p.x = canvas.width;
    if (p.x > canvas.width) p.x = 0;
    if (p.y < 0) p.y = canvas.height;
    if (p.y > canvas.height) p.y = 0;
  }
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = 'rgba(255,255,255,0.8)';
  for (let p of particles) {
    ctx.globalAlpha = p.opacity;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
}

function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}

loop();

// --- Horizontal scrolling with vertical wheel ---
// Translate vertical wheel movements (deltaY) into horizontal scrolling of the
// .horizontal-scroll container. The listener is attached to the container so the
// effect only applies when the pointer is over the scrolling area, and we allow
// normal vertical scrolling when horizontal scrolling is no longer possible.
const horizontalContainer = document.querySelector('.horizontal-scroll');
if (horizontalContainer) {
  horizontalContainer.addEventListener(
    'wheel',
    (e) => {
      // Only act when the container actually overflows horizontally
      if (horizontalContainer.scrollWidth <= horizontalContainer.clientWidth) return;
      // We only care about vertical wheel motion
      if (e.deltaY === 0) return;

      // Determine if we can scroll further in the direction of deltaY
      const canScrollRight =
        e.deltaY > 0 &&
        horizontalContainer.scrollLeft + horizontalContainer.clientWidth <
          horizontalContainer.scrollWidth;
      const canScrollLeft = e.deltaY < 0 && horizontalContainer.scrollLeft > 0;

      if (canScrollRight || canScrollLeft) {
        // Prevent the default vertical scroll when we can scroll horizontally
        e.preventDefault();
        // Scroll the container horizontally – preserve the sign of deltaY
        horizontalContainer.scrollLeft += e.deltaY;
      }
      // If we cannot scroll further horizontally, let the page scroll vertically.
    },
    { passive: false }
  );
}
