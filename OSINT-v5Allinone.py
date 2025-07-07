OSINT V5 - No API, All-in-One

Fitur: Deteksi Nama, Email, HLR, WA Check, Sosial Media, Marketplace, Maps

import requests, re, urllib.parse, time from bs4 import BeautifulSoup

Konfigurasi Telegram

TOKEN = "7275073146:AAGlJkPAhdhhmRLU5CiLF3nFSeeTWjZV_ic" CHAT_ID = "21304444"

Format nomor

def format_nomor(n): n = n.strip().replace(" ", "").replace("-", "") if n.startswith("0"): return "+62" + n[1:] if n.startswith("62"): return "+" + n return n if n.startswith("+") else "+" + n

HLR Lookup

def hlr_lookup(n): try: url = f"https://www.ceebydith.com/operator/cek-hlr-lokasi-hp.php?nomor={n}" r = requests.get(url) s = BeautifulSoup(r.text, "html.parser") hasil = s.find("tr", class_="table-content") if hasil: teks = hasil.text.strip() match = re.search(r'Kota\s*:\s*(.*)', teks) kota = match.group(1) if match else "-" maps = f"https://www.google.com/maps/search/{urllib.parse.quote(kota)}" if kota != "-" else "-" return teks, maps else: return "-", "-" except: return "(Error HLR)", "-"

Google Search untuk nama dan email

def google_info(n): try: q = urllib.parse.quote(n) r = requests.get(f"https://www.google.com/search?q={q}", headers={"User-Agent": "Mozilla/5.0"}) soup = BeautifulSoup(r.text, "html.parser") text = soup.get_text() nama = re.findall(r'([A-Z][a-z]+\s[A-Z][a-z]+)', text) email = re.findall(r'[\w.-]+@[\w.-]+', text) return (nama[0] if nama else "-", list(set(email))[:3] if email else ["-"]) except: return ("(Error Nama)", ["(Error Email)"])

WhatsApp Check

def wa_check(n): try: url = f"https://wa.me/{n.replace('+','')}" r = requests.get(url, allow_redirects=True) return "Aktif" if "whatsapp" in r.url else "Tidak Aktif" except: return "(Error WA)"

Telegram, Facebook, Instagram

def social_check(n): user = n.replace('+','') hasil = [] if requests.get(f"https://t.me/{user}").status_code == 200: hasil.append("Telegram") if "facebook" in requests.get(f"https://www.facebook.com/search/top?q={user}").url: hasil.append("Facebook") if requests.get(f"https://www.instagram.com/{user}/").status_code == 200: hasil.append("Instagram") return hasil if hasil else ["-"]

Cek di OLX

def cek_olx(n): try: url = f"https://www.olx.co.id/items/q-{n}" r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}) if n in r.text: lokasi_match = re.search(r'"location"\s*:\s*"([^"]+)"', r.text) lokasi = lokasi_match.group(1) if lokasi_match else "Ditemukan (lokasi tidak spesifik)" maps = f"https://www.google.com/maps/search/{urllib.parse.quote(lokasi)}" return f"Ada ({lokasi})", maps else: return "Tidak Ada", "-" except: return "(Error OLX)", "-"

Cek di Tokopedia

def cek_tokopedia(n): try: url = f"https://www.tokopedia.com/search?st=product&q={n}" r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}) return "Ada" if n in r.text else "Tidak Ada" except: return "(Error Tokopedia)"

Cek di Shopee

def cek_shopee(n): try: url = f"https://shopee.co.id/search?keyword={n}" r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}) return "Ada" if n in r.text else "Tidak Ada" except: return "(Error Shopee)"

Kirim Telegram

def kirim_telegram(pesan): try: url = f"https://api.telegram.org/bot{TOKEN}/sendMessage" data = {"chat_id": CHAT_ID, "text": pesan} requests.post(url, data=data) except: print("Gagal kirim Telegram")

Proses satu nomor

def proses(n): n = format_nomor(n) nama, email = google_info(n) hlr, map_link = hlr_lookup(n) wa = wa_check(n) sosmed = social_check(n) olx, olx_map = cek_olx(n) tokopedia = cek_tokopedia(n) shopee = cek_shopee(n)

out = f"""

📞 Nomor: {n} 👤 Nama: {nama} 📧 Email: {' | '.join(email)} 📍 HLR Lokasi: {hlr} 🗺️ Maps HLR: {map_link} 💬 WhatsApp: {wa} 👥 Sosial Media: {' | '.join(sosmed)} 🛒 OLX: {olx} 🗺️ Maps OLX: {olx_map} 🏪 Tokopedia: {tokopedia} 🛍️ Shopee: {shopee} """ print(out) kirim_telegram(out)

Main multi-scan

def main(): try: with open("target.txt") as f: for nomor in f.read().splitlines(): if nomor.strip(): proses(nomor) time.sleep(3) except: print("Gagal membuka target.txt")

if name == 'main': main()

