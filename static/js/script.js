/* ============================================
   HANGO — Premium E-Commerce
   Motion Controller & Interactions
   ============================================ */
(function () {
    'use strict';

    const ready = (fn) => document.readyState !== 'loading' ? fn() : document.addEventListener('DOMContentLoaded', fn);

    ready(function () {

        /* ══════════════════════════════════════════
           1. INTERSECTION OBSERVER — Reveal on Scroll
           ══════════════════════════════════════════ */
        const revealEls = document.querySelectorAll('.reveal');
        if (revealEls.length && 'IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const delay = entry.target.dataset.delay || '0s';
                        entry.target.style.transitionDelay = delay;
                        entry.target.classList.add('revealed');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
            revealEls.forEach((el) => observer.observe(el));
        } else {
            revealEls.forEach((el) => el.classList.add('revealed'));
        }

        /* ══════════════════════════════════════════
           2. NAVBAR — Scroll Effect & Toggle
           ══════════════════════════════════════════ */
        const navbar = document.getElementById('navbar');
        const menuToggle = document.getElementById('menuToggle');
        const navbarNav = document.getElementById('navbarNav');

        let ticking = false;
        const handleScroll = () => {
            if (navbar) {
                navbar.classList.toggle('scrolled', window.scrollY > 20);
            }
            ticking = false;
        };
        window.addEventListener('scroll', () => {
            if (!ticking) { requestAnimationFrame(handleScroll); ticking = true; }
        }, { passive: true });

        if (menuToggle && navbarNav) {
            menuToggle.addEventListener('click', () => {
                menuToggle.classList.toggle('active');
                navbarNav.classList.toggle('open');
            });
            navbarNav.querySelectorAll('a').forEach((a) => {
                a.addEventListener('click', () => {
                    menuToggle.classList.remove('active');
                    navbarNav.classList.remove('open');
                });
            });
        }

        /* ══════════════════════════════════════════
           3. SMOOTH SCROLL
           ══════════════════════════════════════════ */
        document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
            anchor.addEventListener('click', function (e) {
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    e.preventDefault();
                    const offset = navbar ? navbar.offsetHeight + 16 : 80;
                    window.scrollTo({ top: target.offsetTop - offset, behavior: 'smooth' });
                }
            });
        });

        /* ══════════════════════════════════════════
           4. BUTTON RIPPLE EFFECT
           ══════════════════════════════════════════ */
        document.querySelectorAll('.btn').forEach((btn) => {
            btn.addEventListener('mousedown', (e) => {
                const rect = btn.getBoundingClientRect();
                btn.style.setProperty('--ripple-x', ((e.clientX - rect.left) / rect.width * 100) + '%');
                btn.style.setProperty('--ripple-y', ((e.clientY - rect.top) / rect.height * 100) + '%');
            });
        });

        /* ══════════════════════════════════════════
           5. DIRECTORY FILTER
           ══════════════════════════════════════════ */
        const filterBtns = document.querySelectorAll('.filter-btn');
        const dirCards = document.querySelectorAll('.dir-card');
        if (filterBtns.length && dirCards.length) {
            filterBtns.forEach((btn) => {
                btn.addEventListener('click', () => {
                    filterBtns.forEach((b) => b.classList.remove('active'));
                    btn.classList.add('active');
                    const cat = btn.dataset.category;
                    dirCards.forEach((card) => {
                        const show = cat === 'all' || card.dataset.category === cat;
                        card.style.opacity = show ? '' : '0';
                        card.style.transform = show ? '' : 'translateY(15px)';
                        setTimeout(() => { card.style.display = show ? '' : 'none'; }, show ? 0 : 350);
                        if (show) { card.style.display = ''; }
                    });
                });
            });
        }

        /* ══════════════════════════════════════════
           6. AJAX LEAD FORM
           ══════════════════════════════════════════ */
        const leadForm = document.getElementById('lead-form');
        if (leadForm) {
            leadForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const submitBtn = leadForm.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span style="display:inline-flex;gap:6px;align-items:center"><span class="spinner"></span> Sending…</span>';
                submitBtn.disabled = true; submitBtn.style.opacity = '.7';
                submitBtn.setAttribute('aria-busy', 'true');

                try {
                    const formData = new FormData(leadForm);
                    const data = Object.fromEntries(formData.entries());
                    const response = await fetch('/api/lead', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    const payload = await response.json().catch(() => ({}));
                    const successEl = document.getElementById('formSuccess');
                    if (response.ok) {
                        leadForm.reset();
                        if (successEl) {
                            successEl.textContent = payload.message || 'Thank you. Your inquiry has been sent.';
                            successEl.style.background = '';
                            successEl.style.color = '';
                            successEl.classList.add('show');
                            setTimeout(() => successEl.classList.remove('show'), 5000);
                        }
                    } else { throw new Error(payload.error || 'Server error'); }
                } catch (err) {
                    const successEl = document.getElementById('formSuccess');
                    if (successEl) {
                        successEl.textContent = '⚠️ Something went wrong. Please try again.';
                        successEl.style.background = '#fef2f2'; successEl.style.color = '#991b1b';
                        successEl.classList.add('show');
                        setTimeout(() => { successEl.classList.remove('show'); successEl.textContent = 'Thank you! Your inquiry has been sent successfully.'; successEl.style.background = ''; successEl.style.color = ''; }, 5000);
                    }
                } finally {
                    submitBtn.innerHTML = originalText; submitBtn.disabled = false; submitBtn.style.opacity = '';
                    submitBtn.removeAttribute('aria-busy');
                }
            });
        }

        /* ══════════════════════════════════════════
           7. FAQ ACCORDION
           ══════════════════════════════════════════ */
        document.querySelectorAll('.faq-question').forEach(btn => {
            btn.addEventListener('click', () => {
                const item = btn.closest('.faq-item');
                const answer = item.querySelector('.faq-answer');
                const isActive = item.classList.contains('active');
                // Close all
                document.querySelectorAll('.faq-item').forEach(fi => {
                    fi.classList.remove('active');
                    fi.querySelector('.faq-answer').style.maxHeight = null;
                });
                if (!isActive) {
                    item.classList.add('active');
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                }
            });
        });

        /* ══════════════════════════════════════════
           8. PRODUCT CARD 3D TILT (Desktop)
           ══════════════════════════════════════════ */
        if (window.innerWidth > 768) {
            document.querySelectorAll('.product-card, .service-card').forEach(card => {
                card.addEventListener('mousemove', (e) => {
                    const rect = card.getBoundingClientRect();
                    const x = (e.clientX - rect.left) / rect.width - 0.5;
                    const y = (e.clientY - rect.top) / rect.height - 0.5;
                    card.style.transform = `translateY(-6px) perspective(600px) rotateY(${x * 6}deg) rotateX(${-y * 6}deg)`;
                });
                card.addEventListener('mouseleave', () => { card.style.transform = ''; });
            });
        }

        /* ══════════════════════════════════════════
           9. PARALLAX HERO IMAGE
           ══════════════════════════════════════════ */
        const heroImg = document.querySelector('.hero-image');
        if (heroImg && window.innerWidth > 1024) {
            window.addEventListener('scroll', () => {
                const scrollY = window.scrollY;
                if (scrollY < 800) {
                    heroImg.style.transform = `translateY(${scrollY * 0.15}px)`;
                }
            }, { passive: true });
        }

        /* ══════════════════════════════════════════
           10. WISHLIST HEART TOGGLE
           ══════════════════════════════════════════ */
        document.querySelectorAll('.product-wish').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const svg = btn.querySelector('svg');
                const isFilled = svg.getAttribute('fill') === 'var(--sale-red)';
                svg.setAttribute('fill', isFilled ? 'none' : 'var(--sale-red)');
                svg.setAttribute('stroke', isFilled ? 'var(--text-secondary)' : 'var(--sale-red)');
                btn.style.transform = 'scale(1.3)';
                setTimeout(() => { btn.style.transform = ''; }, 200);
            });
        });

        /* ══════════════════════════════════════════
           11. DASHBOARD — Counting Stats Animation
           ══════════════════════════════════════════ */
        const countEls = document.querySelectorAll('[data-count]');
        if (countEls.length) {
            const countObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const el = entry.target;
                        const target = parseInt(el.dataset.count, 10);
                        const duration = 1200;
                        const start = performance.now();
                        const animate = (now) => {
                            const progress = Math.min((now - start) / duration, 1);
                            const eased = 1 - Math.pow(1 - progress, 3);
                            el.textContent = Math.round(eased * target);
                            if (progress < 1) requestAnimationFrame(animate);
                        };
                        requestAnimationFrame(animate);
                        countObserver.unobserve(el);
                    }
                });
            }, { threshold: 0.5 });
            countEls.forEach(el => countObserver.observe(el));
        }

        /* ══════════════════════════════════════════
           12. DASHBOARD — Floating Particles
           ══════════════════════════════════════════ */
        const particlesContainer = document.getElementById('dashParticles');
        if (particlesContainer) {
            const spawnParticle = () => {
                const p = document.createElement('div');
                p.classList.add('dash-particle');
                p.style.left = Math.random() * 100 + '%';
                p.style.bottom = '-5px';
                const size = 2 + Math.random() * 3;
                p.style.width = size + 'px';
                p.style.height = size + 'px';
                p.style.animationDuration = (4 + Math.random() * 4) + 's';
                p.style.opacity = (0.15 + Math.random() * 0.35).toFixed(2);
                particlesContainer.appendChild(p);
                setTimeout(() => p.remove(), 8000);
            };
            // Spawn initial batch
            for (let i = 0; i < 15; i++) {
                setTimeout(spawnParticle, i * 200);
            }
            // Keep spawning
            setInterval(spawnParticle, 500);
        }

        /* ══════════════════════════════════════════
           13. DASHBOARD — Enhanced Filter Transitions
           ══════════════════════════════════════════ */
        const dashFilterBtns = document.querySelectorAll('.dash-filter-bar .filter-btn');
        const dashCards = document.querySelectorAll('#directoryGrid .dir-card');
        if (dashFilterBtns.length && dashCards.length) {
            dashFilterBtns.forEach(btn => {
                btn.addEventListener('click', () => {
                    dashFilterBtns.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    const cat = btn.dataset.category;
                    let delay = 0;
                    dashCards.forEach(card => {
                        const show = cat === 'all' || card.dataset.category === cat;
                        if (show) {
                            card.style.display = '';
                            setTimeout(() => {
                                card.style.opacity = '1';
                                card.style.transform = 'translateY(0) scale(1)';
                            }, delay);
                            delay += 50;
                        } else {
                            card.style.opacity = '0';
                            card.style.transform = 'translateY(15px) scale(.97)';
                            setTimeout(() => { card.style.display = 'none'; }, 350);
                        }
                    });
                });
            });
        }

    });
})();
