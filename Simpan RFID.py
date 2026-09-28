import serial
import csv
import os

PORT = "COM5"
BAUDRATE = 115200

# Folder penyimpanan hasil RFID
folder_hasil = r"D:\03_SURYA\SMT 7\Capstone\Hasil RFID"

# Membuat folder jika belum ada
os.makedirs(folder_hasil, exist_ok=True)

# Nama file hasil
nama_file = os.path.join(
    folder_hasil,
    "hasil_RFID.csv"
)

print("================================")
print("       PEREKAMAN RFID ESP32")
print("================================")
print("Menghubungkan ke ESP32...")

try:
    ser = serial.Serial(
        PORT,
        BAUDRATE,
        timeout=1
    )

    print("ESP32 berhasil terhubung!")
    print("Port      :", PORT)
    print("Baud rate :", BAUDRATE)
    print("File      :", nama_file)
    print()
    print("Tempelkan kartu RFID.")
    print("Tekan Ctrl+C untuk berhenti.")
    print()

except serial.SerialException as e:
    print("Gagal membuka port", PORT)
    print()
    print("Periksa:")
    print("1. ESP32 sudah terhubung")
    print("2. Nomor COM sudah benar")
    print("3. Serial Monitor Arduino IDE sudah ditutup")
    print()
    print("Error:", e)
    exit()


with open(
    nama_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    # Header CSV
    writer.writerow([
        "Waktu_ms",
        "UID",
        "UID_Size",
        "Tipe_Kartu"
    ])

    try:

        while True:

            data = ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if not data:
                continue

            print(data)

            # Abaikan header dari ESP32
            if data.startswith("Waktu_ms"):
                continue

            # Memisahkan data berdasarkan koma
            bagian = data.split(",")

            # Memastikan data terdiri dari 4 kolom
            if len(bagian) == 4:

                writer.writerow(bagian)

                # Menyimpan langsung ke file
                file.flush()

    except KeyboardInterrupt:

        print()
        print("================================")
        print("Perekaman dihentikan.")
        print("================================")


ser.close()

print()
print("File berhasil disimpan di:")
print(nama_file)