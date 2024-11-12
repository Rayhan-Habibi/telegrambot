from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = '7229621310:AAGTN0NtL76S0wjrC7J_3J7fwGywIsrTf9Q'


user_data = {}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Hitung zakat", callback_data='hitung_zakat')],
        [InlineKeyboardButton("Informasi tentang zakat", callback_data='informasi_zakat')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Halo! Silahkan pilih layanan yang anda inginkan:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'hitung_zakat':
        keyboard = [
            [InlineKeyboardButton("Zakat Maal", callback_data='zakat_maal')],
            [InlineKeyboardButton("Zakat Fitrah", callback_data='zakat_fitrah')],
            [InlineKeyboardButton("Zakat Perdagangan", callback_data='zakat_peternakan')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Zakat apa yang ingin anda hitung?", reply_markup=reply_markup)

    elif query.data == 'zakat_maal':
        await query.edit_message_text("Masukkan jumlah pemasukan anda dalam satu tahun: Contoh: 20.000.000")
        user_data[query.from_user.id] = {'zakat_type': 'maal'}

    elif query.data == 'zakat_fitrah':
        await query.edit_message_text("Masukkan jumlah anggota keluarga anda: Contoh: 4")
        user_data[query.from_user.id] = {'zakat_type': 'fitrah'}

    elif query.data == 'zakat_peternakan':
        await query.edit_message_text("Masukkan aset usaha anda dalam rupiah: Contoh: 30.000.000")
        user_data[query.from_user.id] = {'zakat_type': 'peternakan'}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

   
    if user_data.get(user_id, {}).get('zakat_type') == 'maal':
        try:
            # Parse user's input to an integer
            input_maal = int(update.message.text.replace(".", "").replace(",", ""))
            user_data[user_id]['input_maal'] = input_maal

            # Calculate Zakat Maal (2.5% of income)
            zakat_maal = input_maal * 0.025
            await update.message.reply_text(f"Jumlah zakat maal yang perlu anda bayar setiap tahunnya sebesar: {zakat_maal}")
        except ValueError:
            await update.message.reply_text("Harap masukkan jumlah pemasukan dalam format angka. Contoh: 20000000")

    if user_data.get(user_id, {}).get('zakat_type') == 'fitrah':
        try:
            # Parse user's input to an integer
            input_fitrah = int(update.message.text.replace(".", "").replace(",", ""))
            user_data[user_id]['input_fitrah'] = input_fitrah

            # Calculate Zakat Maal (2.5% of income)
            zakat_fitrah = input_fitrah * 55000
            await update.message.reply_text(f"Jumlah zakat fitrah yang perlu anda bayar (Sesuai standar SK Baznas) setiap learannya sebesar: {zakat_fitrah} ")
        except ValueError:
            await update.message.reply_text("Harap masukkan jumlah pemasukan dalam format angka. Contoh: 4")
    
    if user_data.get(user_id, {}).get('zakat_type') == 'peternakan':
        try:
            # Parse user's input to an integer
            query = update.callback_query
            input_peternakan = int(update.message.text.replace(".", "").replace(",", ""))
            user_data[user_id]['input_peternakan'] = input_peternakan
            await update.message.reply_text(f"Masukkan hutang jangka pendek usaha anda dalam rupiah: Contoh: 50.000.000")
            user_data[query.from_user.id] = {'zakat_type': 'peternakan2'}

            if user_data.get(user_id, {}).get('zakat_type') == 'peternakan2':
                try: 
                    input_peternakan2 = int(update.message.text.replace(".", "").replace(",", ""))
                    user_data[user_id]['input_peternakan2'] = input_peternakan2
                    zakat_peternakan = 0.025 * (input_peternakan - input_peternakan2)
                    await update.message.reply_text(f"Jumlah zakat perdagangan yang perlu anda bayar adalah sebesar: {zakat_peternakan} ")
                except ValueError: 
                    await update.message.reply_text("Harap masukkan jumlah pemasukan dalam format angka. Contoh: 20000000")
        except ValueError:
            await update.message.reply_text("Harap masukkan jumlah pemasukan dalam format angka. Contoh: 20000000")


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()