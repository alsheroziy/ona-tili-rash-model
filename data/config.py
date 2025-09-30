from environs import Env

env = Env()
env.read_env()

missing = []

BOT_TOKEN = env.str("BOT_TOKEN") if env("BOT_TOKEN", None) else None
if BOT_TOKEN is None:
	missing.append("BOT_TOKEN")

ADMINS = env.list("ADMINS") if env("ADMINS", None) else []
if not ADMINS:
	# Not critical, but warn later (see README)
	pass

IP = env.str("ip", "localhost")

# Database
DB_NAME = "test_bot.db"

if missing:
	raise RuntimeError(
		"Quyidagi environment o'zgaruvchilar topilmadi (yo" "ki .env faylida yo'q): " + ", ".join(missing)
	)
