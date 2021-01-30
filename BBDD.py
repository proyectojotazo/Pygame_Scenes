import sqlite3
import os

from folders import DB_FOLDER
from config import GOLD, SILVER, BRONCE, WHITE


class BBDD:

    def __init__(self):
        '''
        Database class. It creates the database file in 'data' path
        named 'records.db'.
        First time we call it fills with default records
        Every time we instantiate BBDD we set records to have only
        five
        '''
        self.default_records = [
            (10000, 'JGH'),
            (8500, 'AGH'),
            (6000, 'AHD'),
            (4500, 'AGM'),
            (2000, 'NLG'),]
        self._create_table()
        self._insert_default_records()
        
    def _execute_query(self, query, params=(), many=False):
        conn = sqlite3.connect(os.path.join(DB_FOLDER, 'records.db'))
        c = conn.cursor()
        
        if many:
            c.executemany(query, params)
        else:
            c.execute(query, params)
            data = c.fetchall()
            if data:
                conn.commit()
                c.close()
                return data

        conn.commit()
        c.close()

    def _create_table(self):
        '''
        Creates the table IF NOT EXISTS
        '''
        query = '''
        CREATE TABLE IF NOT EXISTS records(
        score INTEGER NOT NULL,
        name text NOT NULL);
        '''
        self._execute_query(query)

    def check_new_record(self, score):

        records = self._select_records()

        for record in records:
            if score > record[0]:
                return True

        return False

    def insert_new_record(self, new_record):
        '''
        Inserts new record
        '''
        query = '''
                INSERT INTO records(score, name)
                VALUES(?, ?)
                '''

        self._execute_query(query, new_record)

    def _insert_default_records(self):
        '''
        If database is empty we fill with default
        records
        '''
        query = '''
                INSERT INTO records(score, name)
                VALUES(?, ?)
                '''

        if not self._select_records():
            self._execute_query(query, self.default_records, many=True)

    def _select_records(self):
        '''
        Order table descendent for score
        First of all we set the db to five records
        Then we execute the query and we get 
        data from records.db
        '''
        query = '''
        SELECT * FROM records ORDER BY score DESC
        '''

        rows = self._execute_query(query)

        return rows

    def _set_records_to_five(self):

        records = self._select_records()

        if len(records) > 5:
            last = records[4][0]
            query = f'''
            DELETE FROM records
            WHERE score < {last}
            '''
            self._execute_query(query)

    def get_dict_records(self, data):
        '''
        returns a dict as:
        d = {
            'record1':{
                'rank':x,
                'score':y,
                'name':'ABC',
                'color':RGBCOLOR(0,0,0)
            },
            ...
        }
        for put them on records screen
        With the first forloop, we create the dicts with
        the records data, then we add them to main dict
        as name records.
        '''
        records = {}
        rec = [f'record{x}' for x in range(1,6)]
        keys = ['rank', 'score', 'name', 'color']
        l = []

        for ix in range(len(data)):
            if ix == 0:
                d = {
                    keys[0]:str(ix+1),
                    keys[1]:data[ix][0],
                    keys[2]:data[ix][1],
                    keys[3]:GOLD,
                }
                l.append(d)
            elif ix == 1:
                d = {
                    keys[0]:str(ix+1),
                    keys[1]:data[ix][0],
                    keys[2]:data[ix][1],
                    keys[3]:SILVER,
                }
                l.append(d)
            elif ix == 2:
                d = {
                    keys[0]:str(ix+1),
                    keys[1]:data[ix][0],
                    keys[2]:data[ix][1],
                    keys[3]:BRONCE,
                }
                l.append(d)
            else:
                d = {
                    keys[0]:str(ix+1),
                    keys[1]:data[ix][0],
                    keys[2]:data[ix][1],
                    keys[3]:WHITE,
                }
                l.append(d)

        for ix in range(len(data)):
            records[rec[ix]] = l[ix]

        return records

    def _delete_all_records(self):

        query = '''
        DELETE FROM records
        '''
        self._execute_query(query)

    def reset_records(self):
        self._delete_all_records()
        self._insert_default_records()
    
if __name__ == '__main__':
    a = BBDD()
    