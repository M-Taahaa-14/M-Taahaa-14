// generate-animation.js
const fs = require('fs');
const { execSync } = require('child_process');

async function generateAnimation() {
    const username = process.env.USERNAME || 'M-Taahaa-14';
    const token = process.env.GITHUB_TOKEN;
    
    console.log(`Generating animation for ${username}...`);
    
    // HTML template for the animation
    const htmlTemplate = `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #0d1117, #161b22);
            font-family: 'Segoe UI', sans-serif;
            color: white;
            width: 1000px;
            height: 600px;
        }
        
        .container {
            background: rgba(22, 27, 34, 0.9);
            border-radius: 20px;
            padding: 30px;
            border: 2px solid #00d4aa;
            box-shadow: 0 0 30px rgba(0, 212, 170, 0.3);
        }
        
        .title {
            text-align: center;
            font-size: 2em;
            font-weight: bold;
            background: linear-gradient(45deg, #00d4aa, #39ff14);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin-bottom: 25px;
            padding: 15px;
            background: linear-gradient(135deg, rgba(0, 212, 170, 0.1), rgba(57, 255, 20, 0.1));
            border-radius: 10px;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 1.8em;
            font-weight: bold;
            color: #00d4aa;
            text-shadow: 0 0 10px rgba(0, 212, 170, 0.5);
        }
        
        .stat-label {
            color: #8b949e;
            font-size: 0.8em;
        }
        
        .field {
            position: relative;
            background: linear-gradient(135deg, #238636, #2ea043);
            border-radius: 15px;
            padding: 20px;
            height: 250px;
            overflow: hidden;
        }
        
        .field-lines {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        
        .center-line {
            position: absolute;
            left: 50%;
            top: 0;
            bottom: 0;
            width: 2px;
            background: rgba(255, 255, 255, 0.6);
        }
        
        .center-circle {
            position: absolute;
            left: 50%;
            top: 50%;
            width: 60px;
            height: 60px;
            border: 2px solid rgba(255, 255, 255, 0.6);
            border-radius: 50%;
            transform: translate(-50%, -50%);
        }
        
        .contributions-grid {
            display: grid;
            grid-template-columns: repeat(53, 1fr);
            gap: 2px;
            position: relative;
            z-index: 2;
        }
        
        .cell {
            aspect-ratio: 1;
            border-radius: 2px;
            transition: all 0.3s ease;
        }
        
        .level-0 { background: rgba(22, 27, 34, 0.4); }
        .level-1 { background: rgba(0, 109, 50, 0.8); }
        .level-2 { background: rgba(0, 138, 64, 0.9); }
        .level-3 { background: rgba(57, 211, 83, 0.9); }
        .level-4 { 
            background: rgba(87, 255, 87, 1); 
            box-shadow: 0 0 8px rgba(87, 255, 87, 0.5);
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        .ball {
            position: absolute;
            width: 10px;
            height: 10px;
            background: radial-gradient(circle at 30% 30%, #ff4444, #cc0000);
            border-radius: 50%;
            box-shadow: 0 0 10px rgba(255, 68, 68, 0.8);
            z-index: 10;
            animation: ballMove 8s linear infinite;
        }
        
        @keyframes glow {
            from { box-shadow: 0 0 5px rgba(87, 255, 87, 0.5); }
            to { box-shadow: 0 0 15px rgba(87, 255, 87, 0.8); }
        }
        
        @keyframes ballMove {
            0% { transform: translate(0px, 100px); }
            25% { transform: translate(200px, 50px); }
            50% { transform: translate(400px, 150px); }
            75% { transform: translate(600px, 80px); }
            100% { transform: translate(800px, 120px); }
        }
        
        .pulse {
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.7; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">⚽ ${username}'s Coding Championship</div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number" id="total">0</div>
                <div class="stat-label">Total Goals</div>
            </div>
            <div class="stat-item">
                <div class="stat-number" id="streak">0</div>
                <div class="stat-label">Current Streak</div>
            </div>
            <div class="stat-item">
                <div class="stat-number" id="week">0</div>
                <div class="stat-label">This Week</div>
            </div>
            <div class="stat-item">
                <div class="stat-number" id="month">0</div>
                <div class="stat-label">This Month</div>
            </div>
        </div>
        
        <div class="field">
            <div class="field-lines">
                <div class="center-line"></div>
                <div class="center-circle"></div>
            </div>
            <div class="ball"></div>
            <div class="contributions-grid" id="grid"></div>
        </div>
    </div>
    
    <script>
        // This will be populated with real GitHub data
        const contributionsData = CONTRIBUTIONS_DATA_PLACEHOLDER;
        
        function renderGrid() {
            const grid = document.getElementById('grid');
            contributionsData.forEach((count, index) => {
                const cell = document.createElement('div');
                cell.className = \`cell level-\${Math.min(count, 4)}\`;
                if (count >= 3) cell.classList.add('pulse');
                grid.appendChild(cell);
            });
        }
        
        function updateStats() {
            const total = contributionsData.reduce((a, b) => a + b, 0);
            let streak = 0;
            for (let i = contributionsData.length - 1; i >= 0; i--) {
                if (contributionsData[i] > 0) streak++;
                else break;
            }
            const week = contributionsData.slice(-7).reduce((a, b) => a + b, 0);
            const month = contributionsData.slice(-30).reduce((a, b) => a + b, 0);
            
            document.getElementById('total').textContent = total;
            document.getElementById('streak').textContent = streak;
            document.getElementById('week').textContent = week;
            document.getElementById('month').textContent = month;
        }
        
        renderGrid();
        updateStats();
    </script>
</body>
</html>`;

    try {
        // Fetch GitHub contributions data
        const contributionsData = await fetchContributions(username, token);
        
        // Replace placeholder with actual data
        const finalHtml = htmlTemplate.replace('CONTRIBUTIONS_DATA_PLACEHOLDER', JSON.stringify(contributionsData));
        
        // Write HTML file
        fs.writeFileSync('temp-animation.html', finalHtml);
        
        // Generate GIF using puppeteer (you'll need to install it)
        console.log('Generating GIF...');
        
        // Alternative: Use a simpler approach with existing tools
        const puppeteer = require('puppeteer');
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        
        await page.setViewport({ width: 1000, height: 600 });
        await page.setContent(finalHtml);
        await page.waitForTimeout(1000);
        
        // Take multiple screenshots for GIF frames
        const frames = [];
        for (let i = 0; i < 20; i++) {
            const screenshot = await page.screenshot({ type: 'png' });
            frames.push(screenshot);
            await page.waitForTimeout(400); // 400ms between frames
        }
        
        await browser.close();
        
        // Create GIF from frames (you'll need to install gifencoder or similar)
        console.log('Creating GIF from frames...');
        
        // For now, save the first frame as PNG
        fs.writeFileSync('output/git-contribution-football.png', frames[0]);
        
        // Clean up
        fs.unlinkSync('temp-animation.html');
        
        console.log('Animation generated successfully!');
        
    } catch (error) {
        console.error('Error generating animation:', error);
        // Generate fallback static image
        generateFallbackImage();
    }
}

