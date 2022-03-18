# -*- coding: utf-8 -*-
import json
import telebot
from telebot import types
import requests
import bs4
from fake_useragent import UserAgent

TOKEN = "5243606006:AAGK-Dm7Wq-gMqdR00Rv5o5V4r-s-O0KlKY"
bot = telebot.TeleBot(TOKEN)
Language = "ru"

#######################################################################################################################
# Парсим данные сериалов NETFLIX  с сайта YOUFLIX
all = []
listok = ['comedy','horror','popular','best','animation','action','detective','drama','historical','crime','melodrama','teen','superhero','thriller','fantasy','science-fiction','usa','spain','germany','canada','great-britain']
ua = UserAgent()
for i in listok:
    reg = requests.get(f'https://youflix.ru/shows-categories/{i}/', headers={'user-agent': f'{ua.random}'})
    soup = bs4.BeautifulSoup(reg.content, 'html.parser')
    section = soup.select('article.page')
    for names in section:
        namess = names.select('p')
        genres = names.select_one('header.entry-header')
        for name in namess:
            if name.select_one('strong') not in name:
                continue
            name = name.select_one('strong')
            print(genres.get_text().strip())
            print(name.get_text())
            all.append({
                'genre': genres.get_text().strip(),
                'film': name.get_text(),
            })
with open('info.json', 'w', encoding='utf-8') as f:
    json.dump(all, f, indent=4, ensure_ascii=False)



##############################################################################
#начальная клава
@bot.message_handler(content_types=["text"])
def snd_msg(message):
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    #Кнопка
    print('******************************************')
    print(message.from_user.first_name+' '+message.from_user.last_name+' |id:'+str(message.from_user.id))
    print('******************************************')
    first_button = types.InlineKeyboardButton(text="Выбрать жанр", callback_data="genres")
    second_button = types.InlineKeyboardButton(text = "Помощь",callback_data = 'help')
    keyboardmain.add(first_button,second_button)
    bot.send_message(message.chat.id,f"{message.from_user.first_name}, с помощь меня ты можешь найти любой сериал от NETFLIX, который тебе придётся по вкусу", reply_markup=keyboardmain)
