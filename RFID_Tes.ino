#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN  5
#define RST_PIN 22

MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(115200);

  // SPI ESP32
  SPI.begin(18, 19, 23, 5);

  // Inisialisasi RFID
  rfid.PCD_Init();

  delay(100);

  // Header CSV
  Serial.println("Waktu_ms,UID,UID_Size,Tipe_Kartu");
}

void loop() {

  // Tidak ada kartu baru
  if (!rfid.PICC_IsNewCardPresent()) {
    return;
  }

  // Gagal membaca kartu
  if (!rfid.PICC_ReadCardSerial()) {
    return;
  }

  // Membuat UID menjadi satu teks
  String uidString = "";

  for (byte i = 0; i < rfid.uid.size; i++) {

    if (i > 0) {
      uidString += ":";
    }

    if (rfid.uid.uidByte[i] < 0x10) {
      uidString += "0";
    }

    uidString += String(rfid.uid.uidByte[i], HEX);
  }

  uidString.toUpperCase();

  // Membaca tipe kartu
  MFRC522::PICC_Type piccType =
    rfid.PICC_GetType(rfid.uid.sak);

  String tipeKartu =
    rfid.PICC_GetTypeName(piccType);

  // ==============================
  // OUTPUT DATA CSV
  // ==============================

  Serial.print(millis());
  Serial.print(",");

  Serial.print(uidString);
  Serial.print(",");

  Serial.print(rfid.uid.size);
  Serial.print(",");

  Serial.println(tipeKartu);

  // Menghentikan komunikasi dengan kartu
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();

  // Jeda agar satu kartu tidak terbaca berkali-kali
  delay(1000);
}