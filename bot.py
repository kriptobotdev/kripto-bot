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
        "bitcoin": "btc-bitcoin",
        "btc": "btc-bitcoin",
        "ethereum": "eth-ethereum",
        "eth": "eth-ethereum",
        "dogecoin": "doge-dogecoin",
        "doge": "doge-dogecoin",
        "solana": "sol-solana",
        "sol": "sol-solana"
    }

    coin_id = coin_id_map.get(coin, coin)

    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"

    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            await update.message.reply_text(f"HATA: '{coin}' bulunamadi.")
            return

        data = response.json()
        usd_price = data.get("quotes", {}).get("USD", {}).get("price", None)
        change = data.get("quotes", {}).get("USD", {}).get("percent_change_24h", 0)

        if usd_price is None:
            await update.message.reply_text(f"HATA: '{coin}' bulunamadi.")
            return

        emoji = "🟢" if change >= 0 else "🔴"
        await update.message.reply_text(
            f"💰 {coin.upper()}\n${usd_price:,.2f}\n{emoji} 24s: %{change:.2f}"
        )
    except:
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

if __name__ == "__main__":
    main()
