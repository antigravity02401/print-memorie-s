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

});
