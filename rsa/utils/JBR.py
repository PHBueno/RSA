class JBR:
    """
    Classe utilizada para relização do cálculo de inverso modular, baseado no algoritmo JBR desenvolvido pelo Doutor Joacil Basílio Rael.
    O algoritmo é baseado em uma releitura do Algoritmo Estentido de Euclides.

    Attributes:
        mod (int): O módulo para o cálculo de inverso modular, maior que 1
    """

    def __init__(self, mod: int) -> None:
        self.mod = mod
        self.original_mod = mod
        self.j, self.b, self.count = 0, 1, 1

    def invMod(self, num: int) -> int:
        """
        Realiza as rodadas do algoritmo JBR.

        Attributes:
            num (int): O número que se deseja saber o inverso modular, maior que 1

        Returns:
            (int): O inverso modular de 'num % mod'

        Examples:
            >>> JBR(mod=256).invMod(num=123)
            179
        """

        if num == 0:
            raise ZeroDivisionError(
                'Não existe inverso modular para o valor informado'
            )

        resto = self.mod % num
        r = self.mod // num

        inv = self.j + self.b * r

        if resto == 1:
            return (
                ((-1) ** self.count) * inv + self.original_mod
            ) % self.original_mod

        self.j, self.b, self.mod = self.b, inv, num
        self.count += 1
        return self.invMod(num=resto)
