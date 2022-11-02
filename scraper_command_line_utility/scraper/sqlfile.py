import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute(
            "CREATE TABLE IF NOT EXISTS rss (id, title, link, domain, author, time_published, keywords, content, content_summary)")
    except sqlite3.Error as e:
        print(e)

    return conn


def insert_rss_data(conn, rss_list):
    sql = """ insert into rss values (?, ?, ?, ?, ?, ?, ?, ?, ?) """
    cur = conn.cursor()
    cur.executemany(sql, rss_list)
    conn.commit()
    return cur.lastrowid


def receive_data(posts):
    database = r"rss.db"
    conn = create_connection(database)
    insert_rss_data(conn, posts)
