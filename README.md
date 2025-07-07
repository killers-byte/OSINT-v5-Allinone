1. Install Git

apt install git -y

2. Konfigurasi Git

git config --global user.name "namamu"
git config --global user.email "emailmu@domain.com"


1. Clone repository GitHub kamu ke Ubuntu:

Ganti USERNAME dan REPO sesuai kamu:

git clone https://github.com/USERNAME/osint-v5-allinone.git
cd osint-v5-allinone

2. Salin file script ke dalam folder:

Misalnya script kamu bernama osint_v5_allinone.py dan target.txt, maka:

cp ~/osint_v5_allinone.py .
cp ~/target.txt .

3. Tambahkan dan commit file:

git add .
git commit -m "Upload OSINT V5 script awal"

4. Push ke GitHub:

git push origin main


💡 Hasil Akhir
