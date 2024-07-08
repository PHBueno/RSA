from pytest import mark, raises

from rsa.utils.MillerRabin import MillerRabin


@mark.parametrize(
    'num,iterations,esperado',
    [(3, 1, True), (7, 3, True), (13, 3, True), (17, 3, True)],
)
def test_deve_retornar_true_para_numeros_primos(num, iterations, esperado):
    miller_rabin = MillerRabin(iterations=iterations)
    assert miller_rabin.verify(num) == esperado


@mark.parametrize(
    'num,iterations,esperado',
    [(4, 3, False), (8, 3, False), (22, 3, False), (124, 3, False)],
)
def test_deve_false_para_numeros_pares(num, iterations, esperado):
    miller_rabin = MillerRabin(iterations=iterations)
    assert miller_rabin.verify(num=num) == esperado


def test_deve_retornar_erro_para_iterations_nao_impar():
    msg_erro = "O valor de 'iterations' precisa ser ímpar."

    with raises(Exception) as error:
        miller_rabin = MillerRabin(iterations=4)
    assert msg_erro == error.value.args[0]


def test_deve_retornar_erro_para_iterations_maior_ou_igual_a_num():
    num = 3
    iterations = 3
    msg_erro = f"O valor de 'iterations' deve ser menor que {num}."

    miller_rabin = MillerRabin(iterations=iterations)

    with raises(Exception) as error:
        miller_rabin.verify(num=num)
    assert msg_erro == error.value.args[0]
