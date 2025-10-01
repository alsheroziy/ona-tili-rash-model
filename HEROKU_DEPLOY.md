# 🚀 Heroku'ga Deploy Qilish

Bu qo'llanma Telegram botni Heroku'ga qanday joylashtirishni ko'rsatadi.

## 📋 Talablar

- Heroku account (https://signup.heroku.com/)
- Heroku CLI o'rnatilgan
- Git o'rnatilgan
- Telegram Bot Token

## 🛠 1. Heroku CLI O'rnatish

### macOS
```bash
brew tap heroku/brew && brew install heroku
```

### Ubuntu/Debian
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### Windows
Heroku CLI'ni yuklab oling: https://devcenter.heroku.com/articles/heroku-cli

## 🔐 2. Heroku'ga Kirish

```bash
# Heroku'ga login qiling
heroku login

# Browser ochiladi va login qilasiz
```

## 📦 3. Heroku App Yaratish

```bash
# Loyiha papkasiga kiring
cd /path/to/your/bot

# Heroku app yaratish
heroku create your-bot-name

# Yoki random nom bilan:
heroku create

# Git remote qo'shilganini tekshiring
git remote -v
```

## ⚙️ 4. Environment Variables Sozlash

```bash
# BOT_TOKEN qo'shish
heroku config:set BOT_TOKEN=your_bot_token_here

# ADMINS qo'shish (comma-separated)
heroku config:set ADMINS=123456789,987654321

# DB_NAME qo'shish
heroku config:set DB_NAME=test_bot.db

# Barcha config'larni ko'rish
heroku config
```

## 🚀 5. Deploy Qilish

```bash
# O'zgarishlarni commit qiling
git add .
git commit -m "Prepare for Heroku deployment"

# Heroku'ga push qiling
git push heroku main

# Yoki master branch bo'lsa:
git push heroku master
```

## 🔄 6. Worker Dyno'ni Yoqish

```bash
# Worker dyno'ni scale qilish (1 ta worker)
heroku ps:scale worker=1

# Dyno holatini ko'rish
heroku ps
```

**Muhim:** Heroku'da worker dyno ishga tushirilishi kerak, web emas!

## 📊 7. Loglarni Ko'rish

```bash
# Real-time loglar
heroku logs --tail

# Oxirgi 100 ta log
heroku logs -n 100

# Faqat app loglari
heroku logs --source app
```

## 🔍 8. Bot Holatini Tekshirish

```bash
# Dyno status
heroku ps

# App ma'lumotlari
heroku apps:info

# Config variables
heroku config
```

## 🔄 9. Bot'ni Restart Qilish

```bash
# Bot'ni qayta ishga tushirish
heroku restart

# Yoki worker dyno'ni restart qilish
heroku ps:restart worker
```

## 💾 10. Database (SQLite Muammosi)

**Diqqat:** Heroku ephemeral filesystem ishlatadi, ya'ni har restart'da fayl tizimi tozalanadi!

### Yechim 1: PostgreSQL Ishlatish (Tavsiya)

```bash
# PostgreSQL qo'shish
heroku addons:create heroku-postgresql:essential-0

# DATABASE_URL avtomatik sozlanadi
heroku config:get DATABASE_URL
```

Keyin `database.py` faylni PostgreSQL uchun o'zgartirish kerak.

### Yechim 2: AWS S3 / Cloudinary (SQLite uchun)

SQLite'ni S3'da saqlash va sync qilish mumkin.

### Yechim 3: Boshqa Hosting (Docker)

Agar SQLite kerak bo'lsa, VPS (DigitalOcean, Linode) yoki Docker container ishlatish yaxshiroq.

## 📝 11. Heroku Fayllari

Loyihangizda quyidagi fayllar bo'lishi kerak:

### `Procfile`
```
worker: python app.py
```

### `runtime.txt`
```
python-3.12.8
```

### `requirements.txt`
```
aiogram==3.4.1
environs==11.0.0
reportlab==4.2.5
```

## ❌ 12. Troubleshooting

### Bot ishlamayapti

```bash
# Loglarni ko'ring
heroku logs --tail

# Worker dyno yoqilganini tekshiring
heroku ps

# Worker dyno'ni scale qiling
heroku ps:scale worker=1
```

### Config xatosi

```bash
# Config'larni tekshiring
heroku config

# Config qo'shish/o'zgartirish
heroku config:set BOT_TOKEN=new_token
```

### Build failed

```bash
# Buildpack'ni tekshiring
heroku buildpacks

# Python buildpack qo'shish
heroku buildpacks:set heroku/python
```

### Database xatosi (SQLite)

Heroku'da SQLite ishlamaydi (ephemeral filesystem). PostgreSQL'ga o'tish kerak:

```bash
heroku addons:create heroku-postgresql:essential-0
```

## 💰 13. Pricing

- **Free tier:** Yo'q (2022'dan beri)
- **Eco Dyno:** $5/oy (1000 soat)
- **Basic Dyno:** $7/oy (unlimited)
- **Standard Dyno:** $25/oy (advanced features)

**Tavsiya:** VPS (DigitalOcean $4/oy) yoki Docker containerlar arzonroq bo'lishi mumkin.

## 🔧 14. Heroku Alternatives

Agar Heroku qimmat bo'lsa:

### Railway.app
- $5/oy
- PostgreSQL bepul
- Deploy oson

### Render.com
- Free tier mavjud
- PostgreSQL bepul
- Docker support

### DigitalOcean App Platform
- $5/oy
- Managed PostgreSQL
- Docker support

### VPS (Tavsiya!)
- DigitalOcean: $4/oy
- Linode: $5/oy
- Vultr: $3.5/oy
- To'liq nazorat + Docker

## 🎯 15. Quick Deploy Commands

```bash
# 1. Login
heroku login

# 2. App yaratish
heroku create

# 3. Config sozlash
heroku config:set BOT_TOKEN=your_token
heroku config:set ADMINS=123456789

# 4. Deploy
git push heroku main

# 5. Worker yoqish
heroku ps:scale worker=1

# 6. Loglar
heroku logs --tail
```

## 📚 16. Foydali Linklar

- Heroku Docs: https://devcenter.heroku.com/
- Python Support: https://devcenter.heroku.com/articles/python-support
- Procfile: https://devcenter.heroku.com/articles/procfile
- Config Vars: https://devcenter.heroku.com/articles/config-vars

## ⚠️ 17. Muhim Eslatmalar

1. **SQLite Muammosi:** Heroku SQLite'ni to'liq support qilmaydi. PostgreSQL ishlatish kerak.
2. **Worker Dyno:** Web emas, worker dyno ishlatish kerak (`Procfile`da).
3. **Pricing:** Free tier yo'q, kamida $5/oy to'lash kerak.
4. **Alternative:** VPS + Docker yaxshiroq variant bo'lishi mumkin.

---

**Savol:** Agar SQLite kerak bo'lsa, VPS + Docker ishlatishni tavsiya qilamiz ([DEPLOYMENT.md](DEPLOYMENT.md) qarang).
