# Discord Locales Bot 🏪

Bot de Discord para registrar locales, asignar membresías y llevar control de compras. Cada 10 compras válidas (de más de $10,000), se otorga un premio al local con membresía.

## 🚀 Deploy en Railway (1 Clic)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/-X5FeG?referralCode=discord-bot)

1. Haz clic en el botón
2. Inicia sesión o regístrate
3. Añade la variable `DISCORD_TOKEN`
4. Railway hará el resto 🚀

## ✅ Comandos disponibles

- `/alta {nombre}` → Solo para roles permitidos: Cajero, Reponedor, Gerente, Gerente General, Supervisor
- `/membresia {nombre}` → Igual que `/alta`
- `/compra {nombre} {monto}` → Solo roles permitidos + monto > $10,000 USD
- `/premio {nombre}` → Permitido a todos excepto @everyone

## 🛠 Requisitos locales

```bash
pip install -r requirements.txt
python bot.py
```
