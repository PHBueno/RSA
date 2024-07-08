from functools import wraps
from typing import Dict, List, Tuple


def is_prime(func):
    """
    Decorator utilizado para retornar True ou False para números primos e compostos

    Arguments:
        func (function): A função original que será decorada

    Returns:
        function: A função decorada com o retorno modificado
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper utilizado para modificação da função decorada

        Arguments:
            *args (args): Argumentos não nomeados da função principal
            **kwargs (kwargs): Argumentos nomeados da função principal

        Returns:
            Um booleano indicando se o valor é primo ou não
        """
        test = func(*args, **kwargs)
        return False if 0 in test.values() else True

    return wrapper


class MillerRabin:
    """
    Classe utilizada para realizar o teste de Miller Rabin para verificação de números primos grandes

    Attributes:
        iterations (int): Quantidade de iterações que o teste irá realizar
    """

    def __init__(self, iterations: int = 3):
        self.iterations = iterations

        if self.iterations % 2 == 0:
            raise Exception("O valor de 'iterations' precisa ser ímpar.")

    def _factorization(self, num: int) -> Tuple[int, int]:
        """
        Realiza a fatorização de 'num', ímpar, para a execução do teste de Miller Rabin. O resultado obtido é 'num-1 = (2 ^ exp) * multiple'

        Attributes:
            num (int): O número que será verificado

        Returns:
            Tuple[int, int]: Uma tupla contendo o expoente e o valor resultante da divisão por todas as bases possíveis de 2.

        Examples:
            >>> MillerRabin(3)._factorization(7)
            (1, 3)

            >>> MillerRabin(3)._factorization(13)
            (2, 3)
        """
        exp = 0
        multiple = num - 1
        while multiple % 2 == 0:
            exp += 1
            multiple = multiple // 2
        return exp, multiple

    def _pseudorandom_base(self, num: int) -> List[int]:
        """
        Realiza a escolha de número pseudo aleatórios entre 2 e num - 1, sem repetir os números já escolhidos.

        Attributes:
            num (int): O número que será verificado

        Returns:
            List[int]: Uma lista com os inteiros pseudoaleatórios
        """
        from random import randint

        count = 0
        rand_list = list()
        while True:
            rand_num = randint(2, num - 1)
            if rand_num not in rand_list:
                rand_list.append(rand_num)
                count += 1
            if count == self.iterations:
                break
        return rand_list

    @is_prime
    def verify(self, num):
        """
        Realiza as rodadas e verificações do teste de Miller Rabin, modificado pelo decorator `is_prime`.

        O decorator `is_prime` modifica a função principal retornando True para números primos e False para números compostos.

        Arguments:
            num (int): O número que será verificado

        Returns:
            Bool: True para números primos e False para números compostos.

        Examples:
            >>> MillerRabin(3).verify(7)
            True

            >>> MillerRabin(3).verify(233)
            True

            >>> MillerRabin(3).verify(235)
            False
        """
        if num % 2 == 0:
            return {0: 0}

        if self.iterations >= num:
            raise Exception(
                f"O valor de 'iterations' deve ser menor que {num}."
            )

        s, d = self._factorization(num=num)  # s = exp, d = multiplo
        prime = dict()
        rand_list = self._pseudorandom_base(num=num)

        for i in range(self.iterations):
            # Escolha da base 'a', pseudoaleatória na iteração 'i'.
            a = rand_list[i]
            x = pow(a, d, num)

            # Se o resultado da primeira iteração com base "a", não for 1, ou -1
            if x not in (1, -1 % num):
                for j in range(s):
                    x = pow(x, 2, num)
                    # "X" é uma raiz quadrada não trivial de "num"
                    # Número que, ao ser elevado ao quadrado e reduzido módulo "num", resulta em -1.

                    if x == -1 % num:  # É primo
                        prime[a] = 1
                        break
                    else:
                        prime[a] = 0  # Não é primo
            else:
                prime[a] = 1
        return prime
