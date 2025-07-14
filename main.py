from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    ConversationHandler, filters
)

# States
BRAND_NAME, PERSONALITY, MOVIE, CUSTOMER_AGE, CUSTOMER_PURPOSE, SLOGAN, PACKAGE_CHOICE = range(7)

# In-memory user data
user_data = {}

# --- Package Selection Logic ---
def suggest_package(profile):
    personality = profile['personality']
    movie = profile['movie']
    age = profile['audience_age']
    purpose = profile['audience_purpose']

    # ترکیب‌های دقیق‌تر با منطق چندشرطی
    if personality == "راهنما" and purpose == "فروش محصول":
        return {
            "theme": "راه‌اندازی حرفه‌ای",
            "colors": ["1A1A40", "FF6F61"],
            "tone": "قاطع و مطمئن",
            "caption": "اعتماد بساز، محصولت رو معرفی کن.",
            "content": "مطالعات موردی، نظرات، ویدیو معرفی"
        }

    elif personality == "دوست صمیمی" and purpose == "روزمرگی/سرگرمی":
        return {
            "theme": "حال‌وهوای خودمونی",
            "colors": ["FFD700", "FF8C00"],
            "tone": "گرم و قابل‌ارتباط",
            "caption": "مثل یه دوست حرف بزن، نه یه برند.",
            "content": "میم‌ها، نظرسنجی‌ها، استوری‌های سریع"
        }

    elif personality == "خریدار محصول" and purpose == "فروش محصول":
        return {
            "theme": "قانع‌سازی منطقی",
            "colors": ["2D3748", "81E6D9"],
            "tone": "مستقیم و قابل‌اعتماد",
            "caption": "چرا این محصول بهترین انتخابه؟",
            "content": "قبل/بعد، نظرات مشتری، تست واقعی"
        }

    elif personality == "عاقل" and purpose == "آموزش" and movie == "مستند":
        return {
            "theme": "یادگیری عمیق",
            "colors": ["003366", "B0C4DE"],
            "tone": "تحلیلی و آرام",
            "caption": "دانش با روایت بهتر جذب می‌شه.",
            "content": "تحلیل، کپشن بلند، نمودار"
        }

    elif personality == "عاقل" and purpose == "آموزش":
        return {
            "theme": "شفافیت و اعتماد",
            "colors": ["003366", "ECECEC"],
            "tone": "آموزنده و آرام",
            "caption": "هر پست یک گام به سمت درک بهتر.",
            "content": "پست‌های اسلایدی، اینفوگرافیک، ویدیوهای آموزشی"
        }

    elif personality == "هنرمند" and movie == "فانتزی" and age == "18–34":
        return {
            "theme": "جوان و خلاق",
            "colors": ["E0BBE4", "957DAD"],
            "tone": "تخیلی و تصویری",
            "caption": "خلاقیتت رو نمایش بده، با رنگ و روایت.",
            "content": "استوری تصویری، ریل مفهومی، بورد رنگی"
        }

    elif personality == "هنرمند" and movie == "فانتزی":
        return {
            "theme": "زیبایی خیال‌انگیز",
            "colors": ["E0BBE4", "957DAD"],
            "tone": "خلاق و زیبا",
            "caption": "یه داستان تصویری بساز که فراموش نشه.",
            "content": "مجموعه عکس‌ها، استوری‌های تصویری، ریل‌های مفهومی"
        }

    elif personality == "بامزه" and movie == "کمدی" and purpose == "پرسونال برندینگ":
        return {
            "theme": "خنده و ارتباط",
            "colors": ["FF6F61", "00CED1"],
            "tone": "طنزآمیز و خودمونی",
            "caption": "با خنده خاطره بساز.",
            "content": "ویدیو فان، پشت صحنه، کپشن فان"
        }

    elif personality == "بامزه" and movie == "کمدی":
        return {
            "theme": "بخند و ارتباط بساز",
            "colors": ["FF6F61", "00CED1"],
            "tone": "بامزه و انسانی",
            "caption": "اگه بخندونیشون، یادت می‌مونه.",
            "content": "پشت‌صحنه‌ها، میم‌ها، سلفی‌های خودمونی"
        }

    # حالت پیش‌فرض
    return {
        "theme": "حضور معنادار",
        "colors": ["A3CEF1", "FDE68A"],
        "tone": "ملایم و هوشمند",
        "caption": "هر حضور دیجیتال باید حرفی برای گفتن داشته باشه.",
        "content": "پست ترکیبی، کپشن قصه‌دار، استوری معرفی، نکات روزمره"
    }


# --- Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌱 سلام! به رنگدانه خوش اومدی 🌈\n"
        "ما بهت کمک می‌کنیم که برندت رو از یه ایده ساده به یه داستان جذاب تبدیل کنی.\n"
        "بیا شروع کنیم!\n\nاسم برندت چیه؟"
    )
    return BRAND_NAME

