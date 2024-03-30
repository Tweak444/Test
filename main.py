import telebot
from telebot import types

# Initialize the bot with the provided token
bot_token = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(bot_token)

# Handler for the '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Send the updated welcome message in Russian
    welcome_text = '''Привет!😃 
Мы рады приветствовать вас в Pride cargo! 
На данный момент вам требуется зарегистрироваться, нажмите пожалуйста кнопку регистрации'''
    bot.send_message(message.chat.id, welcome_text)
    
    # Create the markup with buttons
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    register_button = types.KeyboardButton('Register')
    contact_info_button = types.KeyboardButton('Contact Info')
    markup.add(register_button, contact_info_button)
    
    # Send the message with buttons
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)

# Handler for the 'Register' button
@bot.message_handler(func=lambda message: message.text == 'Register')
def ask_for_name(message):
    msg = bot.send_message(message.chat.id, "Please enter your name:")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        user_name = message.text
        msg = bot.send_message(message.chat.id, "Please share your contact.", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_contact_step, user_name)
    except Exception as e:
        bot.reply_to(message, 'Oops! Something went wrong.')

def process_contact_step(message, user_name):
    try:
        user_contact = message.contact.phone_number if message.contact else None
        if user_contact:
            msg = bot.send_message(message.chat.id, "Please enter your Ai address in Pinduoduo:")
            bot.register_next_step_handler(msg, process_ai_address_step, user_name, user_contact)
        else:
            msg = bot.send_message(message.chat.id, "Please use the 'Share Contact' button to share your contact.")
            bot.register_next_step_handler(msg, process_contact_step, user_name)
    except Exception as e:
        bot.reply_to(message, 'Oops! Something went wrong.')

def process_ai_address_step(message, user_name, user_contact):
    try:
        user_ai_address = message.text
        # Write the user's information into 'register.txt'
        with open('register.txt', 'a') as file:
            file.write(f"Name: {user_name}, Contact: {user_contact}, Ai Address: {user_ai_address}\n")
        bot.send_message(message.chat.id, "Thank you for registering!")
    except Exception as e:
        bot.reply_to(message, 'Oops! Something went wrong.')

# Handler for the 'Contact Info' button
@bot.message_handler(func=lambda message: message.text == 'Contact Info')
def contact_info(message):
    bot.send_message(message.chat.id, "You can contact us at [email protected]")

# Enable 'Share Contact' button
@bot.message_handler(content_types=['contact'])
def contact(message):
    process_contact_step(message, message.from_user.first_name)

# Polling
bot.polling(none_stop=True)