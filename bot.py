import json, os, time, random, asyncio, logging, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# === 🌐 FAKE WEB SERVER (By-pass Koyeb Port Check) ===
def run_web_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"ACL SERVER STATUS: OPTIMAL")
    
    # Koyeb requires port 8000 for "Web Service" health checks
    server = HTTPServer(('0.0.0.0', 8000), Handler)
    print("🌐 Fake Web Server started on port 8000")
    server.serve_forever()

# === 🛠️ CONFIGURATION ===
TOKEN = '8441128784:AAEBQKVR8cD0-_Jg2Sela_JwfVE8As6q9Q4'
ADMIN_ID = 7510150471  # Fixed: removed space
CHANNEL_ID = "@AutoCrypto_Lab"
WEBSITE = "https://autocrypto.online"
USDT_ADDRESS = "Txxxxxxxxxxxxxxxxxxxxxxxxxxxx" 

VIP = {
    'bronze': {'p': 100, 'c': '✨ BRONZE NODE', 'r': 0.015, 'e': '🪙'},
    'silver': {'p': 300, 'c': '🥈 SILVER NODE', 'r': 0.020, 'e': '🥈'},
    'gold': {'p': 700, 'c': '👑 GOLD NODE', 'r': 0.025, 'e': '👑'}
}

# === 📂 DATABASE ===
DB_FILE = 'users.json'
def db():
    if not os.path.exists(DB_FILE): save_db({})
    try:
        with open(DB_FILE,'r') as f: return json.load(f).get('users', {})
    except: return {}

def save_db(d):
    try:
        with open(DB_FILE,'w') as f: json.dump({'users': d}, f, indent=4)
    except: pass

def get_user(uid):
    uid = str(uid); d = db()
    if uid not in d:
        d[uid] = {'balance': 0, 'invested': 0, 'roi': 0, 'pack': 'none', 'refs': 0, 'state': 'idle', 'pending_pack': 'none', 'last_roi': time.time(), 'wd_wallet': ''}
        save_db(d)
    return d[uid]

# === ⚙️ AUTO-ROI TASK ===
async def auto_roi_task(context: ContextTypes.DEFAULT_TYPE):
    d = db(); changed = False; now = time.time()
    for uid, usr in d.items():
        if usr['pack'] != 'none' and usr['invested'] > 0:
            if now - usr.get('last_roi', 0) >= 86400:
                rate = VIP[usr['pack']]['r']
                profit = usr['invested'] * rate
                d[uid]['balance'] += profit
                d[uid]['roi'] += profit
                d[uid]['last_roi'] = now
                changed = True
                try:
                    msg = (f"💰 <b>AI PROFIT DISTRIBUTION</b>\n{'═'*30}\n"
                           f"Node: <b>{VIP[usr['pack']]['c']}</b>\n"
                           f"Daily Profit: <code>+${profit:,.2f}</code>\n"
                           f"Status: 🟢 <b>Credited to Balance</b>")
                    await context.bot.send_message(chat_id=int(uid), text=msg, parse_mode='HTML')
                except: pass
    if changed: save_db(d)

# === 🚀 HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user; get_user(u.id)
    txt = (
        "🔥 <b>THE SYSTEM IS AWAKE...</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Welcome, Agent <b>{u.first_name}</b>.\n"
        "Your AI infrastructure is now live and ready.\n\n"
        "<i>'Wealth is not worked for, it is engineered.'</i>"
    )
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🖥️ ACCESS COMMAND CENTER", callback_data='dashboard')]])
    await update.message.reply_text(txt, reply_markup=kb, parse_mode='HTML')

async def dashboard(update, context):
    q = update.callback_query; uid = str(q.from_user.id if q else update.effective_user.id)
    usr = get_user(uid); p = VIP.get(usr['pack'], {'e': '➖', 'c': 'INACTIVE'})
    txt = (
        f"⚡ <b>AI COMMAND CENTER</b> ⚡\n{'═'*35}\n\n"
        f"💰 <b>TOTAL BALANCE:</b> <code>${usr['balance']:,.2f}</code>\n"
        f"📈 <b>ACTIVE NODE:</b> <code>{p['e']} {p['c']}</code>\n"
        f"💎 <b>NET AI PROFITS:</b> <code>${usr['roi']:,.2f}</code>\n\n"
        f"📡 <b>STATUS:</b> 🟢 <code>OPTIMAL</code>"
    )
    kb = [
        [InlineKeyboardButton("⚡ INVEST", callback_data='packs'), InlineKeyboardButton("📊 STATS", callback_data='stats')],
        [InlineKeyboardButton("💸 WITHDRAW", callback_data='withdraw'), InlineKeyboardButton("🔄 REFRESH", callback_data='dashboard')]
    ]
    if q: await q.message.edit_text(txt, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')
    else: await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; data = q.data; uid = str(q.from_user.id)
    await q.answer()
    if data == 'dashboard': await dashboard(update, context)
    elif data == 'packs':
        kb = [[InlineKeyboardButton(f"✅ ACTIVATE {v['c']}", callback_data=f'pay_{k}')] for k,v in VIP.items()]
        kb.append([InlineKeyboardButton("🏠 BACK", callback_data='dashboard')])
        await q.message.edit_text("⚡ <b>SELECT NODE:</b>", reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')

# === 🏁 RUN BOT ===
if __name__ == '__main__':
    # Start fake web server thread
    threading.Thread(target=run_web_server, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # ROI Task every hour
    if app.job_queue:
        app.job_queue.run_repeating(auto_roi_task, interval=3600, first=10)
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    
    print("🚀 v91.2 SUPREME BYPASS READY!"); app.run_polling()
