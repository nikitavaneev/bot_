from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import datetime
import telebot  # импорт pyTelegramBotAPI
from telebot import types  # также достанем типы
import pandas as pd
import re
bot = telebot.TeleBot("5490566325:AAECPOsb6JlfLrGmBZteaFNqprSQQ9sPbRs")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but2 = types.KeyboardButton("Парсим")
    markup.add(but2)
    bot.reply_to(message, "Нажми кнопку Парсим".format(message.from_user), parse_mode='html', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def parscing_pinnacle(message):
    if message.chat.type == 'private':
        if message.text == "Парсим":

            chatid = message.chat.id
            spisok_true = []
            work_dir_start = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screens_bot')
            E0 = 'england-premier-league'
            D1 = 'germany-bundesliga'
            E1 = 'england-championship'
            F1 = 'france-ligue-1'
            I1 = 'italy-serie-a'
            SP1 = 'spain-la-liga'
            spisok = [E0, D1, E1, F1, I1, SP1]
            chr_options = Options()
            chr_options.add_argument("--start-maximized")
            driver = webdriver.Chrome(executable_path=r'C:\jupiter\ii\chromedriver.exe', options=chr_options)
            spisok_all = [10, 9, 12, 10, 10, 10]
            spisok_start = [0, 0, 0, 0, 0, 0]
            spisok_dict = dict(zip(spisok, spisok_start))
            while len(spisok) > 0:
                dt = []
                # dt_17 = []
                for i, div in enumerate(spisok):
                # if spisok_dict[div]!=spisok_all[i]:
                    link = f'https://www.pinnacle.com/ru/soccer/{div}/matchups/#leagueType:Corners'
                    driver.get(link)
                    if driver.current_url == link:

                        print(div)
                        time.sleep(5)
                        e = driver.find_elements(By.CSS_SELECTOR, "div > [class='style_row__3q4g_ style_row__3hCMX']")
                        # if len(e) == spisok_all[i]:
                        for i in range(len(e)):
                            #     dt_17.append(e[i].text)
                            #     dt_17[-1] = dt_17[-1].splitlines()
                            # else:
                            dt.append(e[i].text)
                            dt[-1] = dt[-1].splitlines()
                            if len(dt[-1]) != 12:
                                dt.remove(dt[-1])
                        # print(dt)
                        full_screen = driver.find_element(By.XPATH,
                                                          '//*[@id="root"]/div/div[2]/main/div/div[5]/h2/span')
                        driver.execute_script('arguments[0].scrollIntoView({block: "end", inline: "nearest"});',
                                              full_screen)
                        driver.save_screenshot(os.path.join(work_dir_start, f'{div}_{len(e)}.png'))
                        spisok_dict[div] = len(e)
                            # spisok.remove(div)
                            # spisok_all.pop(i)
                            # spisok_start.pop(i)

                        # else:
                        #     if len(e) != spisok_start[i]:
                        #         full_screen = driver.find_element(By.XPATH,
                        #                                           '//*[@id="root"]/div/div[2]/main/div/div[5]/h2/span')
                        #         driver.execute_script('arguments[0].scrollIntoView({block: "end", inline: "nearest"});',
                        #                               full_screen)
                        #         driver.save_screenshot(f'C:\jupiter\DREAM\screens_bot/{div}_{len(e)}.png')
                        #         # driver.execute_script("arguments[0].scrollIntoView();", e[-1])
                        #         spisok_start[i] = len(e)
                        # else:
                        #     print('Обновлений нет')

                        print(f'Длина {div} ', len(e))
                        # print('spisok_start', spisok_start)

                        # driver.save_screenshot(f'{div}_{len(e)}.png')
                        # print(screenshot('div.png'))
                    else:
                        print('Web site does not exist')
                        print(link)
                        print(driver.current_url)
                        print('No: ' + div)
            # pr = []
            # for i, div in enumerate(spisok):
            #     if spisok_all[i] == spisok_start[i]:
            #         pr+=[i]
            # for i in pr:
            #     print('Удалили', spisok[i])
            #     del spisok[i]
            #     del spisok_all[i]
            #     del spisok_start[i]
            # print('Остались',spisok)
                dt = pd.DataFrame(dt, columns=['HomeTeam', 'AwayTeam', 'time', 'fora', 'kef_home', 'fora_', 'kef_away',
                                               'Total', 'Kef_B', 'total_', 'Kef_M', 'plus'])
                # dt_17 = pd.DataFrame(dt_17, columns=['HomeTeam','G1', 'AwayTeam','G2', 'time','p1','x','p2', 'fora', 'kef_home', 'fora_', 'kef_away',
                #                                'total', 'kef_B', 'total_', 'kef_M', 'plus'])
                dt = dt[['HomeTeam', 'AwayTeam', 'Total', 'Kef_M', 'Kef_B']]
                dt['Total'] = dt['Total'].astype('float')
                dt['Kef_M'] = dt['Kef_M'].astype('float')
                dt['Kef_B'] = dt['Kef_B'].astype('float')
                dt['HomeTeam'] = dt['HomeTeam'].str.replace(r'..[Уу]гловые.', '', regex=True)
                dt['AwayTeam'] = dt['AwayTeam'].str.replace(r'..[Уу]гловые.', '', regex=True)
                dt['HomeTeam'] = dt['HomeTeam'].str.replace(r'..[Cc]orners.', '', regex=True)
                dt['AwayTeam'] = dt['AwayTeam'].str.replace(r'..[Cc]orners.', '', regex=True)
                x1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Russian_tab.xlsx')
                x = pd.ExcelFile(x1)
                true_data = x.parse('Лист1')
                data_ecxel = true_data['ecxel_name'].tolist()
                data_pinacle = true_data['pinacle_name'].tolist()
                dt = dt.replace(data_pinacle, data_ecxel)
                rt = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stavki_prog_full_matches.xlsx')
                x = pd.ExcelFile(rt)
                load_ = x.parse('all_match')
                load_ = pd.concat([load_,dt])
                load_ = load_.drop_duplicates(subset=['HomeTeam','AwayTeam'],keep='first')
                lst_ = pd.ExcelWriter(rt, mode='a',
                                      engine="openpyxl", if_sheet_exists="replace", )
                load_.to_excel(lst_, sheet_name=f'all_match', index=False)
                lst_.save()
                # print('spisok_start', spisok_dict)
                final_rep = [xlsx for xlsx in os.listdir(work_dir_start)]
                final = list(set(final_rep) - set(spisok_true))
                print(final)
                for i in range(len(final)):
                    # with open(work_dir_start + '/' + final_rep[i], 'rb') as k:
                    k = open(os.path.join(work_dir_start, final[i]), 'rb')
                    bot.send_message(chatid, f"{final[i].split('_')[0]}")
                    bot.send_photo(chatid, k)
                    k.close()
                    # bot.send_photo(chatid, k)
                    # k.close()
                spisok_true += final
                spisok_true = list(set(spisok_true))
                # print(spisok_true)
                print('время загрузки', datetime.datetime.now().time())
                time.sleep(900)
                driver.set_page_load_timeout(600)
                # time.sleep(5)
                # os.remove(work_dir_start + '/' + final_rep[i])
                # shutil.move(os.path.join(work_dir_start, final_rep[i]), work_dir_finish)
                # shutil.rmtree(work_dir_start)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex,'ошибка')
        time.sleep(15)
