import requests
from bs4 import BeautifulSoup
from datetime import datetime


def Question():
    question = input('Поиск: ')
    search_line = '%20'.join(question.split())
    return search_line

def ParserFromAvito(search_line):
    date = str(datetime.now().date())

    #question = input('Поиск: ')
    #search_line = '%20'.join(question.split())
    url = 'https://www.avito.ru/ekaterinburg/sport_i_otdyh/zimnie_vidy_sporta?cd=1&q='+search_line
    r = requests.get(url)

    soup = BeautifulSoup(r.content.decode('utf-8'), "html.parser")
    search = soup.find_all('div', {'class': 'snippet-horizontal item item_table clearfix js-catalog-item-enum item-with-contact js-item-extended'})

    search_list = []
    for items in search:
        items_list = []

        #Ищем внутри одного из div-ов внутренний div и достаем текст ссылки
        name = items.find('div', {'class': 'snippet-title-row'}).find('a').text
        strip_name = name.strip('\n ')
        items_list.append(strip_name)

        #Ищем цену, делим строку, чтобы избавиться от символа рубля и собираем в число
        price = items.find('span', {'class': 'price'}).text
        split_price = price.split()
        clear_price = ''.join(split_price[:-1])
        items_list.append(int(clear_price))

        #Ищем внутри одного из div-ов внутренний div, в нем атрибут а, и из него вытаскиваем ссылку
        href = items.find('div', {'class': 'snippet-title-row'}).find('a').get('href')
        items_list.append(href)

        #Добавляем дату
        items_list.append(date)

        #Добавляем все в итоговый список
        search_list.append(items_list)
    return search_list


if __name__ == "__main__":
    print(ParserFromAvito(Question()))


#with open('/home/padavan/test_avito0512.html', 'w') as output_file:
#    output_file.write(' '.join(search_list))
