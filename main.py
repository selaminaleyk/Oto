import asyncio
import os
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Render'ın ücretsiz web servisini aktif tutmak için mini web sunucusu
app = Flask('')


@app.route('/')
def home():
  return "Bot 7/24 Aktif ve Çalışıyor!"


def run_web():
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


# Telegram API Bilgileri
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
SESSION_STRING = os.environ.get("SESSION_STRING", "")

GRUP_REKLAM_METNI = "ücretsiz karımı izletiyorum"

OTO_YANIT_METNI = """🔥 81 İLDEN TÜRKİYE'NİN DÖRT BİR YANINDAN KIZLARIN VE GENCIN OLDUĞU EN BÜYÜK SOHBET GRUBUMUZ AKTİF! 🔥

🚨 DİKKAT: Gruba katılım tamamen ücretsizdir ancak yoğunluk ve güvenlik nedeniyle herkesin aşağıdaki ana gruba katılması ZORUNLUDUR!

👉 ANA SOHBET GRUBUMUZ: @trarayisda 
(Katılmayanların bot erişimi otomatik olarak engellenir!)

🔞 Aradığınız 100 Tane Ünlü İfşa, Özel Arşivler ve VIP Medya Dosyaları Sadece Bu Botun İçinde!

🎁 Arşivi ve linkleri anında açmak için:
1️⃣ Önce yukarıdaki @trarayisda grubuna katılın.
2️⃣ Aşağıdaki "ARŞİVİ AÇ / BAĞLANTIYI GÖSTER" butonuna basın!"""

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
  client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
  await client.start()
  print("Userbot başarıyla aktif edildi ve 7/24 çalışıyor!")

  # 1. ÖZEL MESAJLAR (Flood korumalı ve garantili DM yakalayıcı)
  @client.on(events.NewMessage(incoming=True))
  async def auto_reply(event):
    if event.is_private and not event.out:
      try:
        # Karşı tarafa insan gibi görünmek ve engellenmemek için yarım saniye bekleme
        await asyncio.sleep(0.5)
        await event.respond(OTO_YANIT_METNI)
        print(f"Özelden yazan kişiye yanıt gönderildi.")
      except Exception as e:
        print(f"Özel mesaja yanıt verilemedi: {e}")

  # 2. GRUPLAR (2 dakikada bir tetiklenir, Telegram filtresine takılmamak için araya mini bekleme ekler)
  async def periodic_poster():
    while True:
      await asyncio.sleep(120)  # Tam 2 dakika bekle
      print("2 dakika doldu, gruplara gönderim başlatılıyor...")
      for grup in HEDEF_GRUPLAR:
        try:
          await client.send_message(grup, GRUP_REKLAM_METNI)
          print(f"{grup} grubuna mesaj iletildi.")
          # Telegram'ın spam filtresine takılmamak için gruplar arası 1.5 saniye mola
          await asyncio.sleep(1.5)
        except Exception as e:
          print(f"{grup} grubuna mesaj gönderilemedi: {e}")
      print("Tüm gruplara döngü tamamlandı.")

  client.loop.create_task(periodic_poster())
  await client.run_until_disconnected()


if __name__ == "__main__":
  import threading

  # Web sunucusunu arka planda başlat
  t = threading.Thread(target=run_web)
  t.start()

  # Telegram botunu başlat
  asyncio.run(main())
