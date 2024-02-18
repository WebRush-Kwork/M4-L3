from telebot import TeleBot
from logic import *
from config import *
import telebot

bot = TeleBot(bot_token)
task_manager = TaskManager(database)


@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот-менеджер задач. Помогу тебе сохранить твои задачи!) 
    /add_task - используй для добавления новой задачи
    /delete_task - используй для удаления задачи""")


@bot.message_handler(commands=["add_task"])
def add_task(message):
    bot.send_message(message.chat.id, "Введите название задачи")
    bot.register_next_step_handler(message, add_description)


@bot.message_handler(commands=["add_description"])
def add_description(message):
    name = message.text
    bot.send_message(message.chat.id, "Введите описание задачи")
    bot.register_next_step_handler(message, save_task, name=name)


def save_task(message, name):
    description = message.text
    user_id = message.chat.id
    task_manager.add_task(user_id, name, description)
    bot.send_message(message.chat.id, "Задача добавлена")


@bot.message_handler(commands=["delete_task"])
def delete_task(message):
    bot.send_message(
        message.chat.id, "Введите имя задачи, которую хотите удалить:")
    bot.register_next_step_handler(message, delete_task_by_id)


def delete_task_by_id(message):
    task_name = message.text
    task_manager.delete_task(task_name)
    bot.send_message(message.chat.id, "Задача удалена")


@bot.message_handler(commands=["show_task"])
def show_task(message):
    count = telebot.util.extract_arguments(message.text)
    user_id = message.chat.id
    try:
        count = int(count)
        tasks = task_manager.select_task(user_id, count)
    except:
        tasks = task_manager.select_task(user_id)
    tasks = "\n".join([x[0] for x in tasks])
    bot.send_message(message.chat.id, tasks)


bot.infinity_polling()
