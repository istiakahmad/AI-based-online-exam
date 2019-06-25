import sqlite3
conn = sqlite3.connect('database.db')
print("database created")
c = conn.cursor()


def create(c):
    sql_create = """
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
               id integer unique primary key autoincrement,
               name text
    );
    """
    c.executescript(sql_create)
    print("Table Created")


def insert(c):
    sql_insert = """INSERT INTO users
    (id, name)
    VALUES (1, 'ahmad'), (2, 'anika'), (3, 'rakin');
    """
    c.executescript(sql_insert)
    print("Inserted")


def select(c):
    c = conn.cursor()
    c.execute("SELECT * FROM users")

    rows = c.fetchall()

    for row in rows:
        print(row)
    print("showed database")


def update(c, query):
    sql = ''' UPDATE users
              SET name = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, query)


def delete(c, query):
    sql = ''' DELETE FROM users where id=? '''
    cur = conn.cursor()
    cur.execute(sql, (query,))


create(c)
insert(c)
select(c)
update(c, ("istiak", 2))
select(c)
#delete(c, 2)
#select(c)

conn.commit()
conn.close()
