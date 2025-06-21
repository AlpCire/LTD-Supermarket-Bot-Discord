import sqlite3
import os

DB_NAME = os.getenv("DB_NAME", "locales.sqlite")

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS locales (nombre TEXT PRIMARY KEY, membresia INTEGER DEFAULT 0, compras INTEGER DEFAULT 0)")
        conn.commit()

def alta_local(nombre):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO locales (nombre) VALUES (?)", (nombre.lower(),))
        conn.commit()

def dar_membresia(nombre):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("UPDATE locales SET membresia = 1 WHERE nombre = ?", (nombre.lower(),))
        conn.commit()

def agregar_compra(nombre):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("UPDATE locales SET compras = compras + 1 WHERE nombre = ?", (nombre.lower(),))
        c.execute("SELECT compras, membresia FROM locales WHERE nombre = ?", (nombre.lower(),))
        row = c.fetchone()
        return row

def obtener_compras(nombre):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT compras FROM locales WHERE nombre = ?", (nombre.lower(),))
        row = c.fetchone()
        return row[0] if row else 0
