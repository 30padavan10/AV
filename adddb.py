import psycopg2
import avito

def add_to_db(table, data):
    table = table.replace('%20', '_')
    conn = psycopg2.connect("dbname=testdb user=postgres password=postgres")
    cur = conn.cursor()
    sql_create = "CREATE TABLE IF NOT EXISTS {} (name varchar(150), href varchar(150), city varchar(150), price int, date date, description text)".format(table)
    cur.execute(sql_create)
    conn.commit()
    for post in data:
        name, price, href, date = post
        city = 'ekaterinburg' if 'ekaterinburg' in href else 'other'
        sql_href = "SELECT price, date, description FROM {} WHERE href = '{}'".format(table, href)
        cur.execute(sql_href)
        try:
            #type(cur.fetchone()[0]) == str
            last_price, last_date, description = cur.fetchone()
        except TypeError:
            sql_insert_table = "insert into {} (name, price, href, city, date) values ('{}', {}, '{}', '{}', '{}')".format(table, name, price, href, city, date)
            cur.execute(sql_insert_table)
            conn.commit()
            print('Новый:  '+name+'  '+str(price)+'  '+city)
        else:
            if last_price != price:
                try:
                    new_desc=str(last_price)+'р '+str(last_date)+' '+description
                except TypeError:
                    new_desc=str(last_price)+'р '+str(last_date)
                finally:
                    sql_del_entry = "DELETE FROM {} WHERE href = '{}'".format(table, href)
                    cur.execute(sql_del_entry)
                    sql_update_table = "insert into {} (name, price, href, city, date, description) values ('{}', {}, '{}', '{}', '{}', '{}')".format(table, name, price, href, city, date, new_desc)
                    cur.execute(sql_update_table)
                    conn.commit()
                    print('Изменился '+name+'  '+str(price)+'  '+city+'  '+new_desc)
            else:
                pass
    cur.close()
    conn.close()
                


data = [['\n Маска для сноуборда и горных лыж Oakley Splice\n ', 5000, '/ekaterinburg/sport_i_otdyh/maska_dlya_snouborda_i_gornyh_lyzh_oakley_splice_1774700923', '2019-12-21'], ['\n Женские Горнолыжные очки Oakley\n ', 2000, '/ekaterinburg/sport_i_otdyh/zhenskie_gornolyzhnye_ochki_oakley_1135058010', '2019-12-19'], ['\n Маска Oakley O2XL Matte White/Persimmon\n ', 3500, '/ekaterinburg/sport_i_otdyh/maska_oakley_o2xl_matte_whitepersimmon_1148321556', '2019-12-19']]

if __name__ == '__main__':
    quest = avito.Question()
    add_to_db(quest, avito.ParserFromAvito(quest))




