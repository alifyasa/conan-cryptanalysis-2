from Crypto.Util.number import long_to_bytes, bytes_to_long, getStrongPrime, GCD
import random
import decimal
from sympy import nextprime


def solve_mode_b(rsa_n, rsa_e, ciphertext):
    """
    p and q are close, so just find the sqrt and look
    around there
    """
    decimal.getcontext().prec = 500
    factor_guess = int(decimal.Decimal(rsa_n).sqrt())

    rsa_p = factor_guess

    # Because p ** 2, different totient function
    rsa_tot = (rsa_p - 1) * rsa_p
    rsa_d = pow(rsa_e, -1, rsa_tot)

    plaintext = pow(ciphertext, rsa_d, rsa_n)
    plaintext = long_to_bytes(plaintext)

    return plaintext


def main():
    message_asli = "KRIPTOGRAFIITB{" + str(random.randint(1, 10000)) + "}"
    message_asli = message_asli.encode("utf-8")
    message_int = bytes_to_long(message_asli)

    p = getStrongPrime(1024)
    n = p * p
    e = 65537
    enc = pow(message_int, e, n)

    print(message_asli)
    print(solve_mode_b(n, e, enc))


if __name__ == "__main__":
    main()
