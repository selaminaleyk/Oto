import asyncio
import os
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Hugging Face / Fly.io için mini web sunucusu (Port ayarı için)
app = Flask('')


@app.route('/')
def home():
  return "Bot 7/24 Aktif ve Çalışıyor!"


def run_web():
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)


# Telegram API Bilgileri (Fly.io Secrets üzerinden okunur)
API_ID = int(os.environ.get('API_ID', 2040))
API_HASH = os.environ.get('API_HASH', "b18441a1ff607e10a989891a5462e627")
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


async def periodic_group_poster(client):
  """Her 50 saniyede bir hedef gruplara reklam atar. Banlı/hata verenleri atlar."""
  while True:
    await asyncio.sleep(50)  # Tam 50 saniye bekle
    print("--- 50 saniye doldu, gruplara toplu gönderim başlatılıyor ---")
    for grup in HEDEF_GRUPLAR:
      try:
        await client.send_message(grup, GRUP_REKLAM_METNI)
        print(f"[GRUP BAŞARILI] {grup} adresine reklam gönderildi.")
        await asyncio.sleep(0.5)  # Flood koruması
      except Exception as e:
        print(f"[GRUP HATA ATLANDI] {grup}: {e}")
    print("--- Toplu gönderim tamamlandı, sonraki 50 saniye bekleniyor ---")


async def main():
  if not SESSION_STRING:
    print("[HATA] SESSION_STRING environment değişkeni tanımlı değil!")
    return

  client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

  # DM Dinleyicisi (Özelden yazanlara anında yanıt)
  @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
  async def instant_dm_reply(event):
    if event.out:
      return
    try:
      await event.respond(OTO_YANIT_METNI)
      print(f"[ANINDA DM] Özelden yazan kullanıcıya yanıt gönderildi.")
    except Exception as e:
      print(f"[DM HATA]: {e}")

  print("Fly.io üzerinde Userbot başlatılıyor...")
  await client.start()
  print("Userbot başarıyla aktif edildi ve 7/24 çalışıyor!")

  # Toplu reklam döngüsünü başlat
  asyncio.create_task(periodic_group_poster(client))

  await client.run_until_disconnected()


if __name__ == "__main__":
  import threading

  # Web sunucusunu arka planda (thread içinde) başlat
  t = threading.Thread(target=run_web)
  t.start()

  # Asıl Telegram botunu çalıştır
  asyncio.run(main())
