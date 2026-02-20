import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr

# --- Ayarlar ---
duration = 5  # Kayıt süresi (saniye)
sample_rate = 44100  # Ses kalitesi (Örnekleme hızı)

# --- Ses Kaydı Aşaması ---
print("Şimdi konuşun...")

# Mikrofondan sesi dizi (array) formatında kaydeder
# channels=1: Mono kayıt yapar, dtype="int16": Standart ses formatıdır
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")

# Kayıt bitene kadar programı bekletir
sd.wait()

# Kaydedilen veriyi fiziksel bir .wav dosyasına yazar
wav.write("output.wav", sample_rate, recording)
print("Kayıt tamamlandı, şimdi tanıma işlemi devam ediyor...")

# --- Ses Tanıma (Speech Recognition) Aşaması ---
recognizer = sr.Recognizer()

# Az önce oluşturduğumuz dosyayı okuyoruz
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source) # Dosyadaki ses verisini yakalar

try:
    # Google Ses Tanıma servisini kullanarak sesi Türkçe metne çevirir
    text = recognizer.recognize_google(audio, language="tr")
    print("Şunu söylediniz:", text)

except sr.UnknownValueError:
    # Eğer ses çok bozuksa veya konuşma yoksa bu hata döner
    print("Konuşma tanınamadı.")

except sr.RequestError as e:
    # İnternet bağlantısı veya API erişim sorunlarında bu hata döner
    print(f"Hizmet hatası: {e}")
