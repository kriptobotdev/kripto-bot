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

    coin = context.args[0].lower()
    coin_id_map = {
        "bitcoin": "bitcoin",
        "btc": "bitcoin",
        "ethereum": "ethereum",
        "eth": "ethereum",
        "dogecoin": "dogecoin",
        "doge": "dogecoin",
        "solana": "solana",
        "sol": "solana"
    }

    coin_id = coin_id_map.get(coin, coin)

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if coin_id not in data:
            await update.message.reply_text(f"HATA: '{coin}' bulunamadi.")
            return

        price_data = data[coin_id]
        usd_price = price_data.get("usd", "?")
        change = price_data.get("usd_24h_change", 0)

        emoji = "YESIL" if change >= 0 else "KIRMIZI"

        await update.message.reply_text(
            f"{coin_id.upper()} Fiyati:\n\n"
            f"${usd_price:,.2f} USD\n"
            f"{emoji} 24s Degisim: %{change:.2f}"
        )
    except Exception as e:
        await update.message.reply_text("Fiyat alinamadi, tekrar dene.")

async def yardim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Komutlar:\n"
        "/start - Botu baslat\n"
        "/price <coin> - Canli fiyat gor\n"
        "/yardim - Bu mesaji goster"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("yardim", yardim))

    print("Bot calisiyor...")
    app.run_polling()

if _name_ == "_main_":
    main()
