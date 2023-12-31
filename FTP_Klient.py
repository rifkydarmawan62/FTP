from ftplib import FTP, FTP_TLS, error_perm
from platform import system
from subprocess import run
from tkinter.filedialog import askopenfilename, askdirectory
from typing import Literal
from colorama import Fore
from socket import gaierror
from os.path import exists, getsize

def __bersihkan_layar(__teks : str | None = None):
    run("cls" if system() == "Windows" else "clear", shell = True)
    if __teks:
        print(__teks)
def __enter_untuk_kembali(__pesan : str | None = None):
    if __pesan:
        print(__pesan)
    input(f"{Fore.RESET}Tekan enter untuk kembali")
def __tutup_program():
    print(f"{Fore.LIGHTRED_EX}Program ditutup{Fore.RESET}")
def __menu_input_argumen(__login_anonymous : bool | None = False, tls : bool = False):
    MENU_FTP = f"""[-] {Fore.LIGHTRED_EX}putuskan koneksi{Fore.RESET}
[0] bersihkan layar
[1] tampilkan direktori saat ini
[2] ganti direktori saat ini
[3] buat direktori baru
[4] hapus direktori
[5] tampilkan daftar direktori dan file
[6] tampilkan ukuran file
[7] ganti nama file
[8] hapus file
[9] download file
[10] upload file"""
    alamat_server_ftp : str
    while True:
        alamat_server_ftp = input(f"{Fore.RESET}Masukkan alamat server FTP : ")
        if alamat_server_ftp:
            break
        else:
            print(f"{Fore.LIGHTRED_EX}Input alamat server FTP kosong!")
    if tls:
        PORT_FTP_DEFAULT = 990
    else:
        PORT_FTP_DEFAULT = 21
    port_ftp = input(f"{Fore.RESET}Masukkan port FTP (default = {PORT_FTP_DEFAULT}) : ")
    if port_ftp.strip() == "":
        print(f"{Fore.LIGHTGREEN_EX}Port default {PORT_FTP_DEFAULT} digunakan")
        port_ftp = PORT_FTP_DEFAULT
    elif port_ftp.strip().isdigit():
        port_ftp = int(port_ftp)
    else:
        print(f"{Fore.LIGHTRED_EX}Input port tidak valid!\n{Fore.LIGHTGREEN_EX}Port default {PORT_FTP_DEFAULT} digunakan")
        port_ftp = PORT_FTP_DEFAULT
    nama_pengguna : str = ""
    kata_sandi : str = ""
    if __login_anonymous == False:
        while True:
            nama_pengguna = input(f"{Fore.RESET}Masukkan nama pengguna : ")
            if nama_pengguna:
                break
            else:
                print(f"{Fore.LIGHTRED_EX}Input nama pengguna kosong!")
        while True:
            kata_sandi = input(f"{Fore.RESET}Masukkan kata sandi : {Fore.BLACK}")
            if kata_sandi:
                __bersihkan_layar()
                break
            else:
                print(f"{Fore.LIGHTRED_EX}Input kata sandi kosong!")
    def hubungkan_ke_server_ftp(__server_ftp : FTP | FTP_TLS):
        print(f"{Fore.LIGHTYELLOW_EX}Menghubungkan ke server FTP {alamat_server_ftp} port {port_ftp} ...")
        try:
            print(f"{Fore.LIGHTBLUE_EX}{__server_ftp.connect(host = alamat_server_ftp, port = port_ftp)}")
        except TimeoutError as error:
            __enter_untuk_kembali(f"{Fore.LIGHTRED_EX}Koneksi ke server FTP {alamat_server_ftp} port {port_ftp} gagal!\n{Fore.LIGHTBLUE_EX}{error}")
        except ConnectionRefusedError as error:
            __enter_untuk_kembali(f"{Fore.LIGHTRED_EX}Server FTP {alamat_server_ftp} port {port_ftp} menolak untuk terhubung\n{Fore.LIGHTBLUE_EX}{error}")
        except gaierror as error:
            __enter_untuk_kembali(f"{Fore.LIGHTRED_EX}Tidak dapat terhubung ke server FTP {alamat_server_ftp} port {port_ftp}\n{Fore.LIGHTBLUE_EX}{error}")
        except OSError as error:
            __enter_untuk_kembali(f"{Fore.LIGHTRED_EX}Tidak dapat terhubung ke server FTP {alamat_server_ftp} port {port_ftp}\n{Fore.LIGHTBLUE_EX}{error}")
        else:
            KONEKSI_TERHUBUNG = f"{Fore.LIGHTGREEN_EX}Terhubung ke server FTP {alamat_server_ftp} port {port_ftp}"
            print(KONEKSI_TERHUBUNG)
            koneksi_error : bool = False
            if isinstance(__server_ftp, FTP_TLS):
                print(f"{Fore.LIGHTYELLOW_EX}Melakukan autentikasi SSL/TLS ...")
                try:
                    print(f"{Fore.LIGHTBLUE_EX}{__server_ftp.auth()}")
                except error_perm as error:
                    __enter_untuk_kembali(f"{Fore.LIGHTRED_EX}Autentikasi SSL/TLS gagal!\n{Fore.LIGHTBLUE_EX}{error}")
                    koneksi_error = True
                else:
                    print(f"{Fore.LIGHTGREEN_EX}Autentikasi SSL/TLS berhasil!")
                    print(f"{Fore.LIGHTYELLOW_EX}Mengamankan koneksi dengan SSL/TLS")
                    print(f"{Fore.LIGHTBLUE_EX}{__server_ftp.prot_p()}")
                    print(f"{Fore.LIGHTGREEN_EX}Koneksi diamankan dengan SSL/TLS")
            if (not koneksi_error) and (__login_anonymous != None):
                print(f"{Fore.LIGHTYELLOW_EX}Melakukan login ...")
                try:
                    if __login_anonymous == False:
                        print(f"{Fore.LIGHTBLUE_EX}{__server_ftp.login(user = nama_pengguna, passwd = kata_sandi)}")
                    else:
                        print(f"{Fore.LIGHTBLUE_EX}{__server_ftp.login()}")
                except error_perm as error:
                    __enter_untuk_kembali(f"{Fore.LIGHTRED_EX}Login gagal\n{Fore.LIGHTBLUE_EX}{error}")
                    koneksi_error = True
                else:
                    print(f"{Fore.LIGHTGREEN_EX}Login berhasil!")
            if not koneksi_error:
                input(f"{Fore.RESET}Tekan enter untuk melanjutkan")
                argumen_ftp : bool = True
                while argumen_ftp:
                    def memutuskan_koneksi():
                        print(f"{Fore.LIGHTYELLOW_EX}Memutuskan koneksi dari server FTP {alamat_server_ftp} port {port_ftp}\n{Fore.LIGHTBLUE_EX}{server_ftp.quit()}")
                        __enter_untuk_kembali(f"{Fore.LIGHTRED_EX}Terputus dari server FTP {alamat_server_ftp} port {port_ftp}")
                    if __login_anonymous == True:
                        __bersihkan_layar(f"{KONEKSI_TERHUBUNG} dalam mode anonymous login\n\nTekan Ctrl + C untuk diskonek\n\n{Fore.LIGHTBLUE_EX}{__server_ftp.getwelcome()}{Fore.RESET}\n\n{MENU_FTP}")
                    else:
                        __bersihkan_layar(f"{KONEKSI_TERHUBUNG}\n\nTekan Ctrl + C untuk diskonek\n\n{Fore.LIGHTBLUE_EX}{__server_ftp.getwelcome()}{Fore.RESET}\n\n{MENU_FTP}")
                    while True:
                        argumen = input(f"{Fore.RESET}Pilih nomor : ")
                        match argumen:
                            case "-":
                                memutuskan_koneksi()
                                argumen_ftp = False
                                break
                            case "0":
                                break
                            case "1":
                                try:
                                    print(f"{Fore.LIGHTGREEN_EX}Direktori saat ini {__server_ftp.pwd()}")
                                except error_perm as error:
                                    print(f"{Fore.LIGHTRED_EX}Gagal menampilkan direktori saat ini\n{Fore.LIGHTBLUE_EX}{error}")
                            case "2":
                                argumen = input(f"{Fore.RESET}Masukkan direktori : ")
                                if argumen:
                                    try:
                                        __server_ftp.cwd(argumen)
                                    except error_perm as error:
                                        print(f"{Fore.LIGHTRED_EX}Gagal mengganti direktori ke \"{argumen}\"\n{Fore.LIGHTBLUE_EX}{error}")
                                        print(f"{Fore.LIGHTGREEN_EX}Direktori saat ini {__server_ftp.pwd()}")
                                    else:
                                        print(f"{Fore.LIGHTGREEN_EX}Direktori diganti ke {__server_ftp.pwd()}")
                                else:
                                    print(f"{Fore.LIGHTRED_EX}Input direktori kosong!")
                            case "3":
                                argumen = input("Masukkan direktori : ")
                                if argumen:
                                    direktori = __server_ftp.mkd(argumen)
                                    print(f"{Fore.LIGHTGREEN_EX}Direktori dibuat menjadi {direktori}")
                                else:
                                    print(f"{Fore.LIGHTRED_EX}Input direktori kosong!")
                            case "4":
                                argumen = input("Masukkan direktori : ")
                                if argumen:
                                    try:
                                        direktori = __server_ftp.rmd(argumen)
                                    except error_perm as error:
                                        print(f"{Fore.LIGHTRED_EX}Gagal menghapus direktori \"{argumen}\"\n{Fore.LIGHTBLUE_EX}{error}")
                                    else:
                                        print(f"{Fore.LIGHTGREEN_EX}Direktori dihapus menjadi {direktori}")
                                else:
                                    print(f"{Fore.LIGHTRED_EX}Input direktori kosong!")
                            case "5":
                                try:
                                    print(f"{Fore.LIGHTGREEN_EX}"); __server_ftp.dir(); print(Fore.RESET)
                                except error_perm as error:
                                    print(f"{Fore.LIGHTRED_EX}Gagal menampilkan direktori dan file\n{Fore.LIGHTBLUE_EX}{error}")
                            case "6":
                                argumen = input(f"{Fore.RESET}Masukkan nama file : ")
                                if argumen:
                                    try:
                                        print(f"{Fore.LIGHTGREEN_EX}{__server_ftp.size(argumen)} byte")
                                    except error_perm as error:
                                        print(f"{Fore.LIGHTRED_EX}Error saat menampilkan ukuran file \"{argumen}\"\n{Fore.LIGHTBLUE_EX}{error}")
                                else:
                                    print(f"{Fore.LIGHTRED_EX}Input nama file kosong!")
                            case "7":
                                nama_file_lama = input(f"{Fore.RESET}Masukkan nama file : ")
                                if nama_file_lama:
                                    if __periksa_karakter(nama_file_lama, "file"):
                                        nama_file_baru = input(f"{Fore.RESET}Masukkan nama file baru : ")
                                        if nama_file_baru:
                                            if __periksa_karakter(nama_file_baru, "file"):
                                                try:
                                                    print(Fore.LIGHTBLUE_EX + __server_ftp.rename(nama_file_lama, nama_file_baru))
                                                except error_perm as error:
                                                    print(f"{Fore.LIGHTRED_EX}Tidak dapat mengganti nama file dari \"{nama_file_lama}\" menjadi \"{nama_file_baru}\"\n{Fore.LIGHTBLUE_EX}{error}")
                                                else:
                                                    print(f"{Fore.LIGHTGREEN_EX}Nama file diubah dari \"{nama_file_lama}\" menjadi \"{nama_file_baru}\"")
                                        else:
                                            print(f"{Fore.LIGHTRED_EX}Input nama file kosong!")
                                else:
                                    print(f"{Fore.LIGHTRED_EX}Input nama file kosong!")
                            case "8":
                                argumen = input(f"{Fore.RESET}Masukkan nama file : ")
                                if argumen:
                                    if __periksa_karakter(argumen, "file"):
                                        print(f"{Fore.LIGHTYELLOW_EX}Menghapus file \"{argumen}\"")
                                        try:
                                            print(Fore.LIGHTBLUE_EX + __server_ftp.delete(argumen))
                                        except error_perm as error:
                                            print(f"{Fore.LIGHTRED_EX}Gagal menghapus file \"{argumen}\"\n{Fore.LIGHTBLUE_EX}{error}")
                                        else:
                                            print(f"{Fore.LIGHTGREEN_EX}File \"{argumen}\" dihapus!")
                                else:
                                    print(f"{Fore.LIGHTRED_EX}Input nama file kosong!")
                            case "9":
                                if len(__server_ftp.nlst()) > 0:
                                    print(Fore.LIGHTGREEN_EX); __server_ftp.dir()
                                    file_server = input(f"{Fore.RESET}Masukkan nama file dari direktori {__server_ftp.pwd()} : ")
                                    if file_server:
                                        if __periksa_karakter(file_server, "file"):
                                            lokasi_download = __buka_jendela_baru("Pilih folder untuk mengunduh file", "pilih folder")
                                            if lokasi_download:
                                                print(f"{Fore.LIGHTYELLOW_EX}Mengunduh file \"{file_server}\" dari server FTP {alamat_server_ftp}")
                                                try:
                                                    with open(f"{lokasi_download}/{file_server}", "wb") as file_yang_di_download:
                                                        if __server_ftp.pwd() == "/":
                                                            ukuran_file = __server_ftp.size(f"/{file_server}")
                                                            if isinstance(ukuran_file, int):
                                                                print(Fore.LIGHTBLUE_EX + __server_ftp.retrbinary(f"RETR /{file_server}", file_yang_di_download.write, ukuran_file))
                                                            else:
                                                                print(Fore.LIGHTBLUE_EX + __server_ftp.retrbinary(f"RETR /{file_server}", file_yang_di_download.write))
                                                        else:
                                                            ukuran_file = __server_ftp.size(f"{__server_ftp.pwd()}/{file_server}")
                                                            if isinstance(ukuran_file, int):
                                                                print(Fore.LIGHTBLUE_EX + __server_ftp.retrbinary(f"RETR {__server_ftp.pwd()}/{file_server}", file_yang_di_download.write, ukuran_file))
                                                            else:
                                                                print(Fore.LIGHTBLUE_EX + __server_ftp.retrbinary(f"RETR {__server_ftp.pwd()}/{file_server}", file_yang_di_download.write))
                                                except error_perm as error:
                                                    print(f"{Fore.LIGHTRED_EX}Gagal mengunduh file \"{file_server}\" dari server FTP {alamat_server_ftp}\n{Fore.LIGHTBLUE_EX}{error}")
                                                else:
                                                    print(f"{Fore.LIGHTGREEN_EX}File \"{file_server}\" telah diunduh dari server FTP {alamat_server_ftp}")
                                            else:
                                                print(f"{Fore.LIGHTRED_EX}Folder tidak dipilih!")
                                    else:
                                        print(f"{Fore.LIGHTRED_EX}Input nama file kosong!")
                                else:
                                    print(f"File dari direktori {__server_ftp.pwd()} kosong!")
                            case "10":
                                file_klient = __buka_jendela_baru("Pilih file untuk diupload ke server FTP", "pilih file")
                                if "/" in file_klient:
                                    nama_file = file_klient.split("/")[-1]
                                    print(f"{Fore.LIGHTYELLOW_EX}Mengupload file \"{nama_file}\" ke server FTP {alamat_server_ftp} ...")
                                    try:
                                        with open(file_klient, mode = "rb") as file_yang_di_upload:
                                            if __server_ftp.pwd() == "/":
                                                print(Fore.LIGHTBLUE_EX + __server_ftp.storbinary(f"STOR /{nama_file}", file_yang_di_upload, getsize(file_klient)))
                                            else:
                                                print(Fore.LIGHTBLUE_EX + __server_ftp.storbinary(f"STOR {__server_ftp.pwd()}/{nama_file}", file_yang_di_upload))
                                    except error_perm as error:
                                        print(f"{Fore.LIGHTRED_EX}Gagal mengupload file \"{file_klient}\" ke server FTP {alamat_server_ftp}\n{Fore.LIGHTBLUE_EX}{error}")
                                    else:
                                        print(f"{Fore.LIGHTGREEN_EX}File \"{nama_file}\" telah diupload ke server FTP {alamat_server_ftp}")
                                else:
                                    print(f"{Fore.LIGHTRED_EX}File tidak dipilih!")
                        print(f"{Fore.LIGHTYELLOW_EX}Memeriksa kode respon server FTP ...")
                        putuskan_koneksi : bool = False
                        KODE_RESPON = __server_ftp.lastresp
                        match KODE_RESPON:
                            case "530":
                                print(f"{Fore.LIGHTRED_EX}Autentikasi tidak valid!")
                                putuskan_koneksi = True
                            case "534":
                                putuskan_koneksi = True
                        print(f"{Fore.LIGHTGREEN_EX}Kode respon server FTP {Fore.LIGHTBLUE_EX}{KODE_RESPON}")
                        if putuskan_koneksi:
                            memutuskan_koneksi()
                            argumen_ftp = False
                            break
    try:
        if not tls:
            with FTP() as server_ftp:
                hubungkan_ke_server_ftp(server_ftp)
        else:
            with FTP_TLS() as server_ftps:
                hubungkan_ke_server_ftp(server_ftps)
    except KeyboardInterrupt:
        __enter_untuk_kembali(f"{Fore.LIGHTRED_EX}Terputus dari server FTP {alamat_server_ftp} karena interupsi keyboard Ctrl + C")
