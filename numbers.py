from random import randint

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5) + 2, 2):
        if num % n == 0:
            return False
    return True


def get_prime_nmber(max_value=10000):
    result = None
    while result is None or not is_prime(result):
        result = randint(10, max_value)


    return result

def get_prmitive_root(p):
    required_set = set(num for num in range(1, p) if gcd(num, p) == 1)
    for g in range(1, p):
        actual_set = set(pow(g, powers) % p for powers in range(1, p))
        if required_set == actual_set:
            return g


