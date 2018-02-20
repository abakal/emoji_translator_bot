# -*- coding: utf-8 -*-
"""
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
import random



allEmojis=json.load(open('emojilib/emojis.json',encoding='utf-8'))
TOKEN=''
SYMBOLS = '!"#$%&\'()*+,-./:;<=>?@[]^_`{|}~'



def getAllEmojiForWord(originalWord):
    word=originalWord.strip().lower()
    
    if not word or word=='' or word=='a' or word =='it' or word=='is':
        return ''
    
    maybeSingular=''
    if len(word)>2 and word[-1]=='s':
        maybeSingular=word[:-1]
    
    maybePlural='' if len(word)==1 else word+'s'
    
    maybeVerbedSimple=''
    maybeVerbedVowel=''
    maybeVerbedDoubled=''
    
    if word.endswith('ing'):
        
        verb=word[0:len(word)-3]
        
        maybeVerbedSimple=verb
        
        maybeVerbedVowel=verb+'e'
        
        maybeVerbedDoubled=verb[0:len(verb)-1]
        
       
        
    useful=[]

    if (word=='i' or word =='you'):
        useful.append('😀')
        useful.append('😃')
    elif (word=='she'):
        useful.append('💁')
    elif (word=='he'):
        useful.append('🤴')
    elif (word=='we' or word=='they'):
        useful.append('👪')
    elif (word=='am' or word=='is' or word=='are'):
        useful.append('👉')
    elif (word=='thanks'):
        useful.append('🙌')
        
        
    for emoji in allEmojis:
        words=allEmojis[emoji].get('keywords')
        if (word ==allEmojis[emoji].get('char') or 
            emoji == word or (emoji==word+'_face') or
            emoji == maybeSingular or emoji == maybePlural or
            emoji == maybeVerbedSimple or emoji == maybeVerbedVowel or emoji == maybeVerbedDoubled or
            (words and words.count(word)>0) or
            (words and words.count(maybeSingular)>0) or 
            (words and words.count(maybePlural)>0) or
            (words and words.count(maybeVerbedSimple)>0) or
            (words and words.count(maybeVerbedVowel)>0) or
            (words and words.count(maybeVerbedDoubled)>0)):
                if (not (len(word)<=3 and allEmojis[emoji].get('category')=='flags')):
                    useful.append(allEmojis[emoji].get('char'))
    return useful

def getEmojiForWord(word):
    translations=getAllEmojiForWord(word)
    if translations:
        return translations[random.randint(0,len(translations)-1)]
    else:
        return word

def translate(sentence,onlyEmoji):
    translation=''
    words=sentence.split()
    for i in range(0,len(words)):
        firstSymbol=''
        lastSymbol=''
        word=words[i]
        
        while (SYMBOLS.find(word[0])!=-1):
            firstSymbol+=word[0]
            word=word[1:len(word)]
        
        while (SYMBOLS.find(word[-1])!=-1):
            lastSymbol+=word[-1]
            word=word[0:len(word)-1]
        
        if onlyEmoji:
            firstSymbol=lastSymbol=''
        
        translated=getEmojiForWord(word)
        if translated:
            translation +=firstSymbol+translated+lastSymbol+' '
        elif not onlyEmoji:
            translation+=firstSymbol+word+lastSymbol+' '
            
    return translation

if len(TOKEN)==0:
	print('Please cpecify TOKEN')
	exit()
	

updater = Updater(TOKEN)

dispatcher = updater.dispatcher


def startCommand(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text='Hello, let translate some words')
    
def helpCommand(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text='''This is Emoji translator, just Enter English sentense or Word:
                                                         Input: Let's eating donuts!
                                                         Output: Let's 🍽 🍩!
                                                         Supported commands:
                                                         /help
                                                         /start							
                                                         ''')    

def textMessage(bot,update):
        response=translate(update.message.text,False)
        bot.send_message(chat_id=update.message.chat_id, text=response)
        
def unknown(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text='This command is unsupported. See /help')

start_handler=CommandHandler('start',startCommand)
help_handler=CommandHandler('help',helpCommand)
text_message_handler=MessageHandler(Filters.text,textMessage)
unknown_handler=MessageHandler(Filters.command, unknown)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling(clean=True)
updater.idle()
