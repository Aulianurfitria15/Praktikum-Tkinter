import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabell
# Membuat tabel dengan kolom seperti id, nama_siswa, 
# biologi, fisika, inggris, dan prediksi_fakultas.
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuat koneksi ke database.
    cursor = conn.cursor() # Membuat objek cursor untuk eksekusi perintah SQL.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    """)
    conn.commit() # Menyimpan perubahan ke database.
    conn.close() # Menutup koneksi database.

# Fungsi untuk mengambil semua data dari database untuk
# ditampilkan di tabel
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fungsi untuk menyimpan data baru ke database
# VALUES (?, ?, ?, ?, ?) menggunakan placeholder untuk 
# memasukkan nilai secara dinamis agar aman dari SQL Injection.
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

# Fungsi untuk memperbarui data di database
# untuk memperbarui data siswa berdasarkan ID uniknya.
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()

# Fungsi untuk menghapus data dari database
# Data akan dihapus dari database berdasarkan ID.
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

# Fungsi untuk menghitung prediksi fakultas
# Menentukan fakultas berdasarkan nilai tertinggi dari 3 mata pelajaran.
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

# Fungsi untuk menangani tombol submit
# Mengelola input dan validasi saat tombol Submit ditekan.
# submit: Mengambil input dari pengguna, memvalidasi data, menghitung prediksi fakultas, 
# menyimpan data ke database, dan memperbarui tampilan tabel.
def submit():
    try:
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menangani tombol update
# Mengatur pembaruan data berdasarkan input dan ID yang dipilih.
# update: Mengupdate data yang telah dipilih dari tabel berdasarkan ID yang 
# dipilih, serta memvalidasi input.
def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menangani tombol delete
# delete: Menghapus data yang dipilih dari tabel dan memperbarui 
# tampilan tabel setelah penghapusan.
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk mengosongkan input
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():
        tree.delete(row) # Menghapus semua baris yang ada di tabel.
    for row in fetch_data():
        tree.insert("", "end", values=row)  # Mengisi tabel dengan data dari database.

# Fungsi untuk mengisi input dengan data dari tabel
# populate_table: Mengambil data dari database dan mengisi 
# tabel dengan data tersebut.
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0] # Mengambil item yang dipilih dari tabel.
        selected_row = tree.item(selected_item)['values'] # Mengambil nilai dari baris yang dipilih.

        selected_record_id.set(selected_row[0]) # Mengisi ID yang dipilih.
        nama_var.set(selected_row[1]) # Mengisi nama siswa.
        biologi_var.set(selected_row[2]) # Mengisi nilai biologi
        fisika_var.set(selected_row[3]) # Mengisi nilai fisika
        inggris_var.set(selected_row[4]) # Mengisi nilai inggris
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
# Memanggil fungsi create_database untuk memastikan bahwa 
# database dan tabel sudah siap digunakan saat aplikasi dijalankan.
create_database()

# Membuat GUI dengan Tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")
root.configure(bg="#B3EDB3")

# Variabel tkinter
# Menggunakan StringVar untuk menyimpan nilai input dari pengguna.
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

# Elemen GUI
# Membuat label dan entry (input) untuk nama siswa dan nilai
# mata pelajaran lainnya. Menggunakan grid untuk menata posisi elemen.
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5) # Label untuk nama siswa.
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5) # Input untuk nama siswa.

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5) # Label untuk nama siswa.
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5) # Input untuk nilai biologi.

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5) # Label untuk nama siswa.
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5) # Input untuk nilai fisika

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5) # Label untuk nama siswa.
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5) # Input untuk nilai inggris

Button(root, text="Submit", command=submit).grid(row=4, column=0, pady=10) # Tombol untuk menambah data.
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10) # Tombol untuk memperbarui data.
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10) # Tombol untuk menghapus data.

# Tabel untuk menampilkan data
# Membuat tabel menggunakan Treeview untuk menampilkan 
# data siswa dengan kolom yang ditentukan.
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas") # Mendefinisikan kolom tabel
tree = ttk.Treeview(root, columns=columns, show='headings') # Membuat tabel untuk menampilkan data.

for col in columns:
    tree.heading(col, text=col.capitalize()) # Mengatur nama kolom.
    tree.column(col, anchor='center') # Menyetel posisi teks di kolom ke tengah

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10) # Menempatkan tabel di grid.
tree.bind('<ButtonRelease-1>', fill_inputs_from_table) # Mengikat event klik pada tabel untuk mengisi input.

# Mengisi tabel dengan data
# Memanggil populate_table untuk mengisi tabel dengan 
# data dari database saat aplikasi dimulai.
populate_table()

# Menjalankan aplikasi
root.mainloop()