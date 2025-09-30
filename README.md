# Online Test Bot (Aiogram v3)

Bu loyiha **aiogram v3** asosida yaratilgan online test o'tkazish boti.

## Xususiyatlar

### Foydalanuvchilar uchun:
- Ro'yxatdan o'tish (ism-familya, telefon raqam)
- Testlarni tanlash va topshirish
- Natijalarni ko'rish

### Adminlar uchun:
- Test yaratish
- Test javoblarini kiritish
- Testlar ro'yxatini ko'rish

### Test tuzilishi:
- 1-32 savollar: A, B, C, D variantli (har biri 1 ball)
- 33-35 savollar: A, B, C, D, E, F variantli (har biri 1 ball)
- 36-39 savollar: Yozma javob (har biri 2 ball)
- 40-44 savollar: A va B qismli (har biri 3 ball: A=1.5, B=1.5)

## O'rnatish

1. Reponi klon qiling:
```bash
git clone <repo-url>
cd mukammal-bot-paid-master
```

2. Virtual muhit yarating:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Kutubxonalarni o'rnating:
```bash
pip install -r requirements.txt
```

4. `.env` fayl yarating:
```
BOT_TOKEN=your_bot_token_here
ADMINS=123456789,987654321
ip=localhost
```

5. Botni ishga tushiring:
```bash
python app.py
```

## Foydalanish

### Oddiy foydalanuvchi:
1. `/start` - Botni boshlash va ro'yxatdan o'tish
2. "📝 Test boshlash" - Test tanlash va topshirish
3. "📊 Natijalarim" - O'z natijalarini ko'rish

### Admin:
1. `/admin` yoki "➕ Test yaratish" - Yangi test yaratish
2. Test nomini kiriting
3. Har bir savol uchun to'g'ri javobni kiriting
4. "📋 Testlar ro'yxati" - Barcha testlarni ko'rish

## Texnologiyalar
- Python 3.9+
- Aiogram 3.4
- SQLite3
- Environs

## Struktura
```
.
├── app.py                 # Asosiy fayl
├── loader.py              # Bot, Dispatcher
├── data/
│   └── config.py          # Konfiguratsiya
├── states/                # FSM state'lar
├── handlers/
│   ├── users/             # Foydalanuvchi handlerlar
│   └── admins/            # Admin handlerlar
├── keyboards/             # Klaviaturalar
├── middlewares/           # Middleware'lar
└── utils/
    └── db_api/            # Ma'lumotlar bazasi
```

## Muammolarni hal qilish

| Muammo | Yechim |
|--------|--------|
| Token xatosi | `.env` fayldagi `BOT_TOKEN` ni tekshiring |
| Admin panel ishlamayapti | `ADMINS` ro'yxatiga o'z ID'ingizni qo'shing |
| Database xatosi | `test_bot.db` faylini o'chirib qayta ishga tushiring |

## Keyingi rivojlantirish
- Webhook rejimi
- Redis storage
- Test statistikasi
- Fayllarni yuklash
- Natijalarni Excel ga eksport qilish

Savollar uchun: [Your Contact]
