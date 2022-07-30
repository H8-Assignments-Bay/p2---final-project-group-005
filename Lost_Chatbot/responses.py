from datetime import datetime

def sample_responses(input_text):
    user_message = str(input_text).lower()
    
# Silahkan tambahkan pada bagian ini 
    if user_message in ("Hai", "Hi", "Halo", "Apa Kabar", "Selamat Pagi", "Selamat Siang", "Selamat Malam", "Salam", "Ping", "P", "siang", "malam", "pagi", "helo", "hola"):
        return ("Halo!", "Hai", "Halo, ada yang bisa GoBot bantu?", "Halo selamat datang", "Hai Kawan Gobot")

    if user_message in ("Dadah", "Selamat Tinggal", "Dah", "Daah", "Semoga harimu menyenangkan", "Ok makasih", "Sampai Jumpa Lagi", "Ok bye"):
        return ("Sampai jumpa lagi kawan GoBot", "Kalau butuh bantuan, hubungi GoBot lagi ya", "Semoga harimu menyenangkan!", "Sampai jumpa, terima kasih telah bertanya!")

    if user_message in ("Thanks", "Thank you", "Terimakasih", "Makasih", "Nuhun"):
        return ("Sama-sama, senang GoBot bisa membantu anda!")
    
    if user_message in ("nama kamu siapa?", "lu siapa?", "siapa sih lo?", "lu sape ?", "nama lo sape dah ?", "nama?"):
        return ("Hi! Namaku GoBot, salam kenal kawan!", "Halo, aku GoBot!", "Kenalin, aku GoBot!")

    if user_message in ("kamu siapa?", "siapa sih kamu?" , "gobot apa?", "apa itu gobot?"):
        return ("GoBot merupakan online Chatbot, yang dapat membantu kawan untuk mecarikan rekomendasi tempat kawan liburan.", "Tugasku jadi asisten di komunitas NgodingPython")

    if user_message in ("emang Let's Get Lost apa si?", "apa tuh Let's Get Lost?", "eman ini apasih?", "wah apa tuh ini?", "Let's Get Lost apaan?"):
        return ("Let's Get Lost ada sebuah aplikasi yang membantu kawan untuk mendapatkan rekomendasi liburan berdasarkan kriteria kamu")

    if user_message in ("Bisakah Anda memberikan link Let's Get Lost?", "Minta link nya dong", "Website nya apa", "Tolong berikan saya link!", "Bagi link", "link apps nya apa?", "link apps?"):
        return ("Baik, GoBot akan memberikan link nya, silahkan klik dari tautan ini:____________")

    if user_message in ("siapa pembuat Let's Get Lost?", "siapa pembuat apps ini?", "siapa yang buat?", "siapa pencipta Let's Get Lost", "apps nya siapa yang bikin", "Let's Get Lost siapa yang bikin?"):
        return ("Let's Get Lost diciptakan oleh Fadhli, Nirwan & Sanzabi")

    if user_message in ("main yuk", "jalan yuk", "kuy yuk", "kuy bot", "gaskan yuk"):
        return ("Yuk, biar GoBot temenin kawan!")

    if user_message in ("gobot sukanya pergi kemana?", "gobot suka liburan kemana?", "bot kemarin liburan kemana?", "gobot pernah liburan?"):
        return ("GoBot gabisa pergi liburan, karena aku hanyalah Artificial Inteligence, tapi aku bisa menemani kawan untuk memberikan rekomendasi liburan")

    if user_message in ("Ada pilihan liburan kemana saja bot?", "bisa liburan kemana aja nih?", "rekomendasi liburan bali?"):
        return ("Saat ini GoBot hanya dapat memberikan rekomendasi liburan di Labuan Bajo saja.")

    if user_message in ("ada hotel apa aja bot?", "carikan hotel terbaik", "ada yang murah ga?", "apa hotelnya bagus?"):
        return ("GoBot akan memberikan rekomendasi hotel terbaik untuk kawan.", "Pilihan hotel terbaik selalu GoBot berikan")

    if user_message in ("uang ku pas-pasan", "uangku sedikit", "apakah ada liburan yang cocok untuk saya?", "liburan yang cocok untuk saya?"):
        return ("Tenang, GoBot akan memberikan rekomendasi hotel, restoran dan hal menarik lainnya sesuai budget kawan.")

    if user_message in ("time", "jam?", "jamber", "jamberapa sekarang?" "jam berapa?"):
        return ("Sekarang jam " + str(datetime.now().strftime("%H:%M:%S")))

    if user_message in ("date", "tanggal?", "tanggal berapa?"):
        return ("Sekarang tanggal " + str(datetime.now().strftime("%d/%m/%Y")))

    if user_message in ("hari ini", "hari apa?", "hari berapa?"):
        return ("Hari ini hari " + str(datetime.now().strftime("%A")))


    return "GoBot tidak mengerti apa yang kamu katakan :("
























