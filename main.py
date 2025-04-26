import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("diary.ui", self)

        self.simpan.clicked.connect(self.simpan_diary)
        self.hapus.clicked.connect(self.hapus_diary)
        self.edit.clicked.connect(self.edit_diary)
        self.daftarDiary.itemDoubleClicked.connect(self.edit_diary)

        # Atur ScrollBar
        self.Diary.setVerticalScrollBar(self.scroll1)
        self.daftarDiary.setVerticalScrollBar(self.scroll2)
        self.daftarDiary.setHorizontalScrollBar(self.scroll3)

        self.load_daftar_diary()

    def simpan_diary(self):
        judul = self.judul.text().strip()
        isi = self.Diary.toPlainText().strip()
        tanggal = self.tanggalCatatan.date().toString("yyyy-MM-dd")

        if not judul or not isi:
            QMessageBox.warning(self, "Peringatan", "Judul dan Diary harus diisi!")
            return

        nama_file = f"{judul}_{tanggal}.txt"
        with open(os.path.join("diary", nama_file), "w", encoding="utf-8") as file:
            file.write(f"{tanggal}\n{judul}\n\n{isi}")

        QMessageBox.information(self, "Berhasil", "Diary berhasil disimpan!")
        self.judul.clear()
        self.Diary.clear()
        self.load_daftar_diary()

    def hapus_diary(self):
        selected = self.daftarDiary.currentItem()
        if not selected:
            QMessageBox.warning(self, "Peringatan", "Pilih file diary yang ingin dihapus!")
            return

        file_path = os.path.join("diary", selected.text())
        if os.path.exists(file_path):
            os.remove(file_path)
            self.load_daftar_diary()
            QMessageBox.information(self, "Berhasil", "Diary berhasil dihapus.")

    def edit_diary(self):
        selected = self.daftarDiary.currentItem()
        if not selected:
            QMessageBox.warning(self, "Peringatan", "Pilih file diary yang ingin diedit!")
            return

        file_path = os.path.join("diary", selected.text())
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                tanggal = lines[0].strip()
                judul = lines[1].strip()
                isi = "".join(lines[3:])

                self.judul.setText(judul)
                self.Diary.setText(isi)
                self.tanggalCatatan.setDate(self.tanggalCatatan.date().fromString(tanggal, "yyyy-MM-dd"))

            os.remove(file_path)
            self.load_daftar_diary()

    def load_daftar_diary(self):
        if not os.path.exists("diary"):
            os.makedirs("diary")

        self.daftarDiary.clear()
        for file in os.listdir("diary"):
            if file.endswith(".txt"):
                self.daftarDiary.addItem(file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main()
    window.show()
    sys.exit(app.exec())
