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

  # Bot açıldığı an hesapta bekleyen okunmamış özel mesajları otomatik tarayıp yanıtlar
  async def check_unread_dms():
    try:
      async for dialog in client.iter_dialogs():
        if dialog.is_user and dialog.unread_count > 0:
          entity = dialog.entity
          if not entity.bot and not entity.out:
            await client.send_message(entity, OTO_YANIT_METNI)
            print(f"[OKUNMAMIŞ DM] {entity.id} kişisinin okunmamış mesajı yanıtlandı.")
            await asyncio.sleep(0.5)
    except Exception as e:
      print(f"Okunmamış DM tarama hatası: {e}")

  # İlk açılışta okunmamışları kontrol et
  await check_unread_dms()

  # 1. ÖZEL MESAJLAR (Gelen yeni/okunmamış tüm DM'lere saniyesinde direkt cevap verir)
  @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
  async def auto_reply(event):
    if event.out:
      return
    try:
      await event.respond(OTO_YANIT_METNI)
      print("[ANINDA DM] Özelden yazan kişiye anında yanıt gönderildi.")
    except Exception as e:
      print(f"[DM HATA]: {e}")

  # 2. GRUPLAR (Tam 50 saniyede bir bütün gruplara toplu olarak mesaj atar)
  async def periodic_poster():
    while True:
      await asyncio.sleep(50)  # Tam 50 saniye bekle
      print("--- 50 saniye doldu, gruplara toplu gönderim başlatılıyor ---")
      for grup in HEDEF_GRUPLAR:
        try:
          # Gruplara peş peşe toplu şekilde iletir
          entity = await client.get_entity(grup)
          await client.send_message(entity, GRUP_REKLAM_METNI)
          print(f"[GRUP BAŞARILI] {grup} grubuna mesaj iletildi.")
        except Exception as e:
          print(f"[GRUP HATA] {grup} grubuna gönderilemedi: {e}")
      print("--- Tüm gruplara toplu gönderim tamamlandı ---")

  client.loop.create_task(periodic_poster())
  await client.run_until_disconnected()


if __name__ == "__main__":
  import threading

  # Web sunucusunu arka planda başlat (UptimeRobot ile uykuyu önler)
  t = threading.Thread(target=run_web)
  t.start()

  # Telegram botunu başlat
  asyncio.run(main())
  
