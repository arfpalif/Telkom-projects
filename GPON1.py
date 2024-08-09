import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

def analyze_log():
    # Minta pengguna memilih file log
    log_file_path = filedialog.askopenfilename(title="Pilih File Log", filetypes=[("Log Files", "*.log"), ("All Files", "*.*")])
    
    if not log_file_path:
        messagebox.showwarning("Peringatan", "File log tidak dipilih!")
        return

    # Minta pengguna memasukkan nama GPON
    gpon_name = gpon_entry.get().strip()

    if not gpon_name:
        messagebox.showwarning("Peringatan", "Nama GPON tidak boleh kosong!")
        return

    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            log_data = file.read()

        # Membuat key pemisah berdasarkan input GPON dengan tambahan "-D5-"
        gpon_split_key = f'{gpon_name[:6]}-D5-{gpon_name[7:]}-3#sho pon onu information'
        print(f"Using split key: {gpon_split_key}")  # Debugging

        # Pisahkan section berdasarkan key ini
        port_sections = log_data.split(gpon_split_key)
        print(f"Number of sections found: {len(port_sections) - 1}")  # Debugging

        if len(port_sections) > 1:
            # Siapkan data untuk DataFrame
            port_results = []
            problem_statuses = ["LOSi", "Shutdown", "UnKnown", "SFi", "LOAMi", "LOAi"]

            for section in port_sections[1:]:
                if section.strip():
                    print(f"Processing section: {section[:200]}")  # Debugging (show first 200 chars)
                    lines = section.strip().split('\n')
                    port_info_line = lines[0].strip()
                    port_name = port_info_line.split()[-1] if len(port_info_line.split()) > 1 else "Unknown"

                    status = 0
                    for status_line in lines:
                        if any(problem in status_line for problem in problem_statuses):
                            status = 1
                            break

                    port_results.append((port_name, status))

            df = pd.DataFrame(port_results, columns=['Port Name', 'Status'])

            # Simpan hasil ke file Excel
            output_file_path = os.path.splitext(log_file_path)[0] + f'-{gpon_name}-Analysis.xlsx'
            df.to_excel(output_file_path, index=False)

            messagebox.showinfo("Sukses", f"File berhasil disimpan di {output_file_path}")
        else:
            messagebox.showwarning("Peringatan", f"Tidak ada section ditemukan dengan kunci: {gpon_split_key}")

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Buat jendela utama
root = tk.Tk()
root.title("GPON Log Analyzer")

# Label dan Entry untuk input nama GPON
tk.Label(root, text="Masukkan nama GPON:").grid(row=0, column=0, padx=10, pady=10)
gpon_entry = tk.Entry(root)
gpon_entry.grid(row=0, column=1, padx=10, pady=10)

# Tombol untuk memulai analisis
analyze_button = tk.Button(root, text="Analyze Log", command=analyze_log)
analyze_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Jalankan aplikasi
root.mainloop()
