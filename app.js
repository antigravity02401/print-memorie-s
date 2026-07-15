/* ============================================================
   Print Memorie's — app.js
   All interactivity: navbar, animations, counter, FAQ, etc.
============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ─── Navbar Scroll Behavior ───────────────────── */
  const navbar = document.getElementById('navbar');
  const navLinks = document.querySelectorAll('.nav-links a');

  const onScroll = () => {
    if (window.scrollY > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
    highlightNavLink();
  };

  window.addEventListener('scroll', onScroll, { passive: true });

  /* ─── Active nav link on scroll ───────────────── */
  const sections = document.querySelectorAll('section[id]');

  function highlightNavLink() {
    let current = '';
    sections.forEach(sec => {
      const top = sec.offsetTop - 100;
      if (window.scrollY >= top) {
        current = sec.getAttribute('id');
      }
    });
    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  }

  /* ─── Smooth scroll for all anchor links ───────── */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const href = anchor.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        closeMobileNav();
        const offset = 80;
        const targetY = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: targetY, behavior: 'smooth' });
      }
    });
  });

  /* ─── Mobile Nav ───────────────────────────────── */
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const mobileNav    = document.getElementById('mobileNav');
  const navOverlay   = document.getElementById('navOverlay');

  function openMobileNav() {
    hamburgerBtn.classList.add('active');
    mobileNav.classList.add('open');
    navOverlay.style.display = 'block';
    document.body.style.overflow = 'hidden';
  }

  function closeMobileNav() {
    hamburgerBtn.classList.remove('active');
    mobileNav.classList.remove('open');
    navOverlay.style.display = 'none';
    document.body.style.overflow = '';
  }

  hamburgerBtn.addEventListener('click', () => {
    if (mobileNav.classList.contains('open')) {
      closeMobileNav();
    } else {
      openMobileNav();
    }
  });

  navOverlay.addEventListener('click', closeMobileNav);

  document.querySelectorAll('.mobile-nav-link').forEach(link => {
    link.addEventListener('click', closeMobileNav);
  });

  /* ─── Scroll-triggered Animations ─────────────── */
  const animatedEls = document.querySelectorAll('.fade-up, .fade-left, .fade-right');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  animatedEls.forEach(el => observer.observe(el));

  /* ─── Counter Animation ────────────────────────── */
  const statEls = document.querySelectorAll('[data-target]');
  let counterStarted = false;

  function animateCounter(el) {
    const target = parseInt(el.dataset.target);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;

    const update = () => {
      current += step;
      if (current >= target) {
        el.textContent = target + '+';
        return;
      }
      el.textContent = Math.floor(current);
      requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
  }

  const statsSection = document.getElementById('stats');
  const statsObserver = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && !counterStarted) {
      counterStarted = true;
      statEls.forEach(el => animateCounter(el));
    }
  }, { threshold: 0.5 });

  if (statsSection) statsObserver.observe(statsSection);

  /* ─── FAQ Accordion ────────────────────────────── */
  document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', () => {
      const item = question.parentElement;
      const isOpen = item.classList.contains('open');

      // Close all
      document.querySelectorAll('.faq-item').forEach(fi => fi.classList.remove('open'));

      // Open clicked if was closed
      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });

  /* ─── Hero Particles ───────────────────────────── */
  const particlesContainer = document.getElementById('heroParticles');
  if (particlesContainer) {
    const numParticles = 20;
    for (let i = 0; i < numParticles; i++) {
      const p = document.createElement('div');
      p.classList.add('particle');

      // Random size
      const size = Math.random() * 4 + 2;
      p.style.width  = `${size}px`;
      p.style.height = `${size}px`;

      // Random position
      p.style.left = `${Math.random() * 100}%`;
      p.style.bottom = `${Math.random() * 30}%`;

      // Random duration & delay
      const duration = Math.random() * 8 + 5;
      const delay    = Math.random() * 8;
      p.style.animationDuration = `${duration}s`;
      p.style.animationDelay   = `${delay}s`;

      particlesContainer.appendChild(p);
    }
  }

  /* ─── Portfolio Card Hover (iframe protect) ──── */
  document.querySelectorAll('.portfolio-card').forEach(card => {
    const overlay = card.querySelector('.portfolio-preview-overlay');
    card.addEventListener('mouseenter', () => {
      if (overlay) overlay.style.pointerEvents = 'auto';
    });
    card.addEventListener('mouseleave', () => {
      if (overlay) overlay.style.pointerEvents = 'none';
    });
  });

  /* ─── Floating WA button pulse on load ──────── */
  const floatWA = document.getElementById('float-wa-btn');
  if (floatWA) {
    setTimeout(() => {
      floatWA.style.transform = 'scale(1.2)';
      setTimeout(() => {
        floatWA.style.transform = '';
      }, 300);
    }, 3000);
  }

  /* ─── Page load: trigger first visible items ── */
  setTimeout(() => {
    document.querySelectorAll('.fade-up, .fade-left, .fade-right').forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.9) {
        el.classList.add('visible');
      }
    });
  }, 100);

  /* ─── Background Music Player (Web Audio API) ── */
  const musicBtn   = document.getElementById('musicBtn');
  const musicIcon  = document.getElementById('musicIcon');
  const musicLabel = document.getElementById('musicLabel');

  if (musicBtn) {

    // ── Romantic wedding chord progression (MIDI notes) ─────────
    // C  Am  F  G  →  romantic Indonesian wedding feel
    const progression = [
      [48, 52, 55, 60, 64],   // C  major  : C3 E3 G3 C4 E4
      [45, 48, 52, 57, 60],   // A  minor  : A2 C3 E3 A3 C4
      [41, 45, 48, 53, 57],   // F  major  : F2 A2 C3 F3 A3
      [43, 47, 50, 55, 59],   // G  major  : G2 B2 D3 G3 B3
    ];

    const BPM        = 60;    // slow, romantic
    const SPB        = 60 / BPM;   // seconds per beat
    const NOTE_DUR   = SPB * 1.8;  // each note duration
    const NOTE_GAP   = SPB * 0.55; // gap between arpeggio notes
    const VOL_TARGET = 0.22;

    let audioCtx    = null;
    let masterGain  = null;
    let delayNode   = null;
    let fbGain      = null;
    let isPlaying   = false;
    let schedTimer  = null;
    let nextTime    = 0;
    let progIdx     = 0;
    let noteIdx     = 0;

    function midiToHz(midi) {
      return 440 * Math.pow(2, (midi - 69) / 12);
    }

    function initAudio() {
      if (audioCtx) return;
      const AC = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AC();

      masterGain = audioCtx.createGain();
      masterGain.gain.value = 0;
      masterGain.connect(audioCtx.destination);

      // Warm reverb via feedback delay
      delayNode = audioCtx.createDelay(2.5);
      delayNode.delayTime.value = 0.38;

      fbGain = audioCtx.createGain();
      fbGain.gain.value = 0.38;

      const delayFilter = audioCtx.createBiquadFilter();
      delayFilter.type = 'lowpass';
      delayFilter.frequency.value = 1800;

      delayNode.connect(delayFilter);
      delayFilter.connect(fbGain);
      fbGain.connect(delayNode);
      fbGain.connect(masterGain);
    }

    function playNote(midi, time) {
      const freq = midiToHz(midi);

      // Two oscillators slightly detuned → richer piano-like tone
      [0, 1.5].forEach((detune, i) => {
        const osc  = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.type = i === 0 ? 'sine' : 'triangle';
        osc.frequency.value = freq * Math.pow(2, detune / 1200);

        // Envelope: soft attack, slow release
        gain.gain.setValueAtTime(0, time);
        gain.gain.linearRampToValueAtTime(i === 0 ? 0.28 : 0.12, time + 0.04);
        gain.gain.exponentialRampToValueAtTime(0.001, time + NOTE_DUR);

        osc.connect(gain);
        gain.connect(masterGain);
        gain.connect(delayNode);   // send to reverb

        osc.start(time);
        osc.stop(time + NOTE_DUR + 0.3);
      });

      // Subtle harmonic overtone (octave above)
      const osc2  = audioCtx.createOscillator();
      const gain2 = audioCtx.createGain();
      osc2.type = 'sine';
      osc2.frequency.value = freq * 2;
      gain2.gain.setValueAtTime(0, time);
      gain2.gain.linearRampToValueAtTime(0.04, time + 0.05);
      gain2.gain.exponentialRampToValueAtTime(0.001, time + NOTE_DUR * 0.6);
      osc2.connect(gain2);
      gain2.connect(masterGain);
      osc2.start(time);
      osc2.stop(time + NOTE_DUR);
    }

    function scheduleNotes() {
      const ahead = 0.25;
      while (nextTime < audioCtx.currentTime + ahead) {
        const chord  = progression[progIdx];
        const midi   = chord[noteIdx];
        playNote(midi, nextTime);

        nextTime += NOTE_GAP;
        noteIdx++;
        if (noteIdx >= chord.length) {
          noteIdx = 0;
          progIdx = (progIdx + 1) % progression.length;
          // Extra pause between chord changes
          nextTime += SPB * 0.4;
        }
      }
      if (isPlaying) {
        schedTimer = setTimeout(scheduleNotes, 80);
      }
    }

    function startMusic() {
      initAudio();
      if (audioCtx.state === 'suspended') audioCtx.resume();

      isPlaying = true;
      nextTime  = audioCtx.currentTime + 0.1;
      progIdx   = 0;
      noteIdx   = 0;

      // Fade in master volume
      masterGain.gain.cancelScheduledValues(audioCtx.currentTime);
      masterGain.gain.setValueAtTime(0, audioCtx.currentTime);
      masterGain.gain.linearRampToValueAtTime(VOL_TARGET, audioCtx.currentTime + 3);

      scheduleNotes();
      setUIPlaying(true);

      musicLabel.textContent = '♪ Wedding Melody';
      musicLabel.classList.add('visible');
      setTimeout(() => musicLabel.classList.remove('visible'), 3000);
    }

    function stopMusic() {
      isPlaying = false;
      clearTimeout(schedTimer);
      // Fade out
      masterGain.gain.cancelScheduledValues(audioCtx.currentTime);
      masterGain.gain.setValueAtTime(masterGain.gain.value, audioCtx.currentTime);
      masterGain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 1.5);
      setUIPlaying(false);
      musicLabel.textContent = '♪ Musik dimatikan';
      musicLabel.classList.add('visible');
      setTimeout(() => musicLabel.classList.remove('visible'), 2000);
    }
    function setUIPlaying(playing) {
      if (playing) {
        musicIcon.classList.add('playing');
        musicIcon.classList.remove('paused');
        musicBtn.classList.remove('paused');
      } else {
        musicIcon.classList.remove('playing');
        musicIcon.classList.add('paused');
        musicBtn.classList.add('paused');
      }
    }

    // ── Button click: toggle play/pause ──────────────────────
    musicBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (isPlaying) {
        stopMusic();
      } else {
        startMusic();
      }
    });

    // ── Triggered by intro overlay button click ───────────────
    document.addEventListener('startWeddingMusic', () => {
      startMusic();
    });

    // Default: paused icon
    setUIPlaying(false);
  }

  /* ─── Intro Overlay ─────────────────────────── */
  const introOverlay  = document.getElementById('introOverlay');
  const introEnterBtn = document.getElementById('introEnterBtn');
  const introParticlesEl = document.getElementById('introParticles');

  // Spawn floating gold particles
  if (introParticlesEl) {
    for (let i = 0; i < 25; i++) {
      const p = document.createElement('div');
      p.classList.add('intro-particle');
      const size = Math.random() * 5 + 2;
      p.style.width  = size + 'px';
      p.style.height = size + 'px';
      p.style.left   = Math.random() * 100 + '%';
      p.style.animationDuration  = (Math.random() * 8 + 6) + 's';
      p.style.animationDelay     = (Math.random() * 6) + 's';
      introParticlesEl.appendChild(p);
    }
  }

  if (introEnterBtn && introOverlay) {
    introEnterBtn.addEventListener('click', () => {
      // Dispatch event to start music (trusted click context)
      document.dispatchEvent(new CustomEvent('startWeddingMusic'));

      // Dismiss overlay with fade
      introOverlay.classList.add('dismissed');
      setTimeout(() => {
        introOverlay.style.display = 'none';
      }, 950);
    });
  }

  /* ─── Portfolio "Show More" Logic (Mobile) ───────────── */
  const portfolioGrid = document.getElementById('portfolioGrid');
  const portfolioMoreBtn = document.getElementById('portfolio-more-btn');
  
  if (portfolioGrid && portfolioMoreBtn) {
    portfolioMoreBtn.addEventListener('click', (e) => {
      e.preventDefault();
      // Remove the class that hides the extra cards
      portfolioGrid.classList.remove('hide-more');
      // Hide the button itself after showing all cards
      portfolioMoreBtn.style.display = 'none';
      
      // Optionally update the CTA text
      const ctaText = portfolioMoreBtn.previousElementSibling;
      if (ctaText && ctaText.tagName.toLowerCase() === 'p') {
        ctaText.textContent = 'Semua tema telah ditampilkan.';
      }
    });
  }

});
