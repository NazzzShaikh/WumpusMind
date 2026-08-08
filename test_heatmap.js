const fs = require('fs');
const js = fs.readFileSync('/home/nazzzshaikh/Desktop/WumpusMind/static/js/heatmap.js', 'utf8');
console.log(js.includes('console.log'));
