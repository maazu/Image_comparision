
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

con = sqlite3.connect('bus_route.db')
c = con.cursor()

img_data = [('Michael', 'Fox'),
                    ('Adam', 'Miller'),
                    ('Andrew', 'Peck'),
                    ('James', 'Shroyer'),
                    ('Eric', 'Burger')]




c.execute('''CREATE TABLE image_data
             (image_id INTEGER PRIMARY KEY,
              route varchar(40),
              image_name varchar(40),
              location varchar(40) )''')

#c.executemany('INSERT INTO image_data(route, image_name,location) VALUES (?,?)', data_person_name)

for row in c.execute('SELECT * FROM image_data'):
    print (row)





