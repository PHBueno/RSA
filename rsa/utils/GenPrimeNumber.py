from random import randint

from rsa.utils.MillerRabin import MillerRabin


def generate_prime(nbit: int) -> int:
    """
    Gera número primo com validação do teste de Miller Rabin

    Arguments:
        nbit (int): Número de bits para o número primo

    Returns:
        Número primo que foi gerado
    """
    num = randint(1 + 2 ** (nbit - 1), 2**nbit)
    miller_rabin = MillerRabin(iterations=3)
    prime = miller_rabin.verify(
        num=num
    )  # Executa a verificação de MillerRabin

    # Enquanto não for primo incrementa o número gerado e executa o teste de primalidade
    while not prime:
        num += 1
        prime = miller_rabin.verify(num=num)
    return num
