from rsa.utils.GenPrimeNumber import generate_prime
from rsa.utils.MillerRabin import MillerRabin


def test_deve_retornar_num_com_quantidade_correta_de_bits():
    bits = 128
    prime = generate_prime(nbit=bits)
    prime_len = len(bin(prime)[2:])

    assert prime_len == bits


def test_deve_retornar_num_primo():
    bits = 128
    prime = generate_prime(nbit=bits)

    miller_rabin = MillerRabin()

    assert miller_rabin.verify(num=prime) == True
