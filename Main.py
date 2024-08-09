import os
import pandas as pd

# Minta pengguna memasukkan nama GPON
gpon_name = input("Masukkan nama GPON (misalnya, GPON04-KLJ atau GPON04-KPO): ")

# Tentukan path direktori di mana file log berada
directory = r'C:\Users\HP\Downloads'

# Buat path lengkap berdasarkan input nama GPON
log_file_path = os.path.join(directory, f'{gpon_name} LOGX.log')

# Cek apakah file ada
if not os.path.isfile(log_file_path):
    print(f"File {log_file_path} tidak ditemukan!")
else:
    with open(log_file_path, 'r', encoding='utf-8') as file:
        log_data = file.read()

    # Membuat key pemisah berdasarkan input GPON dengan tambahan "-D5-"
    gpon_split_key = f'{gpon_name[:6]}-D5-{gpon_name[7:]}-3#sho pon onu information'

    # Pisahkan section berdasarkan key ini
    port_sections = log_data.split(gpon_split_key)

    # Siapkan data untuk DataFrame
    port_results = []
    problem_statuses = ["LOSi", "Shutdown", "UnKnown", "SFi", "LOAMi", "LOAi"]

    for section in port_sections[1:]:
        if section.strip():
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
    output_file_path = os.path.join(directory, f'{gpon_name}-Analysis.xlsx')
    df.to_excel(output_file_path, index=False)

    print(f"File berhasil disimpan di {output_file_path}")
