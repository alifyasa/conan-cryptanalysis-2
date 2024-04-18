from Crypto.Util.number import long_to_bytes, bytes_to_long, getStrongPrime, GCD
import random
import decimal
from sympy import nextprime


def solve_mode_a(rsa_n, rsa_e, ciphertext):
    """
    p and q are close, so just find the sqrt and look
    around there
    """
    decimal.getcontext().prec = 500
    factor_guess = decimal.Decimal(rsa_n).sqrt()
    while True:
        factor_guess = nextprime(factor_guess)
        if rsa_n % factor_guess == 0:
            break

    rsa_q = factor_guess
    rsa_p = rsa_n // factor_guess

    rsa_tot = (rsa_p - 1) * (rsa_q - 1)
    rsa_d = pow(rsa_e, -1, rsa_tot)

    plaintext = pow(ciphertext, rsa_d, rsa_n)
    plaintext = long_to_bytes(plaintext)

    return plaintext


def main():
    message_asli = "KRIPTOGRAFIITB{" + str(random.randint(1, 10000)) + "}"
    message_asli = message_asli.encode("utf-8")
    message_int = bytes_to_long(message_asli)

    while True:
        ran = random.randint(1, 100)
        p = nextprime(getStrongPrime(1024) - ran)
        q = nextprime(nextprime(nextprime(nextprime(p) + ran) + ran) - ran)
        n = p * q
        e = 65537
        check = GCD(e, (p - 1) * (q - 1)) == 1
        if check:
            break

    enc = pow(message_int, e, n)
    print(message_asli)
    print(solve_mode_a(n, e, enc))


if __name__ == "__main__":
    main()
