import customtkinter as ctk
import yt_dlp
import threading
from tkinter import filedialog

# General theme settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SosyalMedyaIndirici(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Universal Video Downloader")
        self.geometry("550x450")
        
        # holding the chosen destination
        self.indirilecek_yer = ""

        # --- GUI ---
        
        # Label
        self.label = ctk.CTkLabel(self, text="Video Downloader", font=("Roboto", 24, "bold"))
        self.label.pack(pady=20)

        # Link Panel
        self.entry = ctk.CTkEntry(self, width=450, placeholder_text="YouTube, Instagram, TikTok veya X linkini yapıştırın...")
        self.entry.pack(pady=10)

        # Choosing the file
        self.sec_btn = ctk.CTkButton(self, text="Kaydedilecek Klasörü Seç", command=self.klasor_sec, fg_color="#4a4a4a", hover_color="#333333")
        self.sec_btn.pack(pady=5)

        self.yol_etiketi = ctk.CTkLabel(self, text="Henüz klasör seçilmedi", font=("Arial", 11), text_color="gray")
        self.yol_etiketi.pack(pady=5)

        # loading bar
        self.progress_bar = ctk.CTkProgressBar(self, width=450)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=25)

        # download button
        self.indir_btn = ctk.CTkButton(self, text="İndirmeyi Başlat", command=self.thread_baslat, font=("Roboto", 16, "bold"), height=40)
        self.indir_btn.pack(pady=10)

        # state message
        self.status_label = ctk.CTkLabel(self, text="Hazır", text_color="white")
        self.status_label.pack(pady=10)

    def klasor_sec(self):
        self.indirilecek_yer = filedialog.askdirectory()
        if self.indirilecek_yer:
            self.yol_etiketi.configure(text=f"Yer: {self.indirilecek_yer}", text_color="white")
        else:
            self.yol_etiketi.configure(text="Klasör seçilmedi!", text_color="red")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                progress_float = float(p) / 100
                self.progress_bar.set(progress_float)
                self.status_label.configure(text=f"İndiriliyor: %{p}", text_color="yellow")
            except:
                pass
        
        if d['status'] == 'finished':
            self.progress_bar.set(1)
            self.status_label.configure(text="İndirme Başarıyla Tamamlandı!", text_color="#2ecc71")

    def thread_baslat(self):
        # Running the task in a background thread
        t = threading.Thread(target=self.indir)
        t.start()

    def indir(self):
        url = self.entry.get()
        
        if not url:
            self.status_label.configure(text="Hata: Lütfen bir link girin!", text_color="#e74c3c")
            return
        
        if not self.indirilecek_yer:
            self.status_label.configure(text="Hata: Lütfen önce kayıt yerini seçin!", text_color="#e74c3c")
            return

        self.status_label.configure(text="Bilgiler alınıyor...", text_color="white")
        
        ydl_opts = {
            'format': 'best', 
            'outtmpl': f'{self.indirilecek_yer}/%(title)s.%(ext)s',
            'progress_hooks': [self.progress_hook],
        
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            self.status_label.configure(text="Hata: Desteklenmeyen link veya bağlantı hatası!", text_color="#e74c3c")

if __name__ == "__main__":
    app = SosyalMedyaIndirici()
    app.mainloop()
