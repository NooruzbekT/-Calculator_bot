import telebot

# Initialize variables to store current and previous values
value = ''
old_value = ''

# Create a bot instance
bot = telebot.TeleBot('API_TOKEN')

# Create an inline keyboard
keyboard = telebot.types.InlineKeyboardMarkup()

# Add buttons to the keyboard
keyboard.row(telebot.types.InlineKeyboardButton('', callback_data='no'),
             telebot.types.InlineKeyboardButton('C', callback_data='C'),
             telebot.types.InlineKeyboardButton('<=', callback_data='<='),
             telebot.types.InlineKeyboardButton('/', callback_data='/'))

keyboard.row(telebot.types.InlineKeyboardButton('7', callback_data='7'),
             telebot.types.InlineKeyboardButton('8', callback_data='8'),
             telebot.types.InlineKeyboardButton('9', callback_data='9'),
             telebot.types.InlineKeyboardButton('*', callback_data='*'))

keyboard.row(telebot.types.InlineKeyboardButton('4', callback_data='4'),
             telebot.types.InlineKeyboardButton('5', callback_data='5'),
             telebot.types.InlineKeyboardButton('6', callback_data='6'),
             telebot.types.InlineKeyboardButton('-', callback_data='-'))

keyboard.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
             telebot.types.InlineKeyboardButton('2', callback_data='2'),
             telebot.types.InlineKeyboardButton('3', callback_data='3'),
             telebot.types.InlineKeyboardButton('+', callback_data='+'))

keyboard.row(telebot.types.InlineKeyboardButton(' ', callback_data='no'),
             telebot.types.InlineKeyboardButton('0', callback_data='0'),
             telebot.types.InlineKeyboardButton('.', callback_data='.'),
             telebot.types.InlineKeyboardButton('=', callback_data='='))


# Handler for the /start command
@bot.message_handler(commands=['start'])
def get_message(message):
    global value
    # If the current value is empty, send '0', otherwise send the current value
    if value == '':
        bot.send_message(message.from_user.id, '0', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)


# Handler for callback queries
@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data

    # Handle button presses
    if data == 'no':
        pass
    elif data == 'C':
        value = ''  # Clear the current value
    elif data == '<=':
        if value != '':
            value = value[:len(value) - 1]  # Remove the last character
    elif data == '=':
        try:
            value = str(eval(value))  # Evaluate the current value
        except ZeroDivisionError:
            value = "Error!"  # Display an error for division by zero
    else:
        value += data  # Append the pressed button to the current value

    # If the current value has changed, update the message
    if (value != old_value and value != '') or ('0' != old_value and value == ''):
        if value == '':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0',
                                  reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value,
                                  reply_markup=keyboard)
            old_value = value  # Update the previous value
    if value == 'Error':  # If the current value is 'Error', reset it
        value = ''


# Start the bot
bot.polling(none_stop=False, interval=0)

