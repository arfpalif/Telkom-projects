import pandas as pd

# Path file log
log_file_path = r'C:\Users\HP\Downloads\GPON00-KEP LOGX.log'
with open(log_file_path, 'r', encoding='utf-8') as file:
    log_data = file.read()

# Pisahkan data berdasarkan port menggunakan pemisah yang konsisten
port_sections = log_data.split('GPON00-D5-KEP-3#sho pon onu information')

# Siapkan data untuk DataFrame
port_results = []
problem_statuses = ["LOSi", "Shutdown", "UnKnown", "SFi", "LOAMi", "LOAi"]

for section in port_sections[1:]:  # Lewati split pertama karena berada sebelum informasi port pertama
    if section.strip():
        lines = section.strip().split('\n')
        port_info_line = lines[0].strip()
        port_name = port_info_line.split()[-1] if len(port_info_line.split()) > 1 else "Unknown"
        
        # Periksa apakah ada status masalah dalam bagian data ini
        status = 0
        for status_line in lines:
            if any(problem in status_line for problem in problem_statuses):
                status = 1
                break
        
        port_results.append((port_name, status))

# Buat DataFrame
df = pd.DataFrame(port_results, columns=['Port Name', 'Status'])

# Simpan DataFrame ke file CSV
output_file_path = r'C:\Users\HP\Downloads\GPON00-KEP-Analysis.csv'  # Ganti dengan path file output Anda
df.to_csv(output_file_path, index=False)

print(f"File berhasil disimpan di {output_file_path}")
