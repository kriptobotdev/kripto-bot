import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8931944236:AAGmbl0AdlXTjPqk_0N-3_1rSbmr7Cf3h4Q"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba! Ben Kripto Fiyat Botu.\n"
        "Kullanim: /price bitcoin veya /price ethereum\n"
        "Ornek: /price bitcoin"
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Lutfen coin adi girin. Orn: /price bitcoin")
        return

    coin = context.args[0].upper()
    
    coin_map = {
        "BITCOIN": "BTCUSDT",
        "BTC": "BTCUSDT",
        "ETHEREUM": "ETHUSDT",
        "ETH": "ETHUSDT",
        "DOGECOIN": "DOGEUSDT",
        "DOGE": "DOGEUSDT",
        "SOLANA": "SOLUSDT",
        "SOL": "SOLUSDT"
    }
    
    symbol = coin_map.get(coin, None)
    if not symbol:
        await update.message.reply_text(f"HATA: '{coin}' desteklenmiyor. Desteklenen: bitcoin, ethereum, dogecoin, solana")
        return

    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            await update.message.reply_text("HATA: Fiyat alinamadi.")
            return
        
        data = response.json()
        usd_price = float(data.get("lastPrice", 0))
        change = float(data.get("priceChangePercent", 0))

        emoji = "🟢" if change >= 0 else "🔴"
        coin_name = coin_map.get(coin, coin)
        await update.message.reply_text(
            f"💰 {coin_name.replace('USDT','')}\n${usd_price:,.2f}\n{emoji} 24s: %{change:.2f}"
        )
    except:
        await update.message.reply_text("Fiyat alinamadi, tekrar dene.")

async def yardim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Komutlar:\n"
        "/start - Botu baslat\n"
        "/price <coin> - Canli fiyat gor\n"
        "/yardim - Bu mesaji goster\n\n"
        "Desteklenen: bitcoin, ethereum, dogecoin, solana"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("yardim", yardim))
    print("Bot calisiyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
