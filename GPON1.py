import os
import pandas as pd
from tkinter import filedialog, messagebox, Tk

# Fungsi untuk menjalankan analisis log
def analyze_log():
    # Buka dialog untuk memilih file log
    log_file_path = filedialog.askopenfilename(title="Pilih File Log", filetypes=[("Log Files", "*.log"), ("All Files", "*.*")])
    
    if not log_file_path:
        messagebox.showwarning("Peringatan", "File log tidak dipilih!")
        return
    
    # Ekstrak nama GPON dari nama file log
    file_name = os.path.basename(log_file_path)
    gpon_name = file_name.split(' ')[0]  # Misalnya, dari "GPON01-KPO LOGX.log" dapatkan "GPON01-KPO"

    with open(log_file_path, 'r', encoding='utf-8') as file:
        log_data = file.read()

    # Membuat key pemisah berdasarkan nama GPON dengan tambahan "-D5-"
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
        output_file_path = os.path.splitext(log_file_path)[0] + '-Analysis.xlsx'
        df.to_excel(output_file_path, index=False)

        messagebox.showinfo("Sukses", f"File berhasil disimpan di {output_file_path}")
    else:
        messagebox.showwarning("Peringatan", f"Tidak ada section ditemukan dengan kunci: {gpon_split_key}")

# Buat GUI untuk memilih file log
root = Tk()
root.withdraw()  # Sembunyikan jendela utama

analyze_log()
