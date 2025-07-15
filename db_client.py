import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("S2_HOST"),
        user=os.getenv("S2_USER"),
        password=os.getenv("S2_PASS"),
        database=os.getenv("S2_DB"),
        port=int(os.getenv("S2_PORT")),
        cursorclass=pymysql.cursors.DictCursor
    )

def save_summary(url, title, summary):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO article_summaries (url, title, summary)
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (url, title, summary))
        conn.commit()
    except Exception as e:
        print(f"❌ DB insert failed: {e}")
    finally:
        if conn:
            conn.close()