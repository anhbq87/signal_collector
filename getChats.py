import time

from pyrogram import Client
from pyrogram.api import functions, types
from pyrogram.api.errors import FloodWait
import codecs, xlwt, datetime

client = None

target = "me"  # "me" refers to your own chat (Saved Messages)
history = []  # List that will contain all the messages of the target chat
limit = 100  # Amount of messages to retrieve for each API call
#offset = 0  # Offset starts at 0
except_ids = []

def get_histories(channel):
    refined_history = []
    offset = 0
    filename = "D:\\QuangAnh\\workspace\\" + str(channel.id) + ".xls"
    if (channel.id != 1145864382  ):
        return
    print(filename)
    while True:
        try:
            messages = client.send(
                functions.messages.GetHistory(
                    client.resolve_peer(channel.id),
                    0, 0, offset, limit, 0, 0, 0
                )
        )
        except FloodWait as e:
            # For very large chats the method call can raise a FloodWait
            time.sleep(e.x)  # Sleep X seconds before continuing
            continue
    
        if not messages.messages:
            break  # No more messages left
    
        history.extend(messages.messages)
        offset += limit
        #print(messages.messages, file = codecs.open(filename, 'a', "utf-8"))
        #print(messages.messages, file = open(filename, 'a'))
    for msg in history:
        #print(msg, file = codecs.open(filename, 'a', "utf-8"))
        if isinstance(msg, types.Message) and "BUY" in msg.message:
            refined_history.append(msg)
    output(filename, "sheet", refined_history)
    
def retrieve_all_chats():
    while True:
        try:
            messages = client.send(
                functions.messages.GetAllChats(except_ids
                )
            )
        except FloodWait as e:
            # For very large chats the method call can raise a FloodWait
            time.sleep(e.x)  # Sleep X seconds before continuing
            continue
    
        if not messages:
            break  # No more messages left
        
        print("abc")
        print(type(messages))
        if isinstance(messages, types.messages.Chats):
            print(messages, file = open("D:\QuangAnh\workspace\chats.txt", 'w'))
            chats = messages.chats
            for chat in chats:
                if isinstance(chat, types.Channel):
                    #print(chat.id, "\t", chat.title, file = codecs.open("D:\QuangAnh\workspace\channel.rtf", 'a', "utf-8"))
                    get_histories(chat)
            break
        
def output(filename, sheet, history):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)
    
    #write header
    sh.write(0, 0, "ID")
    sh.write(0, 1, "Datetime")
    sh.write(0, 2, "Message")
    for n, item in enumerate(history, 1):
        sh.write(n, 0, item.id)
        sh.write(n, 1, datetime.datetime.fromtimestamp(item.date).strftime("%Y-%m-%d %H:%M:%S"))
        sh.write(n, 2, item.message)
    

    book.save(filename)
    
def main():
    global client
    client = Client(
            session_name="QATestApp",
            api_key=(68606, "4cf5577a0b8a95656af4e9df5820150d")
            )
    
    #client.set_update_handler(update_handler)

    client.start()
        
    retrieve_all_chats()

    client.stop()
if __name__ == "__main__":
    main()
    

