from mode_a import solve_mode_a
from mode_b import solve_mode_b
from mode_c import solve_mode_c
from mode_d import solve_mode_d
from mode_e import solve_mode_e

def solve(rsa_n, rsa_e, ciphertext, version):
    if version == "a":
        return solve_mode_a(rsa_n, rsa_e, ciphertext)
    elif version == "b":
        return solve_mode_b(rsa_n, rsa_e, ciphertext)
    elif version == "c":
        return solve_mode_c(rsa_n, rsa_e, ciphertext)
    elif version == "d":
        return solve_mode_d(rsa_n, rsa_e, ciphertext)
    elif version == "e":
        return solve_mode_e(rsa_n, rsa_e, ciphertext)

def main():
    print("select version mode: ")
    mode = input("Paket Mode: ")
    n = int(input("n: "))
    e = int(input("c: "))
    ciphertext = int(input("ciphertext: "))

    ans = solve(n, e, ciphertext, mode)
    print("Solution: "+ str(ans))


if __name__ == "__main__":
    main()