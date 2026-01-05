// CLOAKER PRO - USA ONLY
exports.handler = async (event) => {
  const headers = event.headers;
  const ua = headers['user-agent'] || '';
  const ip = headers['cf-connecting-ip']  headers['x-forwarded-for']  '';
  
  // FB/MOD BOTS = SAFE
  const bots = ['FacebookExternalHit', 'facebot', 'Googlebot', 'bingbot', 'bot'];
  if (bots.some(b => ua.includes(b))) {
    return {
      statusCode: 200,
      headers: {'Content-Type': 'text/html'},
      body: `
<!DOCTYPE html>
<html>
<head><title>AutoCrypto Trading</title></head>
<body style="text-align:center;padding:50px">
<h1>AutoCrypto Platform</h1>
<p>Scheduled maintenance. Available soon in your region.</p>
<p>© 2026 AutoCrypto LLC</p>
</body>
</html>`
    };
  }
  
  // HUMAN USA/EU = FULL LANDING + PIXEL
  return {
    statusCode: 200,
    headers: {'Content-Type': 'text/html'},
    body: <!-- TON INDEX.HTML COMPLET HNA -->
  };
};