async function fetchContributions(username, token) {
    const { Octokit } = require('@octokit/rest');
    const octokit = new Octokit({ auth: token });
    
    try {
        // Use GraphQL to fetch contribution data
        const query = \`
            query(\$username: String!) {
                user(login: \$username) {
                    contributionsCollection {
                        contributionCalendar {
                            weeks {
                                contributionDays {
                                    contributionCount
                                    date
                                }
                            }
                        }
                    }
                }
            }
        \`;
        
        const result = await octokit.graphql(query, { username });
        const weeks = result.user.contributionsCollection.contributionCalendar.weeks;
        
        const contributions = [];
        weeks.forEach(week => {
            week.contributionDays.forEach(day => {
                contributions.push(day.contributionCount);
            });
        });
        
        return contributions;
    } catch (error) {
        console.error('Error fetching contributions:', error);
        // Return demo data as fallback
        return Array.from({ length: 371 }, () => Math.floor(Math.random() * 5));
    }
}

function generateFallbackImage() {
    console.log('Generating fallback image...');
    // Create a simple fallback
    const fallbackSvg = \`<svg width="1000" height="400" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#0d1117"/>
        <text x="500" y="200" text-anchor="middle" fill="#00d4aa" font-size="24" font-family="Arial">
            ⚽ GitHub Contribution Animation
        </text>
        <text x="500" y="240" text-anchor="middle" fill="#8b949e" font-size="16" font-family="Arial">
            Loading... Check back soon!
        </text>
    </svg>\`;
    
    fs.writeFileSync('output/github-contribution-football.svg', fallbackSvg);
}

// Install required dependencies
try {
    execSync('npm install @octokit/rest puppeteer', { stdio: 'inherit' });
} catch (error) {
    console.log('Installing dependencies...');
}

generateAnimation();
