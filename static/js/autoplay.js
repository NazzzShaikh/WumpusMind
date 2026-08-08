window.autoplayAPI = {
    intervalId: null,
    speedMs: 1000,
    
    toggle: function() {
        if (this.intervalId) {
            this.stop();
        } else {
            this.start();
        }
    },
    
    start: function() {
        if (window.gameAPI.isGameOver) return;
        
        const btn = document.getElementById('autoplayBtn');
        if (btn) {
            btn.innerText = "Stop Autoplay";
            btn.style.background = "var(--danger)";
        }
        
        this.intervalId = setInterval(() => {
            window.gameAPI.step();
        }, this.speedMs);
    },
    
    stop: function() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        
        const btn = document.getElementById('autoplayBtn');
        if (btn) {
            btn.innerText = "Autoplay";
            btn.style.background = "var(--safe)";
        }
    }
};
