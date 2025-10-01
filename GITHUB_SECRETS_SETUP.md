# 🔐 GitHub Secrets Sozlash Qo'llanmasi

GitHub Actions orqali serverga avtomatik deploy qilish uchun secretlarni sozlash kerak.

## 📝 1. Server Ma'lumotlarini Tayyorlash

### Server'da SSH Key Yaratish

```bash
# Server'ga SSH orqali kiring
ssh your_user@your_server_ip

# SSH key yaratish
ssh-keygen -t ed25519 -C "github-actions-deploy"

# Enter so'raganda hammasi uchun Enter bosing (default)
```

### Private Key'ni Olish

```bash
# Private key'ni ko'ring va nusxalang
cat ~/.ssh/id_ed25519
```

Private key quyidagicha ko'rinadi:
```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
...
(ko'p qatorlar)
...
-----END OPENSSH PRIVATE KEY-----
```

**Muhim:** Butun matnni `-----BEGIN` dan `-----END` gacha nusxalang!

### Public Key'ni Authorized Keys'ga Qo'shish

```bash
# Public key'ni authorized_keys'ga qo'shish
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys

# Permissions'ni to'g'rilash
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

## 🔑 2. GitHub Secrets Qo'shish

### GitHub Repository'ga O'tish

1. GitHub'da repository'ngizni oching
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret** tugmasini bosing

### Kerakli Secretlar

Quyidagi secretlarni **bittadan** qo'shing:

#### SECRET #1: `SERVER_HOST`
- **Name:** `SERVER_HOST`
- **Value:** Server IP manzilingiz
- **Misol:** `123.45.67.89`

#### SECRET #2: `SERVER_USER`
- **Name:** `SERVER_USER`
- **Value:** SSH username
- **Misol:** `ubuntu` yoki `root`

#### SECRET #3: `SSH_PRIVATE_KEY`
- **Name:** `SSH_PRIVATE_KEY`
- **Value:** Yuqorida nusxalgan private key (butun matn!)
- **Misol:**
```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAA...
...butun key...
-----END OPENSSH PRIVATE KEY-----
```

#### SECRET #4: `PROJECT_PATH` (ixtiyoriy)
- **Name:** `PROJECT_PATH`
- **Value:** Server'dagi loyiha yo'li
- **Default:** `~/telegram-bot`
- **Misol:** `/home/ubuntu/telegram-bot` yoki `~/my-bot`

#### SECRET #5: `SERVER_PORT` (ixtiyoriy)
- **Name:** `SERVER_PORT`
- **Value:** SSH port
- **Default:** `22`
- **Misol:** `2222` (agar standart emas bo'lsa)

## ✅ 3. Tekshirish

### Secretlar To'g'ri Kiritilganini Tekshirish

GitHub'da:
1. **Settings** → **Secrets and variables** → **Actions**
2. Quyidagi secretlar ko'rinishi kerak:
   - ✅ `SERVER_HOST`
   - ✅ `SERVER_USER`
   - ✅ `SSH_PRIVATE_KEY`
   - ✅ `PROJECT_PATH` (agar qo'shgan bo'lsangiz)
   - ✅ `SERVER_PORT` (agar qo'shgan bo'lsangiz)

### Server'da Loyiha Tayyorlash

```bash
# Server'ga kiring
ssh your_user@your_server_ip

# Docker o'rnatilganini tekshiring
docker --version
docker compose version

# Loyihani clone qiling
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git telegram-bot
cd telegram-bot

# .env faylini sozlang
cp .env.example .env
nano .env

# BOT_TOKEN va ADMINS'ni kiriting
```

## 🚀 4. Deploy Qilish

### Manual Deploy (Qo'lda)

1. GitHub'da repository'ngizga kiring
2. **Actions** tab'ini oching
3. **Deploy to Server** workflow'ni tanlang
4. **Run workflow** tugmasini bosing
5. **Run workflow** (yashil tugma)ni bosing

### Deploy Jarayonini Kuzatish

1. **Actions** → **Deploy to Server** → Eng oxirgi run
2. Har bir step'ni ochib ko'ring:
   - ✅ Checkout code
   - ✅ Deploy to server via SSH
   - ✅ Notify deployment status

### Deploy Muvaffaqiyatli Bo'ldi

Agar hammasi to'g'ri bo'lsa:
```
✅ Deployment successful!
```

## ❌ 5. Muammolarni Hal Qilish

### Error: missing server host

**Sabab:** `SERVER_HOST` secret qo'shilmagan

**Yechim:**
1. Settings → Secrets → Actions
2. `SERVER_HOST` secretni qo'shing
3. Qayta deploy qiling

### Error: Permission denied (publickey)

**Sabab:** Private key noto'g'ri yoki public key authorized_keys'da yo'q

**Yechim:**
1. Server'da: `cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys`
2. GitHub'da: `SSH_PRIVATE_KEY` secretni qaytadan qo'shing (butun key!)
3. Qayta deploy qiling

### Error: Could not resolve hostname

**Sabab:** Server IP manzili noto'g'ri

**Yechim:**
1. Server IP'ni tekshiring: `curl ifconfig.me`
2. `SERVER_HOST` secretni to'g'rilang
3. Qayta deploy qiling

### Error: Connection refused

**Sabab:** SSH port yopiq yoki firewall bloklayapti

**Yechim:**
```bash
# Server'da
sudo ufw allow 22/tcp
sudo systemctl restart ssh

# Tekshiring
ssh -v your_user@your_server_ip
```

### Error: docker: command not found

**Sabab:** Docker o'rnatilmagan

**Yechim:**
```bash
# Server'da Docker o'rnatish
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

## 📱 6. Test Deploy

Deploy to'g'ri ishlashini tekshirish:

```bash
# Local'da
git add .
git commit -m "Test deploy"
git push origin main

# GitHub Actions'da workflow'ni manual run qiling
# Actions → Deploy to Server → Run workflow

# Server'da tekshiring
ssh your_user@your_server_ip
cd ~/telegram-bot
docker compose ps
docker compose logs bot
```

## 🎯 7. Yakuniy Checklist

- [ ] SSH key yaratildi
- [ ] Public key authorized_keys'ga qo'shildi
- [ ] GitHub'da 3 ta asosiy secret qo'shildi (HOST, USER, KEY)
- [ ] Server'da Docker o'rnatildi
- [ ] Loyiha clone qilindi
- [ ] .env fayl sozlandi
- [ ] Manual deploy test qilindi
- [ ] Bot ishlayapti

## 🔄 8. Avtomatik Deploy (Ixtiyoriy)

Agar har safar push qilganda avtomatik deploy qilmoqchi bo'lsangiz:

`.github/workflows/deploy.yml` faylida:

```yaml
on:
  push:
    branches:
      - main
  workflow_dispatch:
```

**Tavsiya:** Production'da manual deploy ishlatish yaxshiroq.

## 💡 Foydali Commandlar

```bash
# Bot loglarini ko'rish
docker compose logs -f bot

# Bot'ni restart qilish
docker compose restart bot

# Bot'ni to'xtatish
docker compose down

# Bot'ni ishga tushirish
docker compose up -d

# Database backup
cp data/test_bot.db backup/backup_$(date +%Y%m%d).db
```

---

**Savol bo'lsa:** DEPLOYMENT.md fayliga qarang yoki GitHub Issues'da savol bering.
