import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

# --- Yapılandırma ---
duration = 5  # Kayıt süresi (saniye)
sample_rate = 44100  # Ses kalitesi (Örnekleme hızı)

# --- 1. Adım: Ses Kaydı ---
print("🎙 Şimdi konuşun...")

# Mikrofon girişini dinler ve sayısal veri (array) olarak kaydeder
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")

# Belirlenen süre (duration) dolana kadar kodun devam etmesini bekler
sd.wait()

# Kaydedilen veriyi geçici bir ses dosyası (.wav) olarak diske kaydeder
wav.write("output.wav", sample_rate, recording)
print("✅ Kayıt tamamlandı, şimdi tanıma işlemi devam ediyor...")

# --- 2. Adım: Sesi Metne Dönüştürme (STT) ---
recognizer = sr.Recognizer()

# Kaydettiğimiz dosyayı işlem için açıyoruz
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source) # Dosyadaki ses verisini okur

try:
    # Google Speech Recognition servisini kullanarak sesi Türkçe (tr) metne çevirir
    text = recognizer.recognize_google(audio, language="tr")
    print("📝 Şunu söylediniz:", text)

    # --- 3. Adım: Metni Çevirme (Translation) ---
    translator = Translator()
    
    # Tanınan metni İspanyolca'ya (es) çevirir (dest="en" yaparsan İngilizce olur)
    translated = translator.translate(text, dest="es") 
    print("🌍 İspanyolca'ya çeviri:", translated.text)

# Hata Yönetimi
except sr.UnknownValueError:
    # Ses anlaşılamazsa veya ortam çok gürültülüyse
    print("😕 Konuşma tanınamadı.")
except sr.RequestError as e:
    # İnternet bağlantısı yoksa veya Google servislerine erişilemiyorsa
    print(f"❗ Hizmet hatası: {e}")
