window.boardAPI = {
    size: 4,
    cellSize: 64, // 60px cell + 4px gap
    
    getAgentSVG: function(isAlive, isEscaped) {
        if (!isAlive) {
            return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="12" r="1"/><circle cx="15" cy="12" r="1"/><path d="M8 20v2h8v-2"/><path d="m12.5 17-.5-1-.5 1h1z"/><path d="M16 20a2 2 0 0 0 1.56-3.25 8 8 0 1 0-11.12 0A2 2 0 0 0 8 20"/></svg>';
        } else if (isEscaped) {
            return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="var(--gold)" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>';
        } else {
            return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>';
        }
    },
    
    init: function(size) {
        this.size = size;
        const board = document.getElementById('board');
        
        // Setup grid
        board.style.display = 'grid';
        board.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
        board.style.gridTemplateRows = `repeat(${size}, 1fr)`;
        board.style.width = `${size * this.cellSize + 8}px`; // +8 for padding
        board.style.height = `${size * this.cellSize + 8}px`;
        
        board.innerHTML = `<div id="agent-sprite">${this.getAgentSVG(true, false)}</div>`;
        
        // Generate cells
        for (let y = size - 1; y >= 0; y--) {
            for (let x = 0; x < size; x++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.id = `cell-${x}-${y}`;
                board.appendChild(cell);
            }
        }
    },
    
    updateCell: function(x, y, data, isVisited) {
        const cell = document.getElementById(`cell-${x}-${y}`);
        if (!cell) return;
        
        if (isVisited && !cell.classList.contains('visited')) {
            cell.classList.add('visited');
            
            // Clear any heatmap styles/text before revealing
            cell.style.backgroundColor = '';
            cell.innerText = '';
            
            // Tile reveal animation
            gsap.fromTo(cell, {scale: 0.8, opacity: 0}, {scale: 1, opacity: 1, duration: 0.25, ease: "power2.out"});
            
            // Remove previous classes
            cell.className = 'cell visited';
            
            if (data.wumpus) cell.classList.add('wumpus');
            if (data.pit) cell.classList.add('pit');
            if (data.gold) cell.classList.add('gold');
            
            // Note: Percepts aren't directly in the grid dict, 
            // but we might compute them or receive them.
            // For now, if the agent visits, we'll reveal the actual contents.
        }
    },
    
    addPercept: function(x, y, perceptType) {
        const cell = document.getElementById(`cell-${x}-${y}`);
        if (cell && !cell.classList.contains(perceptType)) {
            cell.classList.add(perceptType);
        }
    },
    
    moveAgent: function(x, y, dir) {
        const sprite = document.getElementById('agent-sprite');
        
        // Board is 0-indexed, bottom-left is 0,0
        // Calculate px position based on CSS grid
        const padding = 4;
        const left = padding + (x * this.cellSize);
        const top = padding + ((this.size - 1 - y) * this.cellSize);
        
        let rotate = 0;
        if (dir === 0) rotate = 0;      // Right
        else if (dir === 1) rotate = -90; // Up
        else if (dir === 2) rotate = 180; // Left
        else if (dir === 3) rotate = 90;  // Down

        // Handle initial load vs animated movement
        if (!this.lastAgentPos) {
            gsap.set(sprite, { x: left, y: top, rotation: rotate });
            this.lastAgentPos = {x, y};
            return;
        }

        this.lastAgentPos = {x, y};
        // GSAP tween for smooth slide
        gsap.to(sprite, {
            x: left, 
            y: top, 
            rotation: rotate,
            duration: 0.35,
            ease: "power2.out"
        });
    },
    
    updatePerceptWarning: function(x, y, percepts) {
        // Clear previous warnings and icons from all cells
        document.querySelectorAll('.cell').forEach(c => {
            c.classList.remove('warning-amber', 'warning-red');
            const icons = c.querySelector('.percept-icons');
            if (icons) icons.remove();
        });
        
        const cell = document.getElementById(`cell-${x}-${y}`);
        if (!cell || !percepts) return;
        
        let hasBreeze = percepts.breeze;
        let hasStench = percepts.stench;
        
        if (hasBreeze || hasStench) {
            if (hasBreeze && hasStench) {
                cell.classList.add('warning-red');
            } else {
                cell.classList.add('warning-amber');
            }
            
            // Inject emoji icons
            const iconContainer = document.createElement('div');
            iconContainer.className = 'percept-icons';
            if (hasBreeze) iconContainer.innerHTML += '<span>🌬️</span>';
            if (hasStench) iconContainer.innerHTML += '<span>🤢</span>';
            cell.appendChild(iconContainer);
            
            // Animate appearance with small pop/fade
            gsap.from(iconContainer, {scale: 0, opacity: 0, duration: 0.3, ease: "back.out(1.7)"});
        }
    }
};
