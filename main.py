import asyncio
import os
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Render'ın ücretsiz web servisini ayakta tutmak için mini web sunucusu
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

  # 1. ÖZEL MESAJLAR (Biri yazdığı an tam 5 saniye sonra yanıt verir)
  @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
  async def dm_reply(event):
    if event.out:
      return
    try:
      await asyncio.sleep(5)  # Tam istediğin gibi 5 saniye bekleyip atar
      await event.respond(OTO_YANIT_METNI)
      print("[DM] Özelden yazan kişiye 5 saniye sonra yanıt gönderildi.")
    except Exception as e:
      print(f"[DM HATA]: {e}")

  # 2. GRUPLAR (Tam 30 saniyede bir toplu reklam atar)
  async def periodic_poster():
    while True:
      await asyncio.sleep(30)  # Tam 30 saniye bekle
      print("--- 30 saniye doldu, gruplara toplu reklam gönderiliyor ---")
      for grup in HEDEF_GRUPLAR:
        try:
          entity = await client.get_entity(grup)
          await client.send_message(entity, GRUP_REKLAM_METNI)
          print(f"[GRUP BAŞARILI] {grup}")
          await asyncio.sleep(0.5)  # Çok hızlı yığılıp ban yememek için mini mola
        except Exception as e:
          print(f"[GRUP HATA] {grup}: {e}")
      print("--- Gruplar döngüsü bitti, sonraki 30 saniye bekleniyor ---")

  client.loop.create_task(periodic_poster())
  await client.run_until_disconnected()


if __name__ == "__main__":
  import threading

  t = threading.Thread(target=run_web)
  t.start()
  asyncio.run(main())
