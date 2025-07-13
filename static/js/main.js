document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const mobileThemeToggle = document.getElementById('mobile-theme-toggle');
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenuClose = document.getElementById('mobile-menu-close');
    const mobileMenu = document.getElementById('mobile-menu');
    const scrollTopButton = document.getElementById('scroll-top');
    const html = document.documentElement;

    // Debug logs
    console.log('Mobile Menu Button:', mobileMenuButton);
    console.log('Mobile Menu:', mobileMenu);
    console.log('Mobile Menu Close:', mobileMenuClose);
    console.log('Theme Toggle:', themeToggle);
    console.log('Mobile Theme Toggle:', mobileThemeToggle);

    // Theme Toggle
    const applyTheme = () => {
        const theme = localStorage.getItem('theme') || 
                     (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        html.classList.remove('dark', 'light');
        html.classList.add(theme);
        console.log('Applied theme:', theme);
    };

    applyTheme(); // Apply theme on page load

    themeToggle?.addEventListener('click', () => {
        html.classList.toggle('dark');
        const newTheme = html.classList.contains('dark') ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);
        console.log('Toggled theme to:', newTheme);
    });

    mobileThemeToggle?.addEventListener('click', () => {
        html.classList.toggle('dark');
        const newTheme = html.classList.contains('dark') ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);
        console.log('Mobile toggled theme to:', newTheme);
    });

    // Mobile Menu Toggle
    if (mobileMenuButton && mobileMenu && mobileMenuClose) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.remove('hidden');
            mobileMenu.classList.add('open');
            mobileMenuButton.setAttribute('aria-expanded', 'true');
            document.body.style.overflow = 'hidden'; // Prevent scrolling
            console.log('Mobile menu opened');
        });

        mobileMenuClose.addEventListener('click', () => {
            mobileMenu.classList.remove('open');
            mobileMenu.classList.add('hidden');
            mobileMenuButton.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = 'auto'; // Restore scrolling
            console.log('Mobile menu closed');
        });

        // Close mobile menu when clicking a link
        document.querySelectorAll('#mobile-menu .scroll-link, #mobile-menu a:not(.scroll-link)').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('open');
                mobileMenu.classList.add('hidden');
                mobileMenuButton.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = 'auto';
                console.log('Mobile menu closed via link click');
            });
        });
    } else {
        console.error('Mobile menu elements not found:', { mobileMenuButton, mobileMenu, mobileMenuClose });
    }

    // Smooth Scrolling
    document.querySelectorAll('.scroll-link').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').split('#')[1];
            if (!targetId) return;

            // If on a different page, redirect to home with hash
            if (window.location.pathname !== '/') {
                window.location.href = `/${'#' + targetId}`;
                return;
            }

            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                history.pushState(null, null, '#' + targetId);
                console.log('Scrolled to:', targetId);
            }
        });
    });

    // Scroll Highlight Effect
    const sections = document.querySelectorAll('section[id]');
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            if (window.scrollY >= sectionTop) {
                current = section.getAttribute('id');
            }
        });
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current)) {
                link.classList.add('active');
            }
        });
    });

    // Scroll to Top Button
    if (scrollTopButton) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollTopButton.classList.remove('hidden');
            } else {
                scrollTopButton.classList.add('hidden');
            }
        });
        scrollTopButton.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            console.log('Scrolled to top');
        });
    }

    // Handle Initial Hash
    if (window.location.hash) {
        const target = document.querySelector(window.location.hash);
        if (target) {
            window.scrollTo({ top: target.offsetTop - 80, behavior: 'smooth' });
            console.log('Initial scroll to:', window.location.hash);
        }
    }

    // Initialize AOS
    AOS.init({ duration: 800, easing: 'ease-in-out', once: true });

    // Initialize Particles.js (only on home page and desktop)


    // Initialize Typed.js (only on home page)
    if (document.getElementById('typed-text')) {
        new Typed('#typed-text', {
            strings: ["Hi, I am Arvind Kumar", "Web Developer"],
            typeSpeed: 50,
            backSpeed: 30,
            loop: true
        });
        console.log('Typed.js initialized');
    }
});


function filterProjects(category, event) {
        const cards = document.querySelectorAll('.project-card');
        const buttons = document.querySelectorAll('.filter-btn');

        buttons.forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');

        cards.forEach(card => {
            const cardCategory = card.getAttribute('data-category');
            if (category === 'all' || cardCategory === category) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }