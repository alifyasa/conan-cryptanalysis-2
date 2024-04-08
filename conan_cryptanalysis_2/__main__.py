import socket
from tqdm import tqdm
import cProfile
import math
import time

from conan_cryptanalysis_2.utils import print_header
from conan_cryptanalysis_2.socket import (
    get_all_messages,
    get_challenge,
    get_access_token,
    get_admin_archive_number,
    get_flag,
)
from conan_cryptanalysis_2.cryptanalysis import (
    solve_mode_a,
    solve_mode_b,
    solve_mode_c,
    solve_mode_d,
    solve_mode_e,
)

TOKEN = "Ovx2cO9i7P"

PART_A_HOST = "165.232.161.196"
PART_A_PORT = 4020

NCOL = 80


def part_a():
    print_header("PART A", NCOL)
    # Connect ke server
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT_SOCKET.connect((PART_A_HOST, PART_A_PORT))

    # Pertama-tama kita perlu submit token
    TOKEN_Q = CLIENT_SOCKET.recv(1024)
    CLIENT_SOCKET.send(TOKEN.encode())
    print(TOKEN_Q.decode().strip(), TOKEN)

    print_header("DOING 30 CHALLENGES", NCOL, "-")
    # Start Challenge
    for _ in tqdm(range(30), ncols=NCOL):
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

        # print(decryped_text.decode())
        CLIENT_SOCKET.send(decryped_text)

    part_a_flag = get_flag(CLIENT_SOCKET)
    CLIENT_SOCKET.close()
    return part_a_flag


PART_B_HOST = "165.232.161.196"
PART_B_PORT = 1303


def part_b():
    print_header("PART B", NCOL)
    # Connect ke server
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT_SOCKET.connect((PART_B_HOST, PART_B_PORT))

    # Pertama-tama kita perlu submit token
    TOKEN_Q = CLIENT_SOCKET.recv(1024)
    CLIENT_SOCKET.send(TOKEN.encode())
    print(TOKEN_Q.decode().strip(), TOKEN)

    # Chosen Plaintext: 2
    print_header("GETTING CIPHERTEXT FOR PLAINTEXT '2'", NCOL, "-")
    get_all_messages(CLIENT_SOCKET, "Masukkan perintah: ")
    CLIENT_SOCKET.send(b"1")

    get_all_messages(CLIENT_SOCKET, "Masukkan nomor arsip (dalam bentuk integer): ")
    CLIENT_SOCKET.send(b"2")

    get_all_messages(CLIENT_SOCKET, "Masukkan isi arsip: ")
    CLIENT_SOCKET.send(b"2")

    access_token_1 = get_access_token(CLIENT_SOCKET)

    # Chosen Plaintext: 3
    print_header("GETTING CIPHERTEXT FOR PLAINTEXT '3'", NCOL, "-")
    CLIENT_SOCKET.send(b"1")

    get_all_messages(CLIENT_SOCKET, "Masukkan nomor arsip (dalam bentuk integer): ")
    CLIENT_SOCKET.send(b"3")

    get_all_messages(CLIENT_SOCKET, "Masukkan isi arsip: ")
    CLIENT_SOCKET.send(b"3")

    access_token_2 = get_access_token(CLIENT_SOCKET)

    pubkey_candidates = []

    pow_1 = pow(2, 2**15)
    pow_2 = pow(3, 2**15)
    print_header("BRUTEFORCING PUBLIC KEY", NCOL, "-")
    for e_guess in tqdm(range(2**15, 2**16 + 1), ncols=NCOL):
        n_guess = math.gcd(pow_1 - access_token_1, pow_2 - access_token_2)
        if n_guess > access_token_1 and n_guess > access_token_2:
            pubkey_candidates.append((e_guess, n_guess))

            test_pow_1 = pow(2, e_guess, n_guess)
            test_pow_2 = pow(3, e_guess, n_guess)
            if test_pow_1 == access_token_1 and test_pow_2 == access_token_2:
                pubkey = (e_guess, n_guess)
                break
        pow_1 *= 2
        pow_2 *= 3

    if pubkey == None:
        # seharusnya nyari lagi pakai (e, kn) sih
        # tapi sekarang throw aja dulu
        raise BaseException("Public Key Not Found")

    print_header("PUBLIC KEY CONFIRMED", NCOL, "-")

    # Get d
    CLIENT_SOCKET.send(b"3")
    admin_archive_number = get_admin_archive_number(CLIENT_SOCKET)

    CLIENT_SOCKET.send(b"2")
    get_all_messages(
        CLIENT_SOCKET, "Masukkan token akses nomor arsip (dalam bentuk integer): "
    )

    CLIENT_SOCKET.send(str(pow(admin_archive_number, pubkey[0], pubkey[1])).encode())
    part_b_flag = get_flag(CLIENT_SOCKET)
    CLIENT_SOCKET.close()
    return part_b_flag


if __name__ == "__main__":
    flag_a = part_a()
    flag_b = part_b()
    print_header("RESULT", NCOL)
    print_header("FLAG PART A", NCOL, "-")
    print(flag_a)
    print_header("FLAG PART B", NCOL, "-")
    print(flag_b)
