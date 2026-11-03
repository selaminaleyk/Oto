import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Telegram'ın resmi açık kaynak test anahtarları
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"

# Render ortam değişkeninden (Environment Variables) aldığımız String Session kodu
SESSION_STRING = os.environ.get("SESSION_STRING", "")

# 1. Gruplara atılacak olan kısa reklam mesajı
GRUP_REKLAM_METNI = "ücretsiz karımı izletiyorum"

# 2. Biri sana özelden yazdığında gidecek uzun oto-mesaj
OTO_YANIT_METNI = """🔥 81 İLDEN TÜRKİYE'NİN DÖRT BİR YANINDAN KIZLARIN VE GENCIN OLDUĞU EN BÜYÜK SOHBET GRUBUMUZ AKTİF! 🔥

🚨 DİKKAT: Gruba katılım tamamen ücretsizdir ancak yoğunluk ve güvenlik nedeniyle herkesin aşağıdaki ana gruba katılması ZORUNLUDUR!

👉 ANA SOHBET GRUBUMUZ: @trarayisda 
(Katılmayanların bot erişimi otomatik olarak engellenir!)

🔞 Aradığınız 100 Tane Ünlü İfşa, Özel Arşivler ve VIP Medya Dosyaları Sadece Bu Botun İçinde!

🎁 Arşivi ve linkleri anında açmak için:
1️⃣ Önce yukarıdaki @trarayisda grubuna katılın.
2️⃣ Aşağıdaki "ARŞİVİ AÇ / BAĞLANTIYI GÖSTER" butonuna basın!"""

# Verdiğin bütün hedef grupların listesi (27 Grup)
HEDEF_GRUPLAR = [
    "@evliciftt31",
    "@arayislocassii",
    "@Bursasohbette",
    "@heraarayis",
    "@TRArayisVip",
    "@trarayis29",
    "@rollarayis4",
    "@kiz_arayis_tr",
    "@arayis10x",
    "@ozel_arayis",
    "@evliciftlernekanisohbet",
    "@cezaevi",
    "@arayislarda",
    "@arayislarinizturkiye",
    "@arayisgruptr",
    "@turkiye_o",
    "@ownerarayisbulma",
    "@arayis_vakti",
    "@kadinarabul",
    "@arayistanis",
    "@arayismuhabbet",
    "@arayis_itiraz",
    "@evliciftler12",
    "@kizarayis34",
    "@Galatasarayt",
    "@atatvl44",
    "@evliciftler_evligizlicift",
]


async def main():
  # String Session ile bulutta doğrudan senin hesabınla oturum açma
  client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
  await client.start()
  print("Userbot başarıyla aktif edildi ve 7/24 çalışıyor!")

  # Biri sana özelden yazarsa hazırladığın uzun oto-mesajı anında gönderir
  @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
  async def auto_reply(event):
    if event.out:
      return
    await event.respond(OTO_YANIT_METNI)

  # Belirli aralıklarla gruplara reklamı atar (Her 3 dakikada bir = 180 saniye)
  async def periodic_poster():
    while True:
      await asyncio.sleep(180)
      for grup in HEDEF_GRUPLAR:
        try:
          await client.send_message(grup, GRUP_REKLAM_METNI)
          print(f"{grup} grubuna mesaj gönderildi.")
          await asyncio.sleep(3)  # Spam koruması için gruplar arası bekleme
        except Exception as e:
          print(f"{grup} grubuna mesaj gönderilemedi: {e}")

  client.loop.create_task(periodic_poster())
  await client.run_until_disconnected()


if __name__ == "__main__":
  asyncio.run(main())
