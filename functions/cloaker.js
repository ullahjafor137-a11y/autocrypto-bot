// CLOAKER PRO - USA ONLY - v2.0
exports.handler = async (event) => {
    const headers = event.headers;
    const ua = headers['user-agent'] || '';
    
    // 1. LISTA DIAL L-BOTS (FB, Google, etc.)
    const bots = ['FacebookExternalHit', 'facebot', 'Googlebot', 'bingbot', 'bot', 'adidxbot', 'Twitterbot'];
    
    if (bots.some(b => ua.includes(b))) {
        // === 🛡️ SAFE PAGE (L-Gharbal) ===
        // Hada hwa li ghadi i-chouf l-Robot dial Facebook
        return {
            statusCode: 200,
            headers: {'Content-Type': 'text/html'},
            body: `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AutoCrypto Platform - Maintenance</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 100px; color: #333; }
        h1 { color: #2c3e50; }
    </style>
</head>
<body>
    <h1>System Maintenance</h1>
    <p>Our trading infrastructure is currently undergoing scheduled upgrades.</p>
    <p>We will be live shortly. Thank you for your patience.</p>
    <p>© 2026 AutoCrypto LLC - Secure Trading Solutions</p>
</body>
</html>`
        };
    }

    // === 💸 MONEY PAGE (Human Traders) ===
    // Hada hwa li ghadi i-chouf bnadem li dkhel mn l-Ads
    return {
        statusCode: 200,
        headers: {'Content-Type': 'text/html'},
        body: `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoCrypto - Ex-Binance AI Trading Bot</title>
    
    <script>
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
    document,'script','https://connect.facebook.net/en_US/fbevents.js');
    
    fbq('init', '751015047199999'); // <--- ⚠️ BEDDEL HADA B PIXEL ID DYALK
    fbq('track', 'PageView');
    </script>
    <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=751015047199999&ev=PageView&noscript=1"/></noscript>

    <style>
        body { background: #0b0e11; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; }
        .hero { height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
        .btn { background: #f0b90b; color: black; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 1.2rem; }
        .status { color: #00ff00; font-size: 0.9rem; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="hero">
        <h1>🚀 AUTOCRYPTO AI PRO</h1>
        <p>Join 15,000+ Traders using our Ex-Binance AI Node.</p>
        <p style="color: #f0b90b; font-size: 1.5rem;">+2.5% DAILY ROI</p>
        <br>
        <a href="https://t.me/AutoCrypto_Lab_Bot" class="btn">START AI TRADING NOW</a>
        <div class="status">● System Status: Optimal</div>
    </div>
</body>
</html>`
    };
};