#обработка клавы
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    global all
    #результат ккнопки 'назад' - главное меню
    if call.data == "mainmenu":
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        first_button = types.InlineKeyboardButton(text="Выбрать жанр", callback_data="genres")
        second_button = types.InlineKeyboardButton(text="Помощь", callback_data='help')
        keyboardmain.add(first_button, second_button)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=f"{call.from_user.first_name}, с помощь меня ты можешь найти любой сериал от NETFLIX, который тебе придётся по вкусу",reply_markup=keyboardmain)
    elif call.data =='help':
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text='Назад',callback_data='mainmenu')
        keyboardmain.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Данный бот предлагает вам найти любой сериал NETFLIX по вкусу и жанру. Навигация: Нажмите кнопку Выбрать жанр>>Нажмите на кнопку нужного жанра>>Выбирайте. В случае необходимости вы всегда можете обновить список сериалов.",reply_markup=keyboardmain)
    elif call.data == "genres":
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        first_button = types.InlineKeyboardButton(text="Популярно на Netflix", callback_data="popular")
        top50_button = types.InlineKeyboardButton(text="Топ-50 по рейтингу", callback_data="top")
        keyboardmain.add(first_button,top50_button)
        animate_button = types.InlineKeyboardButton(text="Анимации", callback_data="animate")
        action_button = types.InlineKeyboardButton(text="Боевики", callback_data="action")
        keyboardmain.add(animate_button,action_button)
        detective_button = types.InlineKeyboardButton(text="Детеквиное", callback_data="detective")
        dram_button = types.InlineKeyboardButton(text="Драмы", callback_data="dram")
        keyboardmain.add(detective_button,dram_button)
        history_button = types.InlineKeyboardButton(text="Исторические", callback_data="historical")
        comedy_button = types.InlineKeyboardButton(text="Комедии", callback_data="comedy")
        keyboardmain.add(history_button,comedy_button)
        crime_button = types.InlineKeyboardButton(text="Криминал", callback_data="crime")
        melodram_button = types.InlineKeyboardButton(text="Мелодрама", callback_data="melodram")
        keyboardmain.add(crime_button,melodram_button)
        teen_button = types.InlineKeyboardButton(text="Подростковые", callback_data="teen")
        super_button = types.InlineKeyboardButton(text="Супергеройские", callback_data="super")
        keyboardmain.add(teen_button,super_button)
        triller_button = types.InlineKeyboardButton(text="Триллеры", callback_data="triller")
        horror_button = types.InlineKeyboardButton(text="Ужасы", callback_data="horror")
        keyboardmain.add(triller_button,horror_button)
        fantastic_button = types.InlineKeyboardButton(text="Фантастика", callback_data="fantastic")
        fantasy_button = types.InlineKeyboardButton(text="Фэнтази", callback_data="fantasy")
        keyboardmain.add(fantastic_button,fantasy_button)
        usa_button = types.InlineKeyboardButton(text="США", callback_data="usa")
        britain_button = types.InlineKeyboardButton(text="Великобритания", callback_data="britain")
        keyboardmain.add(usa_button,britain_button)
        canada_button = types.InlineKeyboardButton(text="Канада", callback_data="canada")
        spain_button = types.InlineKeyboardButton(text="Испания", callback_data="spain")
        keyboardmain.add(canada_button,spain_button)
        germany_button = types.InlineKeyboardButton(text="Германия", callback_data="germany")
        update_button = types.InlineKeyboardButton(text="Обновить данные", callback_data="update")
        personal_button = types.InlineKeyboardButton(text='Подобрать список специально для вас', callback_data = 'personal')
        keyboardmain.add(germany_button)
        keyboardmain.add(update_button)
        keyboardmain.add(personal_button)

        back_button = types.InlineKeyboardButton(text = "НАЗАД", callback_data='mainmenu')
        keyboardmain.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Выберите одну из категорий, чтобы получить список сериалов которые точно стоит посмотреть",reply_markup=keyboardmain)


    elif call.data == "popular":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Список популярных сериалов Netflix':
                print(info['film'])
                text+=f"{i}.{info['film']}\n "
                i+=1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Список популярных сериалов Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "top":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == '50 лучших сериалов Netflix по рейтингу сайта IMDb':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1


        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Список популярных сериалов Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "animate":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Анимационные сериалы Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1


        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Анимационные сериалы Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "action":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Сериалы боевики Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Сериалы боевики Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "detective":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Сериалы детективы Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Сериалы детективы Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "dram":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Драматические сериалы Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Драматические сериалы Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "historical":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Исторические сериалы Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Исторические сериалы Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "comedy":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Комедийные сериалы Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Комедийные сериалы Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "crime":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Криминальные сериалы Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Криминальные сериалы Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "melodram":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Мелодраматические сериалы Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Мелодраматические сериалы Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "teen":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Подростковые сериалы Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Подростковые сериалы Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "super":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Супергеройские сериалы Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Супергеройские сериалы Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "triller":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Сериалы триллеры Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Сериалы триллеры Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "horror":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Сериалы ужасов Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Сериалы ужасов Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "fantastic":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Фантастические сериалы Netflix':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Фантастические сериалы Netflix|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "fantasy":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Сериалы Netflix в стиле фэнтези':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Сериалы Netflix в стиле фэнтези|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "usa":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Сериалы Netflix производства США':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Сериалы Netflix производства США|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "britain":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Сериалы Netflix производства Великобритании':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Сериалы Netflix производства Великобритании|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "canada":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Сериалы Netflix производства Канады':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Сериалы Netflix производства Канады|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)



    elif call.data == "spain":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Сериалы Netflix производства Испании':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Сериалы Netflix производства Испании|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)


    elif call.data == "germany":
        text = ''
        i = 1
        with open('info.json','r',encoding='UTF-8') as f:
            s = json.load(f)
        for info in s:
            if info['genre'] == 'Сериалы Netflix производства Германии':
                # print(info['film'])
                text += f"{i}.{info['film']}\n "
                i += 1

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='|Сериалы Netflix производства Германии|\n'+'*'*45+'\n'+text,
                              reply_markup=keyboard)

    elif call.data == "update":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Происходит обновление списка сериалов. Подождите немного.....')
        all = []
        listok = ['comedy', 'horror', 'popular', 'best', 'animation', 'action', 'detective', 'drama', 'historical',
                  'crime', 'melodrama', 'teen', 'superhero', 'thriller', 'fantasy', 'science-fiction', 'usa', 'spain',
                  'germany', 'canada', 'great-britain']
        ua = UserAgent()
        for i in listok:
            reg = requests.get(f'https://youflix.ru/shows-categories/{i}/', headers={'user-agent': f'{ua.random}'})
            soup = bs4.BeautifulSoup(reg.content, 'html.parser')
            section = soup.select('article.page')
            for names in section:
                namess = names.select('p')
                genres = names.select_one('header.entry-header')
                for name in namess:
                    if name.select_one('strong') not in name:
                        continue
                    name = name.select_one('strong')
                    print(genres.get_text().strip())
                    print(name.get_text())
                    all.append({
                        'genre': genres.get_text().strip(),
                        'film': name.get_text(),
                    })
        with open('info.json', 'w', encoding='utf-8') as f:
            json.dump(all, f, indent=4, ensure_ascii=False)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="genres")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Список сериалов успешно обновлён.',
                              reply_markup=keyboard)

bot.polling(none_stop = 'True')