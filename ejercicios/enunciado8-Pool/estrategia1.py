import multiprocessing as mp

def es_primo(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def main(): #Con pool de procesos
    pool = mp.Pool()

    #Lista de números del 2 al 99
    numbers = list(range(2, 101))

    num_primos = []

    num_primos = pool.map(es_primo, numbers)

    for primo in num_primos:
        if primo:
            print(primo)

if __name__ == "__main__":
    main()
