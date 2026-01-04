import json, os, time, random, asyncio, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# === 🛠️ CONFIGURATION ===
TOKEN = '8441128784:AAEBQKVR8cD0-_Jg2Sela_JwfVE8As6q9Q4'
ADMIN_ID = 7510150471 
CHANNEL_ID = "@AutoCrypto_Lab"
WEBSITE = "https://autocrypto.online"
USDT_ADDRESS = "Txxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Beddel hada!

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

# === ⚙️ AUTO-ROI TASK (Every 24 Hours) ===
async def auto_roi_task(context: ContextTypes.DEFAULT_TYPE):
    d = db(); changed = False; now = time.time()
    for uid, usr in d.items():
        if usr['pack'] != 'none' and usr['invested'] > 0:
            # Check if 24h passed
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
                    await context.bot.send_message(chat_id=uid, text=msg, parse_mode='HTML')
                except: pass
    if changed: save_db(d)

# === 🚀 HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user; get_user(u.id)
    txt = (
        "🔥 <b>THE SYSTEM IS AWAKE...</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Welcome, Agent <b>{u.first_name}</b>. You have successfully bypassed the firewall. "
        "The global financial grid is now under your control via decentralized AI.\n\n"
        "📜 <b>OFFICIAL AGENT CERTIFICATE:</b>\n"
        "┌────────────────────\n"
        f"│ 🆔 <b>ID:</b> <code>ACL-PRO-{u.id}</code>\n"
        "│ 🛡️ <b>AUTH:</b> <code>VERIFIED</code>\n"
        "└────────────────────\n\n"
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
        f"💎 <b>NET AI PROFITS:</b> <code>${usr['roi']:,.2f}</code>\n"
        f"👥 <b>NETWORK:</b> <code>{usr['refs']} Agents</code>\n\n"
        f"📡 <b>STATUS:</b> 🟢 <code>OPTIMAL OPERATIONAL</code>"
    )
    kb = [
        [InlineKeyboardButton("⚡ INVEST", callback_data='packs'), InlineKeyboardButton("📊 STATS", callback_data='stats')],
        [InlineKeyboardButton("📜 LICENSE", callback_data='license'), InlineKeyboardButton("🧠 AI TEST", callback_data='ai_0')],
        [InlineKeyboardButton("💹 MARKET", callback_data='market'), InlineKeyboardButton("🎁 BONUS", callback_data='bonus')],
        [InlineKeyboardButton("👥 PARTNERS", callback_data='ref'), InlineKeyboardButton("🏆 LEADER", callback_data='leader')],
        [InlineKeyboardButton("💸 WITHDRAW", callback_data='withdraw'), InlineKeyboardButton("👨‍💻 SUPPORT", callback_data='support_ask')],
        [InlineKeyboardButton("🌐 WEBSITE", url=WEBSITE), InlineKeyboardButton("🔄 REFRESH", callback_data='dashboard')]
    ]
    if int(uid) == ADMIN_ID:
        kb.append([InlineKeyboardButton("📢 BC", callback_data='admin_bc'), InlineKeyboardButton("🔥 PUMP", callback_data='admin_pump')])
    
    if q: await q.message.edit_text(txt, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')
    else: await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')

# === 📩 MEDIA & BUTTONS LOGIC ===
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; data = q.data; uid = str(q.from_user.id); usr = get_user(uid)
    await q.answer()

    if data == 'dashboard':
        await dashboard(update, context)

    elif data == 'packs':
        txt = "⚡ <b>NODES</b>\nSelect a node to begin algorithm allocation:"
        kb = [[InlineKeyboardButton(f"✅ ACTIVATE {v['c']}", callback_data=f'pay_{k}')] for k,v in VIP.items()]
        kb.append([InlineKeyboardButton("🏠 BACK", callback_data='dashboard')])
        await q.message.edit_text(txt, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')

    elif data.startswith('pay_'):
        pk = data.split('_')[1]; price = VIP[pk]['p']
        d = db(); d[uid]['state'] = 'waiting_screenshot'; d[uid]['pending_pack'] = pk; save_db(d)
        await q.message.edit_text(f"📥 <b>DEPOSIT</b>\nAmount: <b>${price} USDT</b>\nNetwork: <b>TRC-20</b>\n\n<code>{USDT_ADDRESS}</code>\n\n📸 Send screenshot below:", parse_mode='HTML')

    elif data.startswith('adm_app_') and int(uid) == ADMIN_ID:
        _, _, t_uid, pk = data.split('_')
        d = db(); d[t_uid]['invested'] += VIP[pk]['p']; d[t_uid]['pack'] = pk; d[t_uid]['last_roi'] = time.time(); save_db(d)
        await context.bot.send_message(t_uid, f"✅ <b>NODE {VIP[pk]['c']} ACTIVATED!</b>")
        await q.message.edit_caption(caption="✅ Approved.")

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user; uid = str(u.id); usr = get_user(uid)
    if usr.get('state') == 'waiting_screenshot' and update.message.photo:
        pk = usr['pending_pack']
        await context.bot.send_photo(ADMIN_ID, update.message.photo[-1].file_id, 
            caption=f"🔔 <b>DEPOSIT PROOF</b>\nUID: {uid}\nPack: {pk}", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ APPROVE", callback_data=f"adm_app_{uid}_{pk}")]]) )
        d = db(); d[uid]['state'] = 'idle'; save_db(d)
        await update.message.reply_text("⏳ <b>Submitted!</b> Verification in progress.")

# === 🏁 RUN BOT ===
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # This is the JobQueue part that needs "pip install python-telegram-bot[job-queue]"
    if app.job_queue:
        app.job_queue.run_repeating(auto_roi_task, interval=3600, first=10)
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.PHOTO | filters.TEXT, handle_media))
    
    print("🚀 v91.0 SUPREME READY FOR KOYEB!"); app.run_polling()
