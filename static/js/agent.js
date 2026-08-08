window.agentAPI = {
    mode: 'autoplay', // locked session mode
    
    setMode: function(newMode) {
        this.mode = newMode;
        const dpad = document.getElementById('dpad');
        const stepBtn = document.getElementById('stepBtn');
        const autoplayBtn = document.getElementById('autoplayBtn');
        const modeLabel = document.getElementById('activeModeLabel');
        
        if (modeLabel) {
            modeLabel.innerText = newMode === 'manual' ? 'Manual Play' : 'Autoplay / AI';
        }
        
        if (newMode === 'manual') {
            window.autoplayAPI.stop();
            if(dpad) dpad.style.display = 'block';
            if(stepBtn) stepBtn.style.display = 'none';
            if(autoplayBtn) autoplayBtn.style.display = 'none';
        } else {
            if(dpad) dpad.style.display = 'none';
            if(stepBtn) { stepBtn.style.display = 'inline-block'; stepBtn.disabled = false; }
            if(autoplayBtn) { autoplayBtn.style.display = 'inline-block'; autoplayBtn.disabled = false; }
        }
    },
    
    manualMove: function(direction) {
        if (this.mode !== 'manual' || window.gameAPI.isGameOver) return;
        window.gameAPI.step(direction);
    }
};

// Keyboard controls
window.addEventListener('keydown', function(e) {
    if (window.agentAPI.mode !== 'manual' || window.gameAPI.isGameOver) return;
    
    const key = e.key.toLowerCase();
    let dir = null;
    if (key === 'arrowup' || key === 'w') dir = 'UP';
    else if (key === 'arrowdown' || key === 's') dir = 'DOWN';
    else if (key === 'arrowleft' || key === 'a') dir = 'LEFT';
    else if (key === 'arrowright' || key === 'd') dir = 'RIGHT';
    
    if (dir) {
        // Prevent default scrolling for arrows
        if(e.key.startsWith('Arrow')) e.preventDefault();
        window.agentAPI.manualMove(dir);
    }
});

window.gameAPI = {
    isGameOver: false,
    
    fetchState: function() {
        fetch('/api/state')
        .then(res => res.json())
        .then(data => {
            const env = data.env;
            const agentInfo = data.agent;
            
            // Set locked play mode
            if (agentInfo.play_mode) {
                window.agentAPI.setMode(agentInfo.play_mode);
            }
            
            window.agentAPI.hasRisks = !!agentInfo.risks;
            
            document.getElementById('scoreDisplay').innerText = env.score;
            
            // First time setup
            if (!document.getElementById('board').hasChildNodes() || 
                document.getElementById('board').style.gridTemplateColumns === "") {
                window.boardAPI.init(env.size);
                
                if (agentInfo.initial_log) {
                    window.reasoningAPI.addLog(agentInfo.initial_log);
                }
            }
            
            // Render board cells
            env.grid.forEach(cell => {
                const isVisited = agentInfo.visited ? agentInfo.visited.some(v => v[0] === cell.x && v[1] === cell.y) : false;
                window.boardAPI.updateCell(cell.x, cell.y, cell, isVisited);
            });
            
            // Render Heatmap
            if (agentInfo.risks && window.heatmapAPI.active) {
                window.heatmapAPI.apply(agentInfo.risks);
            }
            
            // Move Agent
            window.boardAPI.moveAgent(env.agent_pos[0], env.agent_pos[1], env.agent_dir);
            
            // Render Percept Warnings
            if (env.current_percepts) {
                window.boardAPI.updatePerceptWarning(env.agent_pos[0], env.agent_pos[1], env.current_percepts);
            }
            
            // Set sprite state based on env
            const sprite = document.getElementById('agent-sprite');
            if (sprite && window.boardAPI.getAgentSVG) {
                console.log("Icon swap logic running. agent_alive:", env.agent_alive, "agent_escaped:", env.agent_escaped);
                sprite.innerHTML = window.boardAPI.getAgentSVG(env.agent_alive, env.agent_escaped);
            }
        });
    },
    
    step: function(manualDirection = null) {
        if (this.isGameOver || this.isFetching) return;
        this.isFetching = true;
        
        fetch('/api/step', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ manual_direction: manualDirection })
        })
        .then(res => {
            if (!res.ok) throw new Error('Server error: ' + res.status);
            return res.json();
        })
        .then(data => {
            if (data.status === 'game_over') {
                this.isGameOver = true;
                this.isFetching = false;
                window.autoplayAPI.stop();
                return;
            }
            
            // Update Log
            if (data.decision) {
                window.reasoningAPI.addLog(data.decision);
                
                if (data.decision.reason.includes("DEATH")) {
                    this.isGameOver = true;
                    
                    const sprite = document.getElementById('agent-sprite');
                    if (sprite) {
                        gsap.timeline()
                            .to(sprite, {x: "+=5", duration: 0.05, yoyo: true, repeat: 5})
                            .to(sprite, {opacity: 0, scale: 0.5, duration: 0.2})
                            .to(sprite, {opacity: 1, scale: 1, duration: 0.2})
                            .call(() => {
                                document.getElementById('statusDisplay').innerText = "DEAD";
                                document.getElementById('statusDisplay').style.color = "var(--danger)";
                            });
                    } else {
                        document.getElementById('statusDisplay').innerText = "DEAD";
                        document.getElementById('statusDisplay').style.color = "var(--danger)";
                    }
                    
                    window.autoplayAPI.stop();
                }
                
                if (data.decision.reason.includes("VICTORY")) {
                    this.isGameOver = true;
                    
                    const sprite = document.getElementById('agent-sprite');
                    if (sprite) {
                        gsap.timeline()
                            .to(sprite, {y: "-=10", duration: 0.2, yoyo: true, repeat: 3})
                            .call(() => {
                                document.getElementById('statusDisplay').innerText = "ESCAPED";
                                document.getElementById('statusDisplay').style.color = "var(--gold)";
                            });
                    } else {
                        document.getElementById('statusDisplay').innerText = "ESCAPED";
                        document.getElementById('statusDisplay').style.color = "var(--gold)";
                    }
                    
                    window.autoplayAPI.stop();
                }
            }
            
            // Disable UI controls if game is over
            if (this.isGameOver) {
                const stepBtn = document.getElementById('stepBtn');
                const autoplayBtn = document.getElementById('autoplayBtn');
                if (stepBtn) stepBtn.disabled = true;
                if (autoplayBtn) autoplayBtn.disabled = true;
            }
            
            this.isFetching = false;
            // Re-fetch state to update visual representation
            this.fetchState();
        })
        .catch(err => {
            console.error("Autoplay JS Error:", err);
            this.isFetching = false;
            window.autoplayAPI.stop();
        });
    },
    
    spawnConfetti: function(target) {
        const rect = target.getBoundingClientRect();
        const colors = ['#fbbf24', '#3b82f6', '#22c55e', '#ef4444'];
        for(let i=0; i<15; i++) {
            const confetti = document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.left = rect.left + rect.width/2 + 'px';
            confetti.style.top = rect.top + rect.height/2 + 'px';
            confetti.style.width = '8px';
            confetti.style.height = '8px';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.borderRadius = '50%';
            confetti.style.zIndex = '100';
            confetti.style.pointerEvents = 'none';
            document.body.appendChild(confetti);
            
            gsap.to(confetti, {
                x: (Math.random() - 0.5) * 150,
                y: (Math.random() - 0.5) * 150 - 50,
                opacity: 0,
                scale: 0.5,
                duration: 0.8 + Math.random(),
                ease: "power2.out",
                onComplete: () => confetti.remove()
            });
        }
    }
};
