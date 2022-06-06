import sqlite3
import requests
import xml.etree.ElementTree as et


class WriteDB:
    
    def fetch_book_data(self, isbn):
        endpoint = 'https://iss.ndl.go.jp/api/sru'
        params = {'operation': 'searchRetrieve',
                  'query': f'isbn="{isbn}"',
                  'recordPacking': 'xml'}

        res = requests.get(endpoint, params=params)
        root = et.fromstring(res.text)
        ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
        title = root.find('.//dc:title', ns).text
        creator = root.find('.//dc:creator', ns).text
        publisher = root.find('.//dc:publisher', ns).text
        subject = root.find('.//dc:subject', ns).text

        return isbn, title, creator, publisher, subject

    def is_isbn(self, code):
        return len(code) == 13 and code[:3] == '978'


class OrenoDataBase:

    def __init__(self):
        self.conn = sqlite3.connect(r'.\db.sqlite3')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def get(self):
        self.cur.execute('SELECT * FROM books_book')
        rows = []

        for r in self.cur.fetchall():
            rows.append({'isbn': r['isbn'], 'title': r['title'], 'creator': r['creator'], 
                         'publisher': r['publisher'], 'subject': r['subject']})

        return rows

    def set(self, values):

        try:
            place_holder = ','.join('?'*len(values))
            self.cur.execute(f'INSERT INTO books_book("isbn", "title", "creator", "publisher", "subject") VALUES ({place_holder})', values)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def close(self):
        self.cur.close()
        self.conn.close()



wdb =WriteDB()
db = OrenoDataBase()

result = wdb.fetch_book_data('9784777519699')
print(result)
db.set(result)

db.close()

