from Crypto.Util.number import long_to_bytes, bytes_to_long, getStrongPrime, GCD
import random


def solve_mode_c(rsa_n, _, ciphertext):
    """
    It's just 2 ** 15, we can bruteforce it
    """

    for e_guess in range(2**15, 2**16 + 1):
        plaintext = pow(ciphertext, e_guess, rsa_n)
        plaintext = long_to_bytes(plaintext)
        if "KRIPTOGRAFIITB".encode() in plaintext:
            break

    return plaintext


def main():
    message_asli = "KRIPTOGRAFIITB{" + str(random.randint(1, 10000)) + "}"
    message_asli = message_asli.encode("utf-8")
    message_int = bytes_to_long(message_asli)

    while True:
        p = getStrongPrime(1024)
        q = getStrongPrime(1024)
        e = random.randrange(1, 65537)
        n = p * q
        tot = (p - 1) * (q - 1)
        e = random.randint(2**15, 2**16)
        check = GCD(e, (p - 1) * (q - 1)) == 1
        if check:
            break

    d = pow(e, -1, tot)
    enc = pow(message_int, d, n)
    e = d

    print(message_asli)
    print(solve_mode_c(n, e, enc))


if __name__ == "__main__":
    main()