async def brand_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    brand = update.message.text.strip()
    user_data[update.effective_user.id] = {'brand_name': brand}

    reply_markup = ReplyKeyboardMarkup(
        [["دوست صمیمی", "راهنما", "هنرمند"], ["عاقل","خریدار محصول","بامزه"]], one_time_keyboard=True
    )
    await update.message.reply_text(
        f"اگه {brand} یه آدم بود، چه جور شخصیتی داشت؟",
        reply_markup=reply_markup
    )
    return PERSONALITY

async def personality(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]['personality'] = update.message.text
    brand = user_data[update.effective_user.id]['brand_name']

    reply_markup = ReplyKeyboardMarkup(
        [["درام", "اکشن", "کمدی"], ["فانتزی", "ماجراجویی", "مستند"]], one_time_keyboard=True
    )
    await update.message.reply_text(
        f"چه نوع فیلمی بیشترین شباهت رو به {brand} داره؟",
        reply_markup=reply_markup
    )
    return MOVIE

async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]['movie'] = update.message.text
    await update.message.reply_text("👍 عالی! حالا بریم سراغ بخش مخاطبت.")

    reply_markup = ReplyKeyboardMarkup(
        [["زیر 18 سال", "18–34"], ["35-50", "50+"]], one_time_keyboard=True
    )
    await update.message.reply_text("محدوده سنی مخاطب هدفت چقدره؟", reply_markup=reply_markup)
    return CUSTOMER_AGE

async def customer_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]['audience_age'] = update.message.text
    brand = user_data[update.effective_user.id]['brand_name']

    reply_markup = ReplyKeyboardMarkup(
        [["فروش محصول", "پرسونال برندینگ"], ["آموزش", "روزمرگی/سرگرمی"]], one_time_keyboard=True
    )
    await update.message.reply_text(
        f"چرا {brand} برای این مخاطب‌ها محتوا تولید می‌کنه؟",
        reply_markup=reply_markup
    )
    return CUSTOMER_PURPOSE

async def customer_purpose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]['audience_purpose'] = update.message.text
    brand = user_data[update.effective_user.id]['brand_name']
    await update.message.reply_text(f"شعار یا مأموریت {brand} چیه؟")
    return SLOGAN

async def slogan_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    profile = user_data[update.effective_user.id]
    profile['slogan'] = update.message.text

    package = suggest_package(profile)
    profile['package'] = package
    brand = profile['brand_name']

    await update.message.reply_text(
        f"🎁 بر اساس اطلاعاتی که دادی درباره {brand}، ما پکیج {package['theme']} رو پیشنهاد می‌دیم!\n\n"
        f"🎨 رنگ‌ها: {', '.join(package['colors'])}\n"
        f"🗣 لحن محتوا: {package['tone']}\n"
        f"✍️ سبک کپشن: {package['caption']}\n"
        f"📱 پیشنهاد محتوایی: {package['content']}\n\n"
        "دوست داری یه نمونه رایگان دریافت کنی یا با تیم ما برای یه پکیج اختصاصی صحبت کنی؟",
        reply_markup=ReplyKeyboardMarkup(
            [["نمونه رایگان", "پکیج داستان‌سرایی اختصاصی"]], one_time_keyboard=True
        )
    )
    return PACKAGE_CHOICE

async def package_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    if choice == "نمونه رایگان":
        await update.message.reply_text(
            "🎉 اینم لینک دریافت نمونه رایگان :\n"
            "👉 https://rangdaneh.com/sample-pack"
        )
    else:
        await update.message.reply_text(
            "✨ تیم ما آماده‌ست تا یه داستان اختصاصی برای برندت طراحی کنه!\n"
            "از اینجا با ما در تماس باش: https://rangdaneh.com/contact"
        )
    await update.message.reply_text("مرسی که از رنگدانه استفاده کردی 🌱🌈\nبرای شروع دوباره دستور /start رو بزن.")
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "این بات بهت کمک می‌کنه شخصیت برندت رو کشف کنی و یه پکیج محتوایی مناسب پیشنهاد بده.\n"
        "برای شروع دستور /start رو بزن."
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مکالمه لغو شد. برای شروع دوباره /start رو بزن.")
    return ConversationHandler.END

# --- Main Bot Runner ---
def main():
    import time
    from telegram.error import TimedOut

    while True:
        try:
            app = ApplicationBuilder().token("7642720505:AAGThFlehN2xhZngOHTYyUAp1EPt15i628U").build()

            conv_handler = ConversationHandler(
                entry_points=[CommandHandler("start", start)],
                states={
                    BRAND_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, brand_name)],
                    PERSONALITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, personality)],
                    MOVIE: [MessageHandler(filters.TEXT & ~filters.COMMAND, movie)],
                    CUSTOMER_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, customer_age)],
                    CUSTOMER_PURPOSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, customer_purpose)],
                    SLOGAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, slogan_handler)],
                    PACKAGE_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, package_choice)],
                },
                fallbacks=[CommandHandler("cancel", cancel)],
            )

            app.add_handler(conv_handler)
            app.add_handler(CommandHandler("help", help_command))

            print("Bot polling started...")
            app.run_polling()
        except TimedOut:
            print("⏱️ Timeout occurred, retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print("❌ Unexpected error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
