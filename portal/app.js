document.addEventListener('DOMContentLoaded', () => {
    // Init AOS
    AOS.init({
        duration: 800,
        once: true,
        offset: 100
    });

    const app = {
        data: null,
        lang: 'cn',

        async init() {
            try {
                const response = await fetch('site_content.json');
                this.data = await response.json();
                this.renderAll();
                this.setupEvents();
            } catch (error) {
                console.error('Failed to load site content:', error);
                document.body.innerHTML = '<h1 style="text-align:center; margin-top:20vh">Loading Error. Please check console.</h1>';
            }
        },

        t(obj) {
            if (!obj) return '';
            if (typeof obj === 'string') return obj;
            return obj[this.lang] || obj['cn'] || '';
        },

        setupEvents() {
            // Lang Toggle
            document.getElementById('lang-toggle').addEventListener('click', () => {
                this.lang = this.lang === 'cn' ? 'en' : 'cn';
                this.renderAll();
                // Update button text
                document.getElementById('lang-toggle').textContent = this.lang === 'cn' ? 'EN / 中文' : '中文 / EN';
            });
        },

        renderAll() {
            this.renderNav();
            this.renderHero();
            this.renderAbout();
            this.renderServices();
            this.renderTeam();
            this.renderCases();
            this.renderInvest();
            this.renderContact();
        },

        renderNav() {
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                // Simple mapping for static nav items if needed, or just rely on static HTML + manual toggle if complex
                // For now, let's leave static nav text as is or update if we had a dict.
                // Since nav text is simple, we can just toggle classes or leave mixed.
                // Let's actually update them manually for polish.
                const dict = {
                    'nav.home': {cn: '首页', en: 'Home'},
                    'nav.about': {cn: '关于', en: 'About'},
                    'nav.services': {cn: '服务', en: 'Services'},
                    'nav.team': {cn: '团队', en: 'Team'},
                    'nav.contact': {cn: '联系', en: 'Contact'},
                    'hero.cta': {cn: '加入我们', en: 'Join Us'},
                    'hero.more': {cn: '了解更多', en: 'Learn More'},
                    'section.about': {cn: '关于我们', en: 'About Us'},
                    'section.services': {cn: '我们的服务', en: 'Our Services'},
                    'section.team': {cn: '核心团队', en: 'Core Team'},
                    'section.cases': {cn: '成功案例', en: 'Success Stories'},
                    'section.invest': {cn: '生态与投资', en: 'Ecosystem & Invest'},
                    'section.contact': {cn: '联系我们', en: 'Contact Us'}
                };
                if (dict[key]) {
                    el.textContent = this.t(dict[key]);
                }
            });
        },

        renderHero() {
            const hero = this.data.hero;
            document.getElementById('hero-title').textContent = hero.title;
            document.getElementById('hero-subtitle').textContent = this.t(hero.subtitle);
            // Background image?
            // if (hero.bg_image) {
            //     document.querySelector('.hero-bg').style.backgroundImage = `url('${hero.bg_image}')`;
            // }
        },

        renderAbout() {
            const about = this.data.about;
            document.getElementById('about-intro').textContent = this.t(about.intro);
            
            // Stats
            const statsHtml = about.stats.map(stat => `
                <div class="stat-card">
                    <span class="stat-value">${stat.value}</span>
                    <span class="stat-label">${this.t(stat.label)}</span>
                </div>
            `).join('');
            document.getElementById('stats-grid').innerHTML = statsHtml;

            // Links
            const linksHtml = Object.entries(about.links).map(([key, url]) => `
                <a href="${url}" target="_blank" class="social-icon">${key.toUpperCase()}</a>
            `).join('');
            document.getElementById('about-links').innerHTML = linksHtml;
        },

        renderServices() {
            const services = this.data.services;
            const html = services.map(s => `
                <div class="service-card">
                    <h3>${this.t(s.title)}</h3>
                    <p>${this.t(s.desc)}</p>
                </div>
            `).join('');
            document.getElementById('services-grid').innerHTML = html;
        },

        renderTeam() {
            const team = this.data.team;
            const html = team.map(member => `
                <div class="team-card">
                    <div class="team-img-wrapper">
                        <a href="${member.twitter}" target="_blank" class="team-link">
                            ${member.image ? `<img src="${member.image}" class="team-img" alt="${member.name}">` : ''}
                            <div class="team-overlay">
                                <span class="twitter-icon">𝕏</span>
                            </div>
                        </a>
                    </div>
                    <div class="team-info">
                        <div class="team-header">
                            <h3>${member.name}</h3>
                            ${member.followers ? `<span class="team-followers">${member.followers} Fans</span>` : ''}
                        </div>
                        <p class="text-muted">${this.t(member.desc)}</p>
                    </div>
                </div>
            `).join('');
            document.getElementById('team-grid').innerHTML = html;
        },

        renderCases() {
            const cases = this.data.cases;
            const html = cases.map((c, index) => `
                <div class="case-card" data-aos="fade-up">
                    <div class="case-content">
                        <div class="case-text">
                            <h3>${this.t(c.title)}</h3>
                            <p>${this.t(c.desc)}</p>
                        </div>
                        <div class="case-gallery">
                            ${c.images.slice(0, 4).map(img => `
                                <img src="${img}" class="case-img" loading="lazy">
                            `).join('')}
                        </div>
                    </div>
                </div>
            `).join('');
            document.getElementById('cases-container').innerHTML = html;
        },

        renderInvest() {
            const gallery = this.data.gallery;
            if (!gallery || gallery.length === 0) return;
            const html = gallery.map(img => `
                <img src="${img}" class="gallery-item" loading="lazy">
            `).join('');
            document.getElementById('gallery-grid').innerHTML = html;
        },

        renderContact() {
            const contact = this.data.contact;
            document.getElementById('contact-text').textContent = this.t(contact.text);
            
            const html = `
                <div class="contact-item">
                    <strong>Email:</strong> <a href="mailto:${contact.email}" style="color:var(--secondary)">${contact.email}</a>
                </div>
                <div class="contact-item">
                    <strong>Twitter:</strong> <a href="https://twitter.com/${contact.twitter.replace('@','')}" target="_blank" style="color:var(--secondary)">${contact.twitter}</a>
                </div>
            `;
            document.getElementById('contact-info').innerHTML = html;
        }
    };

    app.init();
});
