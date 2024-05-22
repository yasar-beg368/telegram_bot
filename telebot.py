import logging
from aiogram import Bot , Dispatcher  , types , executor
#from aiogram.utils import executor
from dotenv import load_dotenv
#import google.generativeai as genai
import os
import openai
import sys


class Referance:
    '''A class to store previously response from chatgpt API'''
    def __init__(self) -> None:
        
        self.response=""
load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY")
#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
referance=Referance()
API_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
#model_name
#MODEL_NAME=genai.GenerativeModel('gemini-pro')
MODEL_NAME="gpt-3.5-turbo"

#initialise the bot

bot=Bot(token=API_TOKEN)

dispatcher=Dispatcher(bot)
def clear_past():
    '''A function to clear previous chat'''
    referance.response=""
    
    
@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.message):
    '''This message whith '/start' or '/help' command'''
    await message.reply("Hi\nI am Tele Bot \n created by yasar mirza")
    
    
@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.message):
    '''A handler to clear past chat'''
    await message.reply("I have cleared the past chat")
    
    
@dispatcher.message_handler(commands=['help'])
async def helper(message: types.message):
    '''A handler to display the help menu'''
    help_commands='''
    Hi I am ai bot to help you created by yasar mirza
    /start-to start the chat
    /clear-to clear the past chat
    /help-to get help
    I hope this heips.:)
    '''            
    await message.reply(help_commands)
@dispatcher.message_handler()
async def chatgpt(message: types.message):
    '''A handler to process the user input and generate the response using chatgpt API'''
    print(f">>>USER: \n\t{message.text}")
    response=openai.ChatCompletion.create(
        model=MODEL_NAME,
        message=[
            {"role":"assistant","content":referance.response},
            {"role":"user","content":message.text}
        ]
    )
    referance.response=response.choices[0]['message']['content']
    print(f">>>chatgpt:\n\t{referance.response}")
    await bot.send_message(chat_id=message.chat.id,text=referance.response)
    
if __name__=="__main__":
    executor.start_polling(dispatcher,skip_updates=False)
