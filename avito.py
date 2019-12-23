import requests
from bs4 import BeautifulSoup
question = input('Поиск: ')
search_line = '%20'.join(question.split())
url = 'https://www.avito.ru/ekaterinburg/sport_i_otdyh/zimnie_vidy_sporta?cd=1&q='+search_line
r = requests.get(url)

soup = BeautifulSoup(r.content.decode('utf-8'))
search = soup.find_all('div', {'class': 'snippet-horizontal item item_table clearfix js-catalog-item-enum item-with-contact js-item-extended'})

search_list = []
for items in search:
    total_dict = {}
    #Ищем внутри одного из div-ов внутренний div, в нем атрибут а, и из него вытаскиваем ссылку
    href = items.find('div', {'class': 'snippet-title-row'}).find('a').get('href')
    total_dict.update({'href':href})
    #Тоже самое, но достаем текст ссылки
    name = items.find('div', {'class': 'snippet-title-row'}).find('a').text
    str_name = str(name)
    total_dict.update({'name':name})
    #Ищем цену
    price = items.find('span', {'class': 'price'}).text
    total_dict.update({'price':price})
    search_list.append(total_dict)
    if 'в Екатеринбурге' in str_name:
        ekb_total_dict = total_dict
        search_list.append(ekb_total_dict)

print(search_list)

#with open('/home/padavan/test_avito0512.html', 'w') as output_file:
#    output_file.write(' '.join(search_list))
