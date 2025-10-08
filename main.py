import logging
import hashlib
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# -------------------------------
#  إعداد Flask علشان Replit يفضل صاحي
# -------------------------------
app = Flask('')


@app.route('/')
def home():
    return "Bot is running!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Example resources
resources = {
    "تحدياتنا ✨": {
        "تحديات يومية": {
            "تحدي اللجنه": "روز اشرحيله تحدي اللجنه",
            "تحدي النقاط": "روز اشرحيله تحدي النقاط",
            "لعبه الحبار": "روز اشرحيله لعبه الحبار",
            "تحدي 1v1": "روز اشرحيله تحدي 1v1",
            "تحدي بطولة": "روز اشرحيله تحدي بطولة",
            "تحدي نقطة الصفر": "روز اشرحيله تحدي نقطة الصفر",
            "تحدي ملك اليوم": "روز اشرحيله تحدي ملك اليوم",
            "تحدي يوم الانجاز الثقيل": "روز اشرحيله تحدي يوم الانجاز الثقيل",
            "تحدي المركز الاول والاخير":
            "روز اشرحيله تحدي المركز الاول والاخير "
        },
        "تحديات شهريه": {
            "تحدي الشهر": "روز اشرحيله تحدي الشهر",
            "معسكر الانجاز": "روز اشرحيله معسكر الانجاز"
        }
    },
    "مصادر ✏️": {
        "تحفيز 🔥": {
            "تحفيز": "تحفيز",
            "تحفيز 1": "تحفيز 1",
            "تحفيز 2": "تحفيز 2",
            "تحفيز 3": "تحفيز 3",
            "تحفيز 4": "تحفيز 4",
            "تحفيز 5": "تحفيز 5",
            "تحفيز 6": "تحفيز 6",
            "تحفيز 7": "تحفيز 7",
            "تحفيز 8": "تحفيز 8",
            "جرعة إصرار": "جرعة إصرار بقا عشان تعبااان"
        },
        "نصائح 🎖": {
            "نصيحة 1": "روز هاتي نصيحة 1",
            "نصيحة 2": "روز هاتي نصيحة 2",
            "نصيحة 3": "روز هاتي نصيحة 3",
            "نصحيه 4": "روز هاتي نصيحة 4",
            "نصيحة 5": "روز هاتي نصيحة 1"
        },
        "Planners 🌟": {
            "monthly study planner": "روز وريه ال monthly study planner",
            "study session planner": "روز وريه ال study session planner",
            "weekly study planner": "روز وريه ال weekly study planner",
            "chapter summary": "روز وريه ال chapter summary",
            "to do list": "روز وريه ال to do list",
            "جدول محاضرات": "روز وريه جدول محاضرات"
        },
        "merve ⚡️": {
            "merve": "عايز يتمزج 😌, روز هتايله  merve",
            "merve 1h": "عايز يتمزج 😌, روز هتايله  merve 1h",
            "merve 1.5h": "عايز يتمزج 😌, روز هتايله  merve 1.5h",
            "merve 2h": "عايز يتمزج 😌, روز هتايله  merve 2h",
            "merve 3h": "عايز يتمزج 😌, روز هتايله  merve 3h"
        },
        "ذكر ✨": {
            "دعاء ١": "روز فين دعاء ١",
            "دعاء ٢": "روز ممكن دعاء ٢",
            "القرآن الكريم": "القرآن الكريم",
            "سورة الملك": "سورة الملك",
            "أذكار": "أذكار يا روز",
            "ذِكر": "ذِكر",
            "أجر": "أجر اجارك الله"
        }
    },
    "اوامر 🔒": {
        "الادمن": "روز فكريني كده مين الادمن",
        "مشاركة شاشة": "مشاركة يا روز",
        "حضروني": "حضروني",
        "كيفية مشاركة الشاشة": "روز عرفيه كيفية مشاركة الشاشة",
        "فكرة القناة": "اشرحيله فكرة القناة يا روز",
        "فكرة القناة بالتفصيل": "روز اشرحيله فكرة القناة بالتفصيل",
        "@القوانين": "عرفيه @القوانين يا روز",
        "كيف أستخدم تطبيق فوريست": "روز اشرحيله كيف أستخدم تطبيق فوريست",
        "*استراحة": "روز وديه *استراحة",
    }
}

