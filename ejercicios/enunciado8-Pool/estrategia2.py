import multiprocessing as mp

def es_primo(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def main(): #Con pool de hilos

    pool = mp.Pool(mp.cpu_count())

    #Lista de números del 2 al 99
    numbers = list(range(2, 101))

    primos = []

    primos = pool.map(es_primo, numbers)

    for primo in primos:
        if primo:
            print(primo)

if __name__ == "__main__":
    main()
