import socket
import tqdm
import cProfile
import math

from conan_cryptanalysis_2.socket import get_all_messages, get_challenge, get_access_token
from conan_cryptanalysis_2.cryptanalysis import (
    solve_mode_a,
    solve_mode_b,
    solve_mode_c,
    solve_mode_d,
    solve_mode_e
)

TOKEN = 'Ovx2cO9i7P'

PART_A_HOST = '165.232.161.196'
PART_A_PORT = 4020

def part_a():
    # Connect ke server
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT_SOCKET.connect((PART_A_HOST, PART_A_PORT))

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
    CLIENT_SOCKET.close()

PART_B_HOST = '165.232.161.196'
PART_B_PORT = 1303

def part_b():
    # Connect ke server
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT_SOCKET.connect((PART_B_HOST, PART_B_PORT))

    # Pertama-tama kita perlu submit token
    TOKEN_Q = CLIENT_SOCKET.recv(1024)
    CLIENT_SOCKET.send(TOKEN.encode())
    print(TOKEN_Q.decode().strip(), TOKEN)

    # Chosen Plaintext: 2
    get_all_messages(CLIENT_SOCKET, "Masukkan perintah: ")
    CLIENT_SOCKET.send(b'1')

    get_all_messages(CLIENT_SOCKET, "Masukkan nomor arsip (dalam bentuk integer): ")
    CLIENT_SOCKET.send(b'2')
    
    get_all_messages(CLIENT_SOCKET, "Masukkan isi arsip: ")
    CLIENT_SOCKET.send(b'2')

    access_token_1 = get_access_token(CLIENT_SOCKET)

    # Chosen Plaintext: 3
    CLIENT_SOCKET.send(b'1')

    get_all_messages(CLIENT_SOCKET, "Masukkan nomor arsip (dalam bentuk integer): ")
    CLIENT_SOCKET.send(b'3')
    
    get_all_messages(CLIENT_SOCKET, "Masukkan isi arsip: ")
    CLIENT_SOCKET.send(b'3')

    access_token_2 = get_access_token(CLIENT_SOCKET)

    with cProfile.Profile() as c_perf:
    
        pubkey_candidates = []
        print("BRUTEFORCING PUBKEY")
        pow_1 = pow(2, 2 ** 15)
        pow_2 = pow(3, 2 ** 15)
        for e_guess in tqdm.tqdm(range(2 ** 15, 2 ** 16 + 1)):
            n_guess = math.gcd(
                pow_1 - access_token_1, 
                pow_2 - access_token_2
            )
            if n_guess > access_token_1 and n_guess > access_token_2:
                print(e_guess, n_guess)
                pubkey_candidates.append((e_guess, n_guess))
            pow_1 *= 2
            pow_2 *= 3

        print(pubkey_candidates)

        for e_candidate, n_candidate in pubkey_candidates:
            pow_1 = pow(2, e_candidate, n_candidate)
            pow_2 = pow(3, e_candidate, n_candidate)
            if pow_1 == access_token_1 and pow_2 == access_token_2:
                print('PUBKEY CONFIRMED')
                break
    
        c_perf.print_stats('cumtime')




if __name__ == "__main__":
    part_b()