CREATOR_ID = 7437663760  # استبدلها بـ ID بتاعك
callback_map = {}  # لتخزين المسارات الآمنة


def encode_path(path: str) -> str:
    """Generate short safe callback data"""
    return hashlib.md5(path.encode("utf-8")).hexdigest()[:10]


def build_menu(data, path=""):
    """Generate buttons dynamically"""
    if not isinstance(data, dict) or not data:
        return None

    buttons = []
    for key, value in data.items():
        if not key.strip():
            continue
        full_path = f"{path}/{key}" if path else key
        hash_key = encode_path(full_path)
        callback_map[hash_key] = full_path
        buttons.append([InlineKeyboardButton(key, callback_data=hash_key)])

    # زر الإضافة
    add_hash = encode_path(f"{path}/add")
    callback_map[add_hash] = f"{path}/add"
    buttons.append(
        [InlineKeyboardButton("➕ أضف مصدر", callback_data=add_hash)])

    # زر الرجوع
    if path:
        parent_path = "/".join(path.split("/")[:-1])
        back_hash = encode_path(parent_path)
        callback_map[back_hash] = parent_path
        buttons.append(
            [InlineKeyboardButton("⬅️ رجوع", callback_data=back_hash)])

    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu"""
    user = update.effective_user
    logger.info("User %s (%s) triggered the bot.", user.username, user.id)
    await update.message.reply_text("اختر قسمًا:",
                                    reply_markup=build_menu(resources))


async def trigger_responses(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    """Trigger bot when user writes 'الردود'"""
    if update.message.text.strip() == "الردود":
        await start(update, context)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    hash_key = query.data
    if hash_key not in callback_map:
        await query.message.edit_text("⚠️ حدث خطأ: المعرف غير معروف.")
        return

    path = callback_map[hash_key]
    keys = path.strip("/").split("/") if path else []
    node = resources

    # Navigate to the desired node
    for k in keys:
        if not k:
            continue
        if k in node:
            node = node[k]
        elif k == "add":
            await query.message.edit_text("📩 أرسل لي المصدر الذي تريد إضافته:")
            context.user_data["awaiting_resource"] = "/".join(keys[:-1])
            logger.info("User %s adding resource under: %s", user.username,
                        "/".join(keys[:-1]))
            return
        else:
            await query.message.edit_text("🚫 مسار غير معروف.")
            return

    # If node is a string
    if isinstance(node, str):
        await query.message.edit_text(node)
        logger.info("User %s viewed message: %s", user.username, node)
        return

    # If node is a dict, show sub-menu on same message
    if isinstance(node, dict):
        menu = build_menu(node, path)
        if menu:
            await query.message.edit_text("اختر:", reply_markup=menu)
        else:
            await query.message.edit_text("🚫 لا يوجد محتوى بعد.")
        return


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if "awaiting_resource" in context.user_data:
        resource_path = context.user_data.pop("awaiting_resource")
        msg = f"📌 طلب مصدر جديد:\n📂 المسار: {resource_path}\n👤 من: {user.username} ({user.id})\n📝 المحتوى:\n{text}"

        await context.bot.send_message(CREATOR_ID, msg)
        await update.message.reply_text("✅ تم إرسال مصدرك إلى المشرف للمراجعة!"
                                        )
        logger.info("User %s suggested new resource for %s", user.username,
                    resource_path)
    else:
        logger.info("User %s sent message (ignored): %s", user.username, text)


def main():
    app = Application.builder().token(
        "8360049562:AAFIs4BH7tmr3VtsLYFKCkYhUW8X29TC0iI").build(
        )  # استبدل بالتوكن بتاعك

    # Trigger bot when user writes "الردود"
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, trigger_responses))

    # Handle resource submissions and other messages
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Handle button clicks
    app.add_handler(CallbackQueryHandler(button))

    logger.info("Bot started successfully 🚀")
    app.run_polling()


if __name__ == "__main__":
    keep_alive()  # يشغل السيرفر الخلفي
    main()  # يشغل البوت
