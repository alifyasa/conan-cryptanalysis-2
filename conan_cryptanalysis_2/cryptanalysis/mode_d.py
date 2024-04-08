from Crypto.Util.number import long_to_bytes, bytes_to_long, getStrongPrime, GCD
import random
import decimal


def solve_mode_d(_, rsa_e, ciphertext):
    """
    small e
    """

    decimal.getcontext().prec = 1000
    plaintext = decimal.Decimal(ciphertext) ** (
        decimal.Decimal(1) / decimal.Decimal(rsa_e)
    )
    plaintext = int(plaintext.to_integral())
    plaintext = long_to_bytes(plaintext)

    return plaintext


def main():
    message_asli = "KRIPTOGRAFIITB{" + str(random.randint(1, 10000)) + "}"
    message_asli = message_asli.encode("utf-8")
    message_int = bytes_to_long(message_asli)

    p = getStrongPrime(1024)
    q = getStrongPrime(1024)
    n = p * q
    e = 3
    enc = pow(message_int, e, n)

    print(message_asli)
    print(solve_mode_d(n, e, enc))


if __name__ == "__main__":
    main()
