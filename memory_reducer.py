import ctypes
import time
import psutil
from threading import Thread
import pystray
from PIL import Image

# Define constantes
PROCESS_ALL_ACCESS = 0x1F0FFF
kernel32 = ctypes.windll.kernel32

# Define a função da kernel32.dll
SetProcessWorkingSetSize = kernel32.SetProcessWorkingSetSize
SetProcessWorkingSetSize.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t]
SetProcessWorkingSetSize.restype = ctypes.c_bool

class RedutorDeMemoria:
    def __init__(self):
        self.ativo = False
        self.thread = None

    def reduzir_uso_de_memoria(self):
        while self.ativo:
            processos_chrome = [proc for proc in psutil.process_iter(attrs=['pid', 'name']) if 'chrome' in proc.info['name'].lower()]
            for proc in processos_chrome:
                try:
                    handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, proc.info['pid'])
                    if handle:
                        SetProcessWorkingSetSize(handle, -1, -1)
                        kernel32.CloseHandle(handle)
                        print(f"Uso de memória reduzido para PID {proc.info['pid']} ({proc.info['name']})")
                except Exception as e:
                    print(f"Não foi possível reduzir o uso de memória para PID {proc.info['pid']} ({proc.info['name']}): {e}")
            time.sleep(5)

    def iniciar(self):
        if not self.ativo:
            self.ativo = True
            self.thread = Thread(target=self.reduzir_uso_de_memoria)
            self.thread.start()

    def parar(self):
        if self.ativo:
            self.ativo = False
            if self.thread.is_alive():
                self.thread.join()

redutor_de_memoria = RedutorDeMemoria()

def ao_ativar(icon, item):
    redutor_de_memoria.iniciar()
    atualizar_menu(icon)
    print("Redução de memória ativada.")

def ao_desativar(icon, item):
    redutor_de_memoria.parar()
    atualizar_menu(icon)
    print("Redução de memória desativada.")

def ao_sair(icon, item):
    redutor_de_memoria.parar()
    icon.stop()
    print("Saindo da aplicação.")

def criar_imagem():
    return Image.open("chrome_icon.png") # Ícone da bandeja

def atualizar_menu(icon):
    icon.menu = pystray.Menu(
        pystray.MenuItem('Ativar', ao_ativar, checked=lambda item: redutor_de_memoria.ativo),
        pystray.MenuItem('Desativar', ao_desativar, checked=lambda item: not redutor_de_memoria.ativo),
        pystray.MenuItem('Sair', ao_sair)
    )
    icon.update_menu()

icon = pystray.Icon("Redutor de Memória", criar_imagem(), "Redutor de Memória")
atualizar_menu(icon)
icon.run()

# Créditos: Daniel Paladino (daniel@mamaimagem.com.br)