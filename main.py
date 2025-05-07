import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Bot configuration
API_TOKEN = '7703506774:AAErrMjaBHZ7rMBevQOgHyRSdTbHtR8vAD4'
CHANNEL_ID = '@fwbindonesia77'
COOLDOWN_MINUTES = 10

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import time

# Track last message time for each user
user_last_message = {}

# Simpan data user yang sudah verifikasi
verified_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    
    # Send the FWB logo first
    with open('attached_assets/CD62E361-9455-4F7F-B113-9D5695FFAABF.png', 'rb') as photo:
        await update.message.reply_photo(photo=photo)
    
    keyboard = [
        [InlineKeyboardButton("✨ Subscribe Channel", url=f"https://t.me/fwbindonesia77")],
        [InlineKeyboardButton("✅ Sudah Subscribe", callback_data='check_subscription')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('🔥 Silakan subscribe channel terlebih dahulu untuk melanjutkan:', reply_markup=reply_markup)

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = update.callback_query.from_user.id
        chat_member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        
        if chat_member.status in ['member', 'administrator', 'creator']:
            keyboard = [
                [InlineKeyboardButton("Menu", callback_data='menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.edit_message_text('✅ Terima kasih sudah subscribe!\nSilakan gunakan menu:', reply_markup=reply_markup)
        else:
            keyboard = [
                [InlineKeyboardButton("✨ Subscribe Channel", url=f"https://t.me/fwbindonesia77")],
                [InlineKeyboardButton("✅ Sudah Subscribe", callback_data='check_subscription')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.edit_message_text('❌ Kamu belum subscribe channel! Silakan subscribe terlebih dahulu:', reply_markup=reply_markup)
    except Exception as e:
        print(f"Error in check_subscription: {e}")
        await update.callback_query.edit_message_text('Terjadi kesalahan. Silakan coba lagi.')

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.callback_query.from_user.id
    warning_text = (
        "⚠️ *WARNING!*\n\n"
        "Bot ini bukan tempat untuk ajakan seks, konten 18+, prostitusi, atau tindakan melanggar hukum lainnya. "
        "Dilarang keras mengirimkan menfess yang berisi:\n"
        "• Ajakan kencan dengan tujuan seksual\n"
        "• Deskripsi atau gambar eksplisit\n"
        "• Kata-kata yang mengarah pada aktivitas seksual\n"
        "• Permintaan atau tawaran layanan seksual\n"
        "• Link menuju situs pornografi atau ilegal\n\n"
        "Jika ditemukan pelanggaran, akun kamu akan langsung diblokir dan di-ban permanen dari sistem kami tanpa peringatan.\n\n"
        "Kami ingin menciptakan ruang yang aman, santai, dan menyenangkan untuk semua pengguna. "
        "Hormati privasi, batasan, dan kenyamanan orang lain.\n\n"
        "Terima kasih atas kerja samanya!\n"
        "• Admin Bot FWB\n\n"
        "--------------------\n"
        "*Pilih menu berikut:*"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔞 Kirim Menfess", callback_data='select_gender')],
        [InlineKeyboardButton("↩️ Kembali", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(warning_text, reply_markup=reply_markup, parse_mode='Markdown')
    

async def select_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("👱‍♀️ Cewek", callback_data='menfess_F'),
            InlineKeyboardButton("👱‍♂️ Cowok", callback_data='menfess_M')
        ],
        [InlineKeyboardButton("↩️ Kembali", callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text('🔍 Pilih gendermu:', reply_markup=reply_markup)

async def menfess(update: Update, context: ContextTypes.DEFAULT_TYPE, gender: str) -> None:
    user_id = update.callback_query.from_user.id
    context.user_data['gender'] = gender
    await update.callback_query.edit_message_text('🔥 Silakan kirim menfessmu yang hot! 🥵')

async def receive_menfess(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    current_time = time.time()
    
    # Check cooldown
    if user_id in user_last_message:
        time_diff = current_time - user_last_message[user_id]
        remaining_time = COOLDOWN_MINUTES * 60 - time_diff
        
        if remaining_time > 0:
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            warning = (
                f"⚠️ *PERINGATAN COOLDOWN*\n\n"
                f"Anda harus menunggu *{minutes} menit {seconds} detik* lagi\n"
                f"sebelum dapat mengirim menfess berikutnya!\n\n"
                f"Mohon hormati waktu cooldown untuk mencegah spam."
            )
            await update.message.reply_text(warning, parse_mode='Markdown')
            return
    
    if 'gender' not in context.user_data:
        await update.message.reply_text(
            "⚠️ Silakan pilih gender terlebih dahulu melalui menu utama!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Menu", callback_data='menu')]])
        )
        return

    gender = context.user_data.get('gender', 'M')  # Default to M if not set
    gender_emoji = "👱‍♀️" if gender == "F" else "👱‍♂️"
    
    if update.message.photo:
        # Handle photo with caption
        photo = update.message.photo[-1]
        caption = update.message.caption or ""
        formatted_text = f"_{caption}\n\n{gender_emoji} [{gender}] #fwb #sender #hmu 🔥_"
        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo.file_id,
            caption=formatted_text,
            parse_mode='Markdown'
        )
    elif update.message.text:
        # Handle text-only message
        formatted_text = f"_{update.message.text}\n\n{gender_emoji} [{gender}] #fwb #sender #hmu 🔥_"
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=formatted_text,
            parse_mode='Markdown'
        )
    # Update last message timestamp
    user_last_message[user_id] = time.time()
    await update.message.reply_text('Menfessmu sudah terkirim! ⏳ Tunggu 10 menit untuk mengirim menfess berikutnya.')
    

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Menu", callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text('Halo! Saya bot FWB Indonesia. Tekan tombol di bawah untuk melanjutkan:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'menu':
        await menu(update, context)
    elif query.data == 'select_gender':
        await select_gender(update, context)
    elif query.data.startswith('menfess_'):
        gender = query.data.split('_')[1]  # Get F or M
        await menfess(update, context, gender)
    elif query.data == 'check_subscription':
        await check_subscription(update, context)
    elif query.data == 'back':
        await back(update, context)

def main() -> None:
    try:
        # Build application
        application = Application.builder().token(API_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))
        application.add_handler(MessageHandler((filters.TEXT | filters.PHOTO) & ~filters.COMMAND, receive_menfess))

        # Run the bot with cleanup
        print("Bot starting...")
        application.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False, drop_pending_updates=True)

    except Exception as e:
        print(f"Error: {e}")
        if 'application' in locals():
            asyncio.run(application.shutdown())

if __name__ == '__main__':
    main()
