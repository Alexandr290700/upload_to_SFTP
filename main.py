import paramiko
import zipfile
import os


hostname = "sftp.ex.com"
port = 22
username = "username"
password = "password"
remote_path = "/<Partner code>/SELLTHR/"

# Генерация данных для файлов INVOIC и INVRPT
invoice_data = "G|GUID|...\r\nC|PartnerCode|...\r\nD|Data|..."
invrpt_data = "G|GUID|...\r\nS|Date1|Stats1|...\r\nS|Date2|Stats2|..."


invoice_data = invoice_data.encode('utf-8').decode('cp1251', 'ignore')
invrpt_data = invrpt_data.encode('utf-8').decode('cp1251', 'ignore')

# Создание текстовых файлов
with open("INVOIC.txt", "w", encoding="cp1251") as inv_file:
    inv_file.write(invoice_data)

with open("INVRPT.txt", "w", encoding="cp1251") as rpt_file:
    rpt_file.write(invrpt_data)

# Упаковка в ZIP
with zipfile.ZipFile("ST_INVOIC_<Partner code>_<GUID>.zip", "w") as inv_zip:
    inv_zip.write("INVOIC.txt")

with zipfile.ZipFile("ST_INVRPT_<Partner_code>_<GUID>.zip", "w") as rpt_zip:
    rpt_zip.write("INVRPT.txt")

# Устанавливаем соединение
client = paramiko.SSHClient()
client.set_missing_host_key_policy((paramiko.AutoAddPolicy()))
client.connect(hostname, port, username, password)

# Загрузка архивов на сервер
try:
    sftp = client.open_sftp()
    sftp.put("ST_INVOIC_<Partner code>_<GUID>.zip", remote_path + "ST_INVOIC_<Partner code>_<GUID>.zip")
    sftp.put("ST_INVRPT_<Partner code>_<GUID>.zip", remote_path + "ST_INVRPT_<Partner code>_<GUID>.zip")
    sftp.close()
except Exception as ex:
    log_data = f"Ошибка при загрузке файла на SFTP: {str(ex)}\n"

# Создание лог файла с результатами
log_data += "Логи событий и сообщений\n"
with open("log.txt", "w", encoding="utf-8") as log_file:
    log_file.write(log_data)

try:
    sftp = client.open_sftp()
    sftp.put("log.txt", remote_path + "LOG/log.txt")
    sftp.close()
except Exception as ex:
    log_data = f"Ошибка при загрузке лог файла: {str(ex)}\n"

log_data += "Логи остальных событий\n"
with open("log.txt", "w", encoding="utf-8") as log_file:
    log_file.write(log_data)

client.close()

print("Complete...")
