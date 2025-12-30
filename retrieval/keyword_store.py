import sqlite3

class KeywordStore:
    def __init__(self, db_path="keywords.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5(text)"
        )

    def add(self, chunks):
        for c in chunks:
            self.conn.execute("INSERT INTO docs(text) VALUES (?)", (c["text"],))
        self.conn.commit()

    def search(self, query, top_k=5):
        cursor = self.conn.execute(
            "SELECT text FROM docs WHERE docs MATCH ? LIMIT ?",
            (query, top_k)
        )
        return [{"text": row[0], "score": 0.3} for row in cursor.fetchall()]
