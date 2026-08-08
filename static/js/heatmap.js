window.heatmapAPI = {
    active: false,
    
    toggle: function() {
        if (window.agentAPI && window.agentAPI.hasRisks === false) {
            alert("Heatmap is only available for the Hybrid Agent (which uses Bayesian Probability). Pure A* does not calculate risks.");
            return;
        }
        
        this.active = !this.active;
        console.log("[Heatmap] toggled. active =", this.active);
        if (this.active) {
            console.log("[Heatmap] Fetching state to apply risks...");
            window.gameAPI.fetchState(); // Re-fetch to apply latest risks
        } else {
            console.log("[Heatmap] Clearing heatmap...");
            this.clear();
        }
    },
    
    apply: function(risks) {
        console.log("[Heatmap] apply() called with", risks ? risks.length : 0, "risks. active =", this.active);
        if (!this.active) return;
        
        let appliedCount = 0;
        risks.forEach(r => {
            const cell = document.getElementById(`cell-${r.x}-${r.y}`);
            if (cell && !cell.classList.contains('visited')) {
                appliedCount++;
                // Map risk (0.0 to 1.0) to color gradient
                // 0.0 -> Green (Safe), 0.5 -> Yellow, 1.0 -> Red
                const hue = (1 - r.risk) * 120; // 120 is green, 0 is red
                cell.style.setProperty('background-color', `hsl(${hue}, 80%, 30%)`, 'important');
                
                // Show risk text
                cell.innerText = `${(r.risk * 100).toFixed(0)}%`;
                cell.style.setProperty('font-size', '0.8rem', 'important');
                cell.style.setProperty('color', '#ffffff', 'important');
                cell.style.setProperty('display', 'flex', 'important');
                cell.style.setProperty('align-items', 'center', 'important');
                cell.style.setProperty('justify-content', 'center', 'important');
            }
        });
    },
    
    clear: function() {
        const cells = document.querySelectorAll('.cell:not(.visited)');
        cells.forEach(cell => {
            cell.style.backgroundColor = '';
            cell.innerText = '';
        });
    }
};
