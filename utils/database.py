import requests
import sqlite3
import datetime

class database:
    def __init__(self):
        self.initiate_db()

    def initiate_db(self):
        conn = sqlite3.connect("llm_chat.db")

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            timestamp TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user', 'system', 'assistant')),
            message TEXT NOT NULL
        )
        """)

        conn.commit()
        self.cursor = cursor
        self.conn = conn

    def get_conversation(self, user_id):
        self.cursor.execute("""
                       SELECT timestamp, role, message FROM chat_messages
                       WHERE user_id = ?
                       ORDER BY timestamp ASC
                       """, (user_id,))

        return self.cursor.fetchall()

    def insert_message(self, user_id, role, message):

        timestamp = datetime.datetime.now()
        self.cursor.execute("""
            INSERT INTO chat_messages (user_id, timestamp, role, message)
            VALUES (?, ?, ?, ?)
        """, (user_id, timestamp, role, message))
        self.conn.commit()

    def chat(self, user_id, prompt):
        self.initiate_new_user(user_id)
        url = "http://192.168.0.176:11434/api/chat"
        headers = {"Content-Type": "application/json"}

        messages = [{"role": role, "content": message}
                    for _timestamp, role, message in self.get_conversation(user_id)]
        
        messages.append({"role": "user", "content": prompt})

        
        payload = {
            "model": "llama3.2",
            "messages": messages,
            "stream": False
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_string = None
        try:
            data = response.json()
            response_string = data['message']['content']
            if len(response_string) > 2000:
                response_string = response_string[:2000]

            self.insert_message(user_id, "user", prompt)
            self.insert_message(user_id, "assistant", response_string)
            return response_string
        except Exception as e:
            print(e)

    def initiate_new_user(self, user_id):
        if not self.user_exists(user_id):
            message = "You are a helpful assistant. Try to keep your responses under 2000 characters"
            self.insert_message(user_id, "system", message)
    

    def user_exists(self, user_id):
        self.cursor.execute("""
                            SELECT 1 FROM chat_messages
                            WHERE user_id = ?
                            LIMIT 1
                            """, (user_id,))
        return self.cursor.fetchone()


    def delete_convo (self, user_id):
        self.cursor.execute("""
        DELETE FROM chat_messages
        WHERE user_id = ?
    """, (user_id,))
        self.conn.commit()



    def delete_recent_convo(self, user_id, within_minutes=60):
        cutoff = datetime.datetime.now() - datetime.timedelta(minutes=within_minutes)

        self.cursor.execute("""
        DELETE FROM chat_messages
        WHERE user_id = ?
        AND timestamp >= ?
        AND role != 'system'
        """, (user_id, cutoff))

        self.conn.commit()