# MDC Euclides:
# MDC(a=25, b=70)
# como a < b, então: a=70, b=25, dessa forma:
#################################
#   MDC(a=70, b=25)
# 70 = 25 * 2 + 20 => [20 é o resto]
#   MDC(70, 25) = MDC(25, 20)
# 25 = 20 * 1 + 5  => [5 é o resto]
#   MDC(25, 20) = MDC(20, 5)
# 20 = 5 * 3 + 5   => [5, é o resto]
#   MDC(20, 5) = MDC(5, 5)
# 5 = 5 * 1 + 0    => [0 é o resto]
#   MDC(5, 5) = MDC(5, 0) = 5
#################################


def mdc(a: int, b: int):
    """
    MDC utilizando algoritmo de euclides, onde MDC(a,b) = MDC(b,r),
    sendo 'r' o resto da divisão de a por b

    Attributes:
        a (int): O primeiro inteiro que será utilizado para o cálculo do MDC
        b (int): O segundo inteiro que será utilizado para o cálculo do MDC

    Returns:
        (int): O Máximo Divisor Comum entre 'a' e 'b'

    Examples:
        >>> mdc(12, 4)
        4

        >>> mdc(5, 9)
        1
    """
    if b > a:
        a, b = b, a

    # O objetivo é que esta condição seja atingida para que termine a recursividade
    if b == 0:
        return a
    r = a % b
    return mdc(a=b, b=r)
