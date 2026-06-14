import serial
import mysql.connector
import time

# Isi dengan data dari Clever Cloud
db = mysql.connector.connect(
    host="bseedukya7gi08pqaq0z-mysql.services.clever-cloud.com",
    user="uwddtw93oxttkgox",
    passwd="2FzfDbzE17Nj8lLzH0zW",
    database="bseedukya7gi08pqaq0z",
    port=3306
)
cursor = db.cursor()

# Ganti 'COM4' sesuai port ESP8266 Anda di Device Manager
ser = serial.Serial(port='COM7', baudrate=115200, timeout=1)

print("Bridge berjalan, menunggu data dari ESP...")

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if "Data dari" in line:
            id_tiang = int(line.split("Tiang ")[1])
            cahaya = int(ser.readline().decode().split(": ")[1])
            status = ser.readline().decode().split(": ")[1].strip()
            
            cursor.execute("INSERT INTO tbl_monitoring (id_tiang, nilai_cahaya, status_lampu) VALUES (%s, %s, %s)", 
                           (id_tiang, cahaya, status))
            db.commit()
            print(f"Data Masuk: {status}")