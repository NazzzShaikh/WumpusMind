const puppeteer = require('puppeteer');

(async () => {
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        
        // Listen to console logs
        page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
        
        await page.goto('http://localhost:5000/');
        // Select Manual
        await page.select('#playMode', 'manual');
        await page.click('button[onclick="startGame()"]');
        await page.waitForNavigation();
        
        console.log("On play page.");
        await page.waitForTimeout(1000);
        
        console.log("Clicking toggle heatmap...");
        await page.click('button[onclick="window.heatmapAPI.toggle()"]');
        await page.waitForTimeout(1000);
        
        // Check cell (1, 1) innerText
        const cellText = await page.evaluate(() => {
            const cell = document.getElementById('cell-1-1');
            return cell ? cell.innerText : 'CELL NOT FOUND';
        });
        console.log("Cell (1,1) text:", cellText);
        
        await browser.close();
    } catch (err) {
        console.error(err);
        process.exit(1);
    }
})();
