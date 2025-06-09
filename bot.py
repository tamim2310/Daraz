from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from daraz_scraper import get_daraz_price
from database import init_db, add_tracking, get_all_tracking
import asyncio

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Daraz Price Tracker Bot!\nUse /track <Daraz link> <target_price> to track a product.")

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usage: /track <Daraz link> <target_price>")
        return

    url = context.args[0]
    try:
        target_price = float(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Target price must be a number.")
        return

    user_id = update.effective_user.id
    add_tracking(user_id, url, target_price)
    await update.message.reply_text(f"✅ Tracking started for:\n{url}\nTarget Price: ৳{target_price}")

async def price_checker(application):
    while True:
        print("🔁 Checking prices...")
        for user_id, url, target_price in get_all_tracking():
            current_price = get_daraz_price(url)
            if current_price is not None and current_price <= target_price:
                try:
                    await application.bot.send_message(
                        chat_id=user_id,
                        text=f"🔥 Price dropped!\n{url}\nCurrent Price: ৳{current_price}\nTarget: ৳{target_price}"
                    )
                except:
                    pass
        await asyncio.sleep(3600)  # Check every 1 hour

if __name__ == "__main__":
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("track", track))

    app.post_init = lambda app: asyncio.create_task(price_checker(app))
    app.run_polling()
