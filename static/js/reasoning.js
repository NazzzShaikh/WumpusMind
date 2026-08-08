window.reasoningAPI = {
    addLog: function(decision) {
        const container = document.getElementById('logContainer');
        
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        
        if (decision.is_manual) {
            const userMoveSpan = document.createElement('div');
            userMoveSpan.style.fontWeight = 'bold';
            userMoveSpan.style.color = 'var(--text-primary)';
            userMoveSpan.innerText = `YOUR MOVE — ${decision.manual_direction}`;
            
            const resultSpan = document.createElement('div');
            resultSpan.style.marginBottom = '0.5rem';
            resultSpan.innerText = `Result: ${decision.result_text || 'Moved successfully.'}`;
            
            const aiAdviceSpan = document.createElement('div');
            aiAdviceSpan.style.color = 'var(--text-secondary)';
            aiAdviceSpan.style.borderTop = '1px solid var(--border-color)';
            aiAdviceSpan.style.paddingTop = '0.5rem';
            aiAdviceSpan.style.fontSize = '0.85rem';
            aiAdviceSpan.innerText = `AI's advice at this turn: Would have chosen ${decision.ai_action}. Reason: ${decision.ai_explanation}`;
            
            entry.appendChild(userMoveSpan);
            entry.appendChild(resultSpan);
            entry.appendChild(aiAdviceSpan);
        } else {
            const reasonSpan = document.createElement('div');
            reasonSpan.className = 'reason';
            reasonSpan.innerText = `${decision.reason} - Conf: ${(decision.confidence * 100).toFixed(0)}%`;
            
            const actionSpan = document.createElement('div');
            actionSpan.style.fontWeight = 'bold';
            actionSpan.innerText = `Action: ${decision.action}`;
            
            const expSpan = document.createElement('div');
            expSpan.innerText = decision.explanation;
            
            entry.appendChild(reasonSpan);
            entry.appendChild(actionSpan);
            entry.appendChild(expSpan);
        }
        
        container.appendChild(entry);
        
        // Auto scroll to bottom
        container.scrollTop = container.scrollHeight;
        
        // Highlight cell logic if target exists
        if (decision.target) {
            entry.style.cursor = 'pointer';
            entry.onclick = () => {
                const cellId = `cell-${decision.target[0]}-${decision.target[1]}`;
                const cell = document.getElementById(cellId);
                if (cell) {
                    gsap.to(cell, {backgroundColor: 'var(--accent)', duration: 0.2, yoyo: true, repeat: 1});
                }
            };
        }
    }
};
