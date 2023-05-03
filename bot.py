import telebot

inventory = [
    {'item': 'toothpaste', 'price(Rs.)': 199, 'quantity': 100000, 'weight': 500},
    {'item': 'toothbrush', 'price(Rs.)': 50, 'quantity': 1000, 'weight': 500},
    {'item': 'salt', 'price(Rs.)': 100, 'quantity': 100000, 'weight': 500},
    {'item': 'turmeric', 'price(Rs.)': 150, 'quantity': 100000, 'weight': 500},
    {'item': 'soap', 'price(Rs.)': 99, 'quantity': 100000, 'weight': 100},
    {'item': 'shampoo', 'price(Rs.)': 299, 'quantity': 500000, 'weight': 500},
    {'item': 'detergent', 'price(Rs.)': 399, 'quantity': 800000, 'weight': 1000},
    {'item': 'honey', 'price(Rs.)': 199, 'quantity': 100000, 'weight': 500},
    {'item': 'sugar', 'price(Rs.)': 49, 'quantity': 500000, 'weight': 500},
    {'item': 'milk', 'price(Rs.)': 149, 'quantity': 700000, 'weight': 500},
    {'item': 'eggs', 'price(Rs.)': 99, 'quantity': 1200000, 'weight': 500},
    {'item': 'bread', 'price(Rs.)': 129, 'quantity': 900000, 'weight': 500},
    {'item': 'butter', 'price(Rs.)': 159, 'quantity': 100000, 'weight': 500},
    {'item': 'cheese', 'price(Rs.)': 299, 'quantity': 100000, 'weight': 500},
    {'item': 'bananas', 'price(Rs.)': 39, 'quantity': 300000, 'weight': 1000},
    {'item': 'apples', 'price(Rs.)': 49, 'quantity': 250000, 'weight': 500}
]

ordered_items = {}
bot = telebot.TeleBot("5874913363:AAHqklZq4yoOCEl1BZROAoVkemhRXQ9zloE")

@bot.message_handler(commands=['start', 'help', 'info', 'status', 'inventory', 'order',])
def handle_command(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, "Hello! Welcome to our general store. Enter /help to view the commands that be given.")
    elif message.text == '/help':
        bot.send_message(message.chat.id, "Commands:\n/start - start the bot\n/help - show this message\n/info - show info about the bot\n/inventory- to view the items in the store\n/order- to order the items from the store\n/status - show the status of the bot")
    elif message.text == '/info':
        bot.send_message(message.chat.id, "This bot helps you to order items from our store.")
    elif message.text == '/status':
        bot.send_message(message.chat.id, "The bot is up and running!")
    elif message.text == '/inventory':
        msg = ""
        for item in inventory:
            msg += f"{item['item']} - Price(Rs.): {item['price(Rs.)']} - Quantity: {item['quantity']} - Weight: {item['weight']}\n"
        bot.send_message(message.chat.id, msg)
        bot.send_message(message.chat.id,"Enter /order to order from inventory.")
    elif message.text == '/order':
        ordered_items.clear()
        bot.send_message(message.chat.id, "Please enter the names and quantities of the items you want to order, separated by commas. For example: Toothpaste 2, Soap 3, Shampoo 1")
        bot.register_next_step_handler(message, get_order_items)

def get_order_items(message):
    ordered_items = {}
    order_items = message.text.split(',')
    total_cost = 0
    ordered = False  # flag to track whether any items are ordered or not

    for order_item in order_items:
        if ' ' in order_item:
            name, quantity_str=order_item.split(' ')
            name=name.lower()
            if quantity_str.isdigit():
                quantity = int(quantity_str)
                for item in inventory:
                    if item['item'] == name:
                        if item['quantity'] >= quantity:
                            ordered_items[item['item']] = {'price(Rs.)': item['price(Rs.)'], 'quantity': quantity}
                            total_cost += item['price(Rs.)'] * quantity
                            item['quantity'] -= quantity
                            ordered = True  # set flag to True
                            break
                        else:
                            bot.send_message(message.chat.id, f"Sorry, we don't have enough {item['item']} in stock. Enter the command /inventory to view available items and quantity.")
                
            else:
                bot.send_message(message.chat.id, f"Invalid quantity format: {quantity_str}")
        else:
            bot.send_message(message.chat.id, f"Invalid input format: {order_item}")

    if ordered:
        msg = ""
        for item in ordered_items:
            msg += f"{item}: {ordered_items[item]['quantity']} x {ordered_items[item]['price(Rs.)']} = {ordered_items[item]['quantity'] * ordered_items[item]['price(Rs.)']:.2f}\n"
        msg += f"Total cost: {total_cost:.2f}"
        bot.send_message(message.chat.id, msg)
        bot.send_message(message.chat.id,"Enter 'yes' if you want to place order otherwise enter 'no'.")
        bot.register_next_step_handler(message, accept_ord)
    else:
        bot.send_message(message.chat.id, "Sorry, your order could not be placed. Enter the command /order to order items.")

def accept_ord(message):
  message.text=message.text.lower()
  if message.text=='yes':
    bot.send_message(message.chat.id, "yay! The order is placed.Send the adress to the store owner to deliver the order or you can collect the items from store.\n /order -> to re-order")
  else:
    bot.send_message(message.chat.id, "To view items in inventory-/inventory.")

bot.polling()