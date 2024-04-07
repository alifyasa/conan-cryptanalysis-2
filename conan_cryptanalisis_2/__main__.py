import socket
import re

from conan_cryptanalisis_2.socket import get_all_messages, get_challenge
from conan_cryptanalisis_2.cryptanalysis import (
    solve_mode_a,
    solve_mode_b,
    solve_mode_c,
    solve_mode_d,
    solve_mode_e
)

HOST = '165.232.161.196'
PORT = 4020
TOKEN = 'Ovx2cO9i7P'

def main():
    # Connect ke server
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT_SOCKET.connect((HOST, PORT))

    # Pertama-tama kita perlu submit token
    TOKEN_Q = CLIENT_SOCKET.recv(1024)
    CLIENT_SOCKET.send(TOKEN.encode())
    print(TOKEN_Q.decode().strip(), TOKEN)

    # Start Challenge
    for _ in range(30):
        paket_soal, rsa_n, rsa_e, ciphertext = get_challenge(CLIENT_SOCKET)

        if paket_soal == "A":
            decryped_text = solve_mode_a(rsa_n, rsa_e, ciphertext)
        elif paket_soal == "B":
            decryped_text = solve_mode_b(rsa_n, rsa_e, ciphertext)
        elif paket_soal == "C":
            decryped_text = solve_mode_c(rsa_n, rsa_e, ciphertext)
        elif paket_soal == "D":
            decryped_text = solve_mode_d(rsa_n, rsa_e, ciphertext)
        elif paket_soal == "E":
            decryped_text = solve_mode_e(rsa_n, rsa_e, ciphertext)
        else:
            print(f"Unexpexted value for paket_soal: {paket_soal}")
        
        print(decryped_text.decode())
        CLIENT_SOCKET.send(decryped_text)
    
    get_all_messages(CLIENT_SOCKET, '}', True)



if __name__ == "__main__":
    main()