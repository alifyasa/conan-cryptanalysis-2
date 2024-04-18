from Crypto.Util.number import long_to_bytes, bytes_to_long, getStrongPrime, GCD
import random
import decimal


def solve_mode_e(rsa_n, rsa_e, ciphertext):
    """
    Easy tot n
    """

    rsa_tot = rsa_n - 1
    rsa_d = pow(rsa_e, -1, rsa_tot)

    plaintext = pow(ciphertext, rsa_d, rsa_n)
    plaintext = long_to_bytes(plaintext)

    return plaintext


def main():
    message_asli = "KRIPTOGRAFIITB{" + str(random.randint(1, 10000)) + "}"
    message_asli = message_asli.encode("utf-8")
    message_int = bytes_to_long(message_asli)

    n = getStrongPrime(1024)
    e = 65537
    enc = pow(message_int, e, n)

    print(message_asli)
    print(solve_mode_e(n, e, enc))


if __name__ == "__main__":
    main()
