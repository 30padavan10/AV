import psycopg2
import re

def connect():
    conn = psycopg2.connect("dbname=testdb user=postgres password=postgres")
    cur = conn.cursor()
    return cur

def exit():
    cur.close()
    conn.close()

def datainput():
    data = input('Search: ')
    return data


def add_to_db(table, data):
    conn = psycopg2.connect("dbname=testdb user=postgres password=postgres")
    cur = conn.cursor()
    #try:
    #    sql = "SELECT * FROM {};".format(table)
    #    cur.execute(sql)
    #except UndefinedTable:
    sql_create = "CREATE TABLE IF NOT EXISTS {} (name varchar(150), href varchar(150), city varchar(150), price int, date date, description text)".format(table)
    print(sql_create)
    cur.execute(sql_create)
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
            print('Новый:  '+name+'  '+str(price)+'  '+href+'  '+city)
        else:
            try:
                new_desc=str(last_price)+'р '+str(last_date)+' '+description
            except TypeError:
                new_desc=str(last_price)+'р '+str(last_date)
            finally:
                sql_del_entry = "DELETE FROM {} WHERE href = '{}'".format(table, href)
                cur.execute(sql_del_entry)
                sql_update_table = "insert into {} (name, price, href, city, date, desc) values ('{}', {}, '{}', '{}' '{}', '{}')".format(table, name, price, href, city, date, new_desc)
                cur.execute(sql_update_table)
                conn.commit()
                print('Изменился '+name+'  '+str(price)+'  '+href+'  '+city+'  '+new_desc)
                


data = [['\n Маска для сноуборда и горных лыж Oakley Splice\n ', 5000, '/ekaterinburg/sport_i_otdyh/maska_dlya_snouborda_i_gornyh_lyzh_oakley_splice_1774700923', '2019-12-19'], ['\n Женские Горнолыжные очки Oakley\n ', 2000, '/ekaterinburg/sport_i_otdyh/zhenskie_gornolyzhnye_ochki_oakley_1135058010', '2019-12-19'], ['\n Маска Oakley O2XL Matte White/Persimmon\n ', 3500, '/ekaterinburg/sport_i_otdyh/maska_oakley_o2xl_matte_whitepersimmon_1148321556', '2019-12-19']]

if __name__ == '__main__':
    add_to_db('oakley', data)




