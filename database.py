import sqlite3

DB_NAME = "sportsnews.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS posted_news(
            article_id TEXT PRIMARY KEY,
            channel TEXT,
            published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    def is_posted(self, article_id, channel):
        self.cursor.execute(
            "SELECT 1 FROM posted_news WHERE article_id=? AND channel=?",
            (article_id, channel),
        )
        return self.cursor.fetchone() is not None

    def save_post(self, article_id, channel):
        self.cursor.execute(
            "INSERT OR IGNORE INTO posted_news(article_id, channel) VALUES(?, ?)",
            (article_id, channel),
        )
        self.conn.commit()


db = Database()
