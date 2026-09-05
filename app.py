import json
import os
import sqlite3

DB_NAME = "jarvis_command_core.db"
BACKUP_JSON = "jarvis_universal_backup.json"


def init_db_and_sync():
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()

  # Creación de tablas de almacenamiento
  c.execute(
      "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT,"
      " timestamp TEXT, content TEXT, category TEXT)"
  )
  c.execute(
      "CREATE TABLE IF NOT EXISTS documents_store (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, title TEXT, category TEXT, content TEXT)"
  )
  c.execute(
      "CREATE TABLE IF NOT EXISTS finances (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, concept TEXT, amount REAL, type TEXT)"
  )
  c.execute(
      "CREATE TABLE IF NOT EXISTS legal_records (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, title TEXT, category TEXT, expiry"
      " TEXT, content TEXT)"
  )
  c.execute(
      "CREATE TABLE IF NOT EXISTS gmail_cache (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, timestamp TEXT, sender TEXT, subject TEXT, snippet"
      " TEXT)"
  )

  # Restauración automática desde archivo JSON si la BD local está vacía
  c.execute("SELECT COUNT(*) FROM documents_store")
  doc_count = c.fetchone()[0]

  if doc_count == 0 and os.path.exists(BACKUP_JSON):
    try:
      with open(BACKUP_JSON, "r", encoding="utf-8") as f:
        backup_data = json.load(f)

        for d in backup_data.get("documents", []):
          c.execute(
              "INSERT INTO documents_store (timestamp, title, category,"
              " content) VALUES (?, ?, ?, ?)",
              (d["timestamp"], d["title"], d["category"], d["content"]),
          )

        for l in backup_data.get("legal", []):
          c.execute(
              "INSERT INTO legal_records (timestamp, title, category, expiry,"
              " content) VALUES (?, ?, ?, ?, ?)",
              (l["timestamp"], l["title"], l["category"], l["expiry"], l["content"]),
          )

        for m in backup_data.get("gmail", []):
          c.execute(
              "INSERT INTO gmail_cache (timestamp, sender, subject, snippet)"
              " VALUES (?, ?, ?, ?)",
              (m["timestamp"], m["sender"], m["subject"], m["snippet"]),
          )

        for f_item in backup_data.get("finances", []):
          c.execute(
              "INSERT INTO finances (timestamp, concept, amount, type) VALUES"
              " (?, ?, ?, ?)",
              (
                  f_item["timestamp"],
                  f_item["concept"],
                  f_item["amount"],
                  f_item["type"],
              ),
          )

        conn.commit()
    except Exception:
      pass

  conn.close()
  export_to_json_backup()


def export_to_json_backup():
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT timestamp, title, category, content FROM documents_store")
    docs = [
        {
            "timestamp": r[0],
            "title": r[1],
            "category": r[2],
            "content": r[3],
        }
        for r in c.fetchall()
    ]

    c.execute(
        "SELECT timestamp, title, category, expiry, content FROM legal_records"
    )
    legal = [
        {
            "timestamp": r[0],
            "title": r[1],
            "category": r[2],
            "expiry": r[3],
            "content": r[4],
        }
        for r in c.fetchall()
    ]

    c.execute("SELECT timestamp, sender, subject, snippet FROM gmail_cache")
    gmail = [
        {
            "timestamp": r[0],
            "sender": r[1],
            "subject": r[2],
            "snippet": r[3],
        }
        for r in c.fetchall()
    ]

    c.execute("SELECT timestamp, concept, amount, type FROM finances")
    finances = [
        {
            "timestamp": r[0],
            "concept": r[1],
            "amount": r[2],
            "type": r[3],
        }
        for r in c.fetchall()
    ]

    conn.close()

    backup_data = {
        "documents": docs,
        "legal": legal,
        "gmail": gmail,
        "finances": finances,
    }
    with open(BACKUP_JSON, "w", encoding="utf-8") as f:
      json.dump(backup_data, f, ensure_ascii=False, indent=4)
  except Exception:
    pass


# Llamar a la función al arrancar la app
init_db_and_sync()
