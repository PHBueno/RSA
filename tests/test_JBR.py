from pytest import mark, raises

from rsa.utils.JBR import JBR


def test_deve_retornar_1_ao_multiplicar_o_inverso_modular_por_num():
    esperado = 1
    modulo = 256
    num = 179

    jbr = JBR(mod=modulo)
    inverso_modular = jbr.invMod(num=num)

    assert (inverso_modular * num) % modulo == esperado


@mark.parametrize(
    'num,mod,esperado', [(7, 2, 1), (123, 56, 51), (315, 256, 243)]
)
def test_deve_retornar_o_inverso_modular_de_num(num, mod, esperado):
    jbr = JBR(mod=mod)

    result = jbr.invMod(num=num)

    assert result == esperado


@mark.parametrize('num,mod', [(315, 560), (0, 256), (250, 315)])
def test_deve_retornar_erro_para_num_sem_inverso_modular(num, mod):
    msg_error = 'Não existe inverso modular para o valor informado'

    jbr = JBR(mod=mod)

    with raises(ZeroDivisionError) as error:
        result = jbr.invMod(num=num)
    assert msg_error == error.value.args[0]
