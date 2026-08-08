const { JSDOM } = require('jsdom');
const fs = require('fs');

async function run() {
    console.log("Loading play.html with jsdom...");
    const html = fs.readFileSync('templates/play.html', 'utf8');
    
    // We need to mock fetch
    const dom = new JSDOM(html, {
        url: "http://localhost/",
        runScripts: "dangerously",
        resources: "usable",
        beforeParse(window) {
            window.fetch = async (url, options) => {
                console.log(`FETCH: ${url}`);
                if (url === '/api/state') {
                    return {
                        json: async () => ({
                            env: {
                                size: 4,
                                score: 0,
                                agent_pos: [0,0],
                                agent_dir: 0,
                                agent_alive: true,
                                agent_escaped: false,
                                grid: []
                            },
                            agent: { play_mode: 'autoplay' }
                        })
                    };
                }
                if (url === '/api/step') {
                    return {
                        json: async () => ({
                            status: 'success',
                            decision: { reason: "Search", action: "FORWARD", explanation: "explaining", confidence: 1 },
                            score: 0
                        })
                    };
                }
            };
            
            // Mock gsap
            window.gsap = {
                fromTo: () => {},
                to: () => {},
                from: () => {},
                set: () => {},
                timeline: () => ({
                    to: function() { return this; },
                    call: function(cb) { cb(); return this; }
                })
            };
            
            // Pass errors to console
            window.addEventListener("error", (event) => {
                console.error("JSDOM ERROR:", event.error);
            });
            window.addEventListener("unhandledrejection", (event) => {
                console.error("JSDOM UNHANDLED REJECTION:", event.reason);
            });
        }
    });

    // Load scripts
    const loadScript = (path) => {
        const code = fs.readFileSync(path, 'utf8');
        const script = dom.window.document.createElement('script');
        script.textContent = code;
        dom.window.document.body.appendChild(script);
    };
    
    loadScript('static/js/board.js');
    loadScript('static/js/reasoning.js');
    loadScript('static/js/heatmap.js');
    loadScript('static/js/agent.js');
    loadScript('static/js/autoplay.js');

    await new Promise(resolve => setTimeout(resolve, 100)); // wait for init
    
    console.log("Calling gameAPI.fetchState()...");
    dom.window.gameAPI.fetchState();
    
    await new Promise(resolve => setTimeout(resolve, 100));
    
    console.log("Clicking autoplay toggle()...");
    dom.window.autoplayAPI.toggle();
    
    await new Promise(resolve => setTimeout(resolve, 3100));
    console.log("Done.");
}

run().catch(console.error);
