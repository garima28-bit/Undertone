/* ============================================================
   UNDERTONE — cursor.js
   Tracks pointer position and writes it to CSS custom properties
   (--mx, --my) that the .field::after spotlight mask reads.
   Uses requestAnimationFrame so it never fights the browser's
   paint schedule. No frameworks, no dependencies.
   ============================================================ */
(function () {
  var field = document.querySelector('.field');
  if (!field) return;

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isTouch = window.matchMedia('(hover: none)').matches;
  if (reduceMotion || isTouch) return;

  var targetX = window.innerWidth / 2;
  var targetY = window.innerHeight * 0.4;
  var currentX = targetX;
  var currentY = targetY;
  var ticking = false;

  window.addEventListener('pointermove', function (e) {
    targetX = e.clientX;
    targetY = e.clientY;
    if (!ticking) {
      requestAnimationFrame(update);
      ticking = true;
    }
  }, { passive: true });

  function update() {
    // gentle easing so the reveal trails the cursor slightly,
    // rather than snapping — feels like light catching something
    currentX += (targetX - currentX) * 0.18;
    currentY += (targetY - currentY) * 0.18;

    field.style.setProperty('--mx', currentX + 'px');
    field.style.setProperty('--my', currentY + 'px');

    if (Math.abs(targetX - currentX) > 0.5 || Math.abs(targetY - currentY) > 0.5) {
      requestAnimationFrame(update);
    } else {
      ticking = false;
    }
  }
})();
