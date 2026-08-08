const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const dom = new JSDOM(`
<!DOCTYPE html>
<html>
<body>
    <div class="board-container">
        <div id="board">
            <div id="agent-sprite"></div>
        </div>
    </div>
</body>
</html>
`);

const document = dom.window.document;

// Simulate board.js
const boardAPI = {
    size: 4,
    cellSize: 60, // Fixed
    
    init: function(size) {
        this.size = size;
        const board = document.getElementById('board');
        
        // Setup grid
        board.style.gridTemplateColumns = \`repeat(\${size}, 60px)\`;
        board.style.gridTemplateRows = \`repeat(\${size}, 60px)\`;
        board.style.width = 'max-content';
        board.style.height = 'max-content';
        
        board.innerHTML = '<div id="agent-sprite"></div>';
        
        // Generate cells
        for (let y = size - 1; y >= 0; y--) {
            for (let x = 0; x < size; x++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.id = \`cell-\${x}-\${y}\`;
                board.appendChild(cell);
            }
        }
    }
};

// Simulate agent.js logic
boardAPI.init(4);

console.log(document.getElementById('board').outerHTML);