def __periksa_karakter(__nama_file_atau_folder : str, __file_atau_folder : Literal["folder", "file"]):
    DAFTAR_KARAKTER_TIDAK_VALID = "*", "\\", "/", ":", "?", "|", "\""
    for karakter_tidak_valid in DAFTAR_KARAKTER_TIDAK_VALID:
        if karakter_tidak_valid in __nama_file_atau_folder:
            print(f"{Fore.LIGHTRED_EX}Nama {__file_atau_folder} \"{__nama_file_atau_folder}\" tidak boleh menggunakan karakter {karakter_tidak_valid}")
            return False
    return True
def __buka_jendela_baru(__judul : str, __argumen : Literal["pilih folder", "pilih file"]):
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru")
    if __argumen == "pilih folder":
        return askdirectory(title = __judul)
    else:
        return askopenfilename(title = __judul)
BERANDA = f"""{Fore.RESET}Menu Login FTP (File Transfer Protocol) Client\n
Instagram : @rifkydarmawan62
GitHub : rifkydarmawan62\n
[-] {Fore.LIGHTRED_EX}keluar (Ctrl + C){Fore.RESET}
[0] bersihkan layar
[1] tanpa login
[2] login pengguna
[3] login anonymous
[4] tanpa login (SSL/TLS)
[5] login pengguna (SSL/TLS)
[6] login anonymous (SSL/TLS)"""
__menu_beranda : bool = True
try:
    while __menu_beranda:
        __bersihkan_layar(BERANDA)
        while True:
            argumen = input(f"{Fore.RESET}Pilih nomor : ")
            match argumen:
                case "-":
                    __menu_beranda = False
                    __tutup_program()
                case "0":
                    break
                case "1":
                    __menu_input_argumen(None)
                case "2":
                    __menu_input_argumen()
                case "3":
                    __menu_input_argumen(True)
                case "4":
                    __menu_input_argumen(None, True)
                case "5":
                    __menu_input_argumen(tls = True)
                case "6":
                    __menu_input_argumen(True, True)
                case _:
                    print(f"{Fore.LIGHTRED_EX}Input tidak valid!")
                    continue
            break
except KeyboardInterrupt:
    __tutup_program()