from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

# Создаем класс Todo и миксины
class Todo:
    def __init__(self, description):
        self.description = description

class CreateMixin:
    def create_task(self, description):
        task = Todo(description)
        self.tasks.append(task)
        return task

class ReadMixin:
    def read_task(self, index):
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        else:
            return None

class UpdateMixin:
    def update_task(self, index, new_description):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            task.description = new_description
            return task
        else:
            return None

class DeleteMixin:
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            task = self.tasks.pop(index)
            return task
        else:
            return None

class TodoList(CreateMixin, ReadMixin, UpdateMixin, DeleteMixin):
    def __init__(self):
        self.tasks = []

# Создаем экземпляр TodoList
todo_list = TodoList()

# Функция-обработчик команды /start
def start(update, context):
    reply_text = "Привет! Я телеграм-бот для работы с задачами. Введите /help для получения списка команд."
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

# Функция-обработчик команды /help
def help(update, context):
    reply_text = "Доступные команды:\n\n"\
                 "/create - Создать задачу\n"\
                 "/read <индекс> - Прочитать задачу по индексу\n"\
                 "/update <индекс> <новое_описание> - Обновить задачу по индексу\n"\
                 "/delete <индекс> - Удалить задачу по индексу\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

# Функция-обработчик команды /create
def create_task(update, context):
    task_description = ' '.join(context.args)
    task = todo_list.create_task(task_description)
    reply_text = f"Создана задача: {task.description}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

# Функция-обработчик команды /read
def read_task(update, context):
    index = int(context.args[0])
    task = todo_list.read_task(index)
    if task:
        reply_text = f"Задача {index}: {task.description}"
    else:
        reply_text = f"Задача {index} не найдена"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

# Функция-обработчик команды /update
def update_task(update, context):
    index = int(context.args[0])
    new_description = ' '.join(context.args[1:])
    task = todo_list.update_task(index, new_description)
    if task:
        reply_text = f"Обновлена задача {index}: {task.description}"
    else:
        reply_text = f"Задача {index} не найдена"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

# Функция-обработчик команды /delete
def delete_task(update, context):
    index = int(context.args[0])
    task = todo_list.delete_task(index)
    if task:
        reply_text = f"Удалена задача {index}: {task.description}"
    else:
        reply_text = f"Задача {index} не найдена"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

# Функция-обработчик текстовых сообщений
def handle_message(update, context):
    text = update.message.text
    reply_text = "Неизвестная команда. Введите /help для получения списка команд."
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

# Создаем экземпляр Updater и регистрируем обработчики
updater = Updater(token='6241813520:AAEmnzYETEKwHVwITA-eMZVY5Widzlx-dJo', use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('create', create_task))
dispatcher.add_handler(CommandHandler('read', read_task))
dispatcher.add_handler(CommandHandler('update', update_task))
dispatcher.add_handler(CommandHandler('delete', delete_task))
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# Запускаем бота
updater.start_polling()
updater.idle()
