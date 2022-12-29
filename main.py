from flask import Flask, request, render_template
from datetime import datetime
from os import path
import json
app = Flask(__name__)

# формат файла: {"messages" : messages_list}
MESSAGES_FILE = "messages.json"

def load_messages():
    if not path.isfile(MESSAGES_FILE):
        print(f"Can't find file {MESSAGES_FILE}")
        return []

    with open(MESSAGES_FILE, "r") as mess_file:
        json_data = json.load(mess_file)
        return json_data["messages"]

messages_list = load_messages()

def save_messages():
    with open(MESSAGES_FILE, "w") as mess_file:
        json_data = {
            "messages": messages_list
        }
        json.dump(json_data, mess_file)

# Функция для добавления новых сообщений (имя отправителя, текст сообщений) в список
def add_message(name, text):
    global messages_list
    new_message = {
        "name": name,
        "text": text,
        "time": datetime.now().strftime('%H:%M'),  # ДЗ: Подставить текущее время Часы:Минуты
    }
    messages_list.append(new_message)
    if len(messages_list) == 100  :
        messages_list = messages_list[-100:]
    save_messages()



@app.route("/")
def hello():
    return "Hello, welcome to PythonMessenger2000"


# 1. Display all chat messages: JSON
@app.route("/get_messages")
def get_messages():
    return {"messages": messages_list}


# 2. Ability to sent new messages
# HTTP GET
# http://127.0.0.1:5000/send_message?name=Mike&text=Hello
@app.route("/send_message")
def send_message():
    name = request.args.get("name")
    text = request.args.get("text")

    if 3 > len(name) or len(name) > 100:
        return {"result": False, "error": "Invalid Name"}
    if 1 > len(text) or len(text) > 3000:
        return {"result": False, "error": "Invalid text"}

    add_message(name, text)
    return "OK"

@app.route('/info')
def info_page():
    return f"Total message in chat:{len(messages_list)}"

# 3. UI for messenger
@app.route("/chat")
def display_chat():
    return render_template("chat.html")


app.run()
