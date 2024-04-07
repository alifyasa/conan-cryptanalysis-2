import re
import socket

def get_all_messages(recv_socket: socket.socket, stop_str = "Jawaban = ", print_message = False):
    msg = ''
    while True:
        msg_part = recv_socket.recv(1024).decode()
        if msg_part and print_message: print(msg_part)
        msg += msg_part
        if stop_str is not None and stop_str in msg:
            break
    return msg

CHALLENGE_PATTERN = r'paket_soal = ([A-E])\s*n = (\d*)\s*e = (\d*)\s*c = (\d*)'

def get_challenge(recv_socket: socket.socket):
    question = get_all_messages(recv_socket)
    print(question, end='')

    paket_soal, rsa_n, rsa_e, ciphertext = re.search(CHALLENGE_PATTERN, question).groups()

    rsa_n = int(rsa_n)
    rsa_e = int(rsa_e)
    ciphertext = int(ciphertext)

    return paket_soal, rsa_n, rsa_e, ciphertext

ACCESS_TOKEN_PATTERN = r'Token akses nomor arsip: (\d*)'
def get_access_token(recv_socket: socket.socket):
    msg = get_all_messages(recv_socket, "Masukkan perintah: ")
    access_token = re.search(ACCESS_TOKEN_PATTERN, msg).group(1)
    return int(access_token)