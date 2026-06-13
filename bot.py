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

    # Yeni API endpoint'i
    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}?quotes=USD"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            await update.message.reply_text(f"HATA: '{coin}' bulunamadi veya API hatasi.")
            return
        
        data = response.json()
        usd_price = data.get("quotes", {}).get("USD", {}).get("price", None)
        change = data.get("quotes", {}).get("USD", {}).get("percent_change_24h", 0)

        if usd_price is None:
            await update.message.reply_text(f"HATA: '{coin}' bulunamadi.")
            return

        emoji = "🟢" if change >= 0 else "🔴"

        await update.message.reply_text(
            f"💰 *{coin_id.upper()}*\n${usd_price:,.2f}\n{emoji} 24s: %{change:.2f}",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"Fiyat alinamadi: {str(e)[:50]}")
