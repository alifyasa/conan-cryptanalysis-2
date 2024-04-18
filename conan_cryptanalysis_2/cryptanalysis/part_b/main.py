from Crypto.Util.number import long_to_bytes, bytes_to_long, getStrongPrime, GCD
import random
import decimal
from sympy import nextprime


def solve(d, n, plaintext):
    e = pow(d, -1, tot)


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
