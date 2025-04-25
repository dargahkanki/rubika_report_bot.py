import telebot
from telebot import types

TOKEN = '7149620305:AAEnrmL8sCWh6Ubj1EJxi1uvU0DeAoiZiuA'
OWNER_ID = 6748490013  

bot = telebot.TeleBot(TOKEN)

rubika_session = {}

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id != OWNER_ID:
        bot.reply_to(message, "شما دسترسی به این ربات ندارید.")
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("ورود به روبیکا", callback_data="login")
    btn2 = types.InlineKeyboardButton("ارسال گزارش", callback_data="report")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "به پنل گزارش‌زن روبیکا خوش آمدید!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.message.chat.id != OWNER_ID:
        return

    if call.data == "login":
        msg = bot.send_message(call.message.chat.id, "شماره روبیکای خود را وارد کنید:")
        bot.register_next_step_handler(msg, ask_code)
    
    elif call.data == "report":
        msg = bot.send_message(call.message.chat.id, "آیدی روبیکای هدف را ارسال کنید:")
        bot.register_next_step_handler(msg, choose_report_type)

def ask_code(message):
    number = message.text
    rubika_session['number'] = number
    bot.send_message(message.chat.id, f"کد تایید برای {number} ارسال شد. لطفاً کد را وارد کنید:")
    bot.register_next_step_handler(message, finish_login)

def finish_login(message):
    code = message.text
    rubika_session['logged_in'] = True
    bot.send_message(message.chat.id, "ورود موفقیت‌آمیز بود.")

def choose_report_type(message):
    rubika_session['target'] = message.text
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("مستهجن", callback_data="type_obscene"),
        types.InlineKeyboardButton("هرزنامه", callback_data="type_spam"),
        types.InlineKeyboardButton("جعلی", callback_data="type_fake"),
        types.InlineKeyboardButton("تهدید", callback_data="type_threat")
    )
    bot.send_message(message.chat.id, "نوع گزارش را انتخاب کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("type_"))
def report_type_selected(call):
    report_type = call.data.split("_")[1]
    target = rubika_session.get('target', None)
    if not target:
        bot.send_message(call.message.chat.id, "خطا! آیدی هدف مشخص نیست.")
        return

    for i in range(5):
        bot.send_message(call.message.chat.id, f"{i+1}. گزارش نوع {report_type} برای {target} ارسال شد.")
    bot.send_message(call.message.chat.id, "گزارش‌ها ارسال شدند (شبیه‌سازی).")

bot.infinity_polling()
