class AnimatedDetails extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        const baseUrl = window.animatedDetailsBaseUrl || '.';
        const linkElem = document.createElement('link');
        linkElem.setAttribute('rel', 'stylesheet');
        linkElem.setAttribute('href', `${baseUrl}/files/style.css`);

        const template = document.createElement('template');
        template.innerHTML = `<div class="summary-trigger" id="trigger" role="button" tabindex="0" aria-expanded="false">
        <slot name="summary">Detaljer</slot>
      </div>
      <div class="content-wrapper">
        <div class="content-box">
          <div class="inner-padding">
            <slot></slot>
          </div>
        </div>
      </div>`;

        this.shadowRoot.appendChild(linkElem);
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.trigger = this.shadowRoot.getElementById('trigger');
        this.trigger.addEventListener('click', () => this.toggle());

        this.trigger.addEventListener('keydown', (e) => {
            if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                this.toggle();
            }
        });

        this._updateAccessibility();
    }

    toggle() {
        if (this.hasAttribute('open')) {
            this.removeAttribute('open');
        } else {
            this.setAttribute('open', '');
        }
        this._updateAccessibility();
    }

    _updateAccessibility() {
        if (this.trigger) {
            const isOpen = this.hasAttribute('open');
            this.trigger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        }
    }
}
customElements.define('animated-details', AnimatedDetails);