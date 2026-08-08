const puppeteer = require('puppeteer');

(async () => {
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        
        // Setup console intercept
        page.on('console', msg => console.log('PAGE LOG:', msg.text()));
        page.on('pageerror', error => console.log('PAGE ERROR:', error.message));
        page.on('requestfailed', request => console.log('REQUEST FAILED:', request.url(), request.failure().errorText));
        
        console.log("Navigating to setup...");
        await page.goto('http://localhost:5000/');
        
        // Wait for setup card to be visible (or click Got it)
        try {
            await page.evaluate(() => {
                const btn = document.querySelector('.rules-card.setup-card button');
                if (btn) btn.click();
            });
            await page.waitForTimeout(500);
        } catch (e) {}

        // Select Hybrid Agent
        console.log("Starting game...");
        await page.evaluate(() => {
            document.getElementById('playMode').value = 'autoplay';
            document.getElementById('algorithm').value = 'AStar';
            startGame();
        });
        
        // Wait for navigation to /play
        await page.waitForNavigation();
        console.log("On play screen. Waiting 1s...");
        await page.waitForTimeout(1000);
        
        console.log("Clicking Autoplay...");
        await page.evaluate(() => {
            const btn = document.getElementById('autoplayBtn');
            if (btn) btn.click();
        });
        
        // Monitor requests to /api/step for 10 seconds
        let stepCount = 0;
        page.on('request', req => {
            if (req.url().includes('/api/step')) {
                stepCount++;
                console.log(`[Network] POST /api/step (Count: ${stepCount})`);
            }
        });
        page.on('response', async res => {
            if (res.url().includes('/api/step')) {
                const json = await res.json().catch(e => null);
                if (json) {
                    console.log(`[Network] Response /api/step -> Status: ${json.status}`);
                    if (json.decision) {
                         console.log(`          -> Reason: ${json.decision.reason}`);
                    }
                }
            }
        });
        
        await page.waitForTimeout(10000);
        
        console.log(`Total steps requested: ${stepCount}`);
        
        await browser.close();
    } catch (e) {
        console.error(e);
    }
})();
