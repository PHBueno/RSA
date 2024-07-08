from pyasn1.codec.der.decoder import decode
from pyasn1.error import PyAsn1Error
from pytest import raises

from rsa.core.RSA import RSA
from rsa.utils.der.DataTypes.PrivateKey import PrivateKey
from rsa.utils.der.DataTypes.PublicKey import PublicKey
from rsa.utils.MillerRabin import MillerRabin

# Gera as chaves para os testes
rsa = RSA(key_size=1024)
priv, pub = rsa.generate_keys()


def test_os_valores_p_e_q_da_chave_privada_devem_ser_primos():
    miller_rabin = MillerRabin()
    esperado = (True, True)

    priv_key_bytes = bytes.fromhex(str(priv))
    priv_key, _ = decode(priv_key_bytes, asn1Spec=PrivateKey())

    assert esperado == (
        miller_rabin.verify(int(priv_key['p'])),
        miller_rabin.verify(int(priv_key['q'])),
    )


def test_chave_privada_deve_ser_inverso_modular_da_chave_publica():
    esperado = 1

    # Decode de chave privada
    priv_key_bytes = bytes.fromhex(str(priv))
    priv_key, _ = decode(priv_key_bytes, asn1Spec=PrivateKey())

    # Decode de chave publica
    public_key_bytes = bytes.fromhex(str(pub))
    public_key, _ = decode(public_key_bytes, asn1Spec=PublicKey())

    phi = int(priv_key['phi'])
    private_expoent = int(priv_key['private_expoent'])
    public_expoent = int(public_key['public_expoent'])

    assert (private_expoent * public_expoent) % phi == esperado


def test_deve_cifrar_e_decifrar_a_mensagem():
    mensagem = 'teste cifra'

    cifra = rsa.cript(public_key=pub, msg=mensagem)
    msg_decifrada = rsa.dcript(private_key=priv, criptogram=cifra)

    assert mensagem == msg_decifrada


def test_deve_retornar_erro_se_a_chave_publica_nao_estiver_no_formato_correto():
    # hexadecimal incorreto
    pub_key = '82010a02820101009686ab71705c873a381e3eb9ada1cbb2149788e3ab1f403dc4146b1a179938bbac521ff6286439f5938c1d5888a69dc3f1e3fef169dfc4ab285a9e7195576cdecf902eb0fa1fb62a8146e4a87aac8aec42842a5d972c659010dbde7384ebb666b14804ddf15445f04087c1afb38b9e576f74caf3f569d81d746ae2f2dfc827c202170aee55640adeb2475453be395ce9e7aedaa7a5d9de97eacbe390958b6e82f58a8c7d28edbba285057c7375062d66125938444675cc68513c0348c752caf5cb8ef8d4de3aa4e444cef40c2c30a68b3693761ec0445ade25d5885fa14e66ab04bb9be6806397ae09f638bd64fa52213df2dad8eb6d9be870c8aba1cbb7c40f0203010001'

    msg_erro = 'A chave não está no formato DER esperado!'

    with raises(PyAsn1Error) as error:
        result = rsa.cript(public_key=pub_key, msg='teste')

    assert msg_erro == error.value.args[0]


def test_deve_retornar_erro_se_a_chave_privada_nao_estiver_no_formato_correto():
    # hexadecimal incorreto
    private_key = '82041602820101009686ab71705c873a381e3eb9ada1cbb2149788e3ab1f403dc4146b1a179938bbac521ff6286439f5938c1d5888a69dc3f1e3fef169dfc4ab285a9e7195576cdecf902eb0fa1fb62a8146e4a87aac8aec42842a5d972c659010dbde7384ebb666b14804ddf15445f04087c1afb38b9e576f74caf3f569d81d746ae2f2dfc827c202170aee55640adeb2475453be395ce9e7aedaa7a5d9de97eacbe390958b6e82f58a8c7d28edbba285057c7375062d66125938444675cc68513c0348c752caf5cb8ef8d4de3aa4e444cef40c2c30a68b3693761ec0445ade25d5885fa14e66ab04bb9be6806397ae09f638bd64fa52213df2dad8eb6d9be870c8aba1cbb7c40f028201002c95ef2a46b1e18c291b2c512b510558d6289c6f733c6a76e1217b27db5d932463c25f9d361199e957aee4f25867a1cb6c56b02929c71225f06a070c75c3d3879bcb8548fe8d6e13e0fef2b3c4c25ed3e44fe98c973e9b46b4f7ab486452bd5065aa83668a19002e4daee87bf69ea0641dab6682246b198c7ff3390ddfa315c336ca39cea11587207ce935367aef0a81da00d90353a371a2d14231c6cee7c6d3094f1b3f924e8677c413a7100d989b89872ae4d179245943351d24414ffd78f16dba3f4d1c9b03eb15b0d4b8987d321265b63617d943f576d677b377836eb12eb497df5d55e7090b65f43086f4bcf8709289d7fd2887b9b877e69bf81825050102818100a00d96bd4c588256fbdf160c33940360b6b8f7fe9ca68da9f196c58cfff251123452d3fa79136673fff40fc665aeb7e31b5bc3de10bcd057fcd0265ed7ffa2977830106a9082e8e7ecb8ab83e57279990dc72995c0de273b49baa7009e118ba6590804a4feee32fd98a5681230900b505467a5c06f4d3bdab8339704c9cab0ef02818100f0c30609541b839903aa34e4d7bf63c1ff494c28e53d95f35e5ecd9bc2fb867bac244d130baa1bb4af3943453ccddeab2d94e7132774b17adaee74c04fa9f92bc14ece275d2c0b081618c897b76526ac87f3dd5ca48312bc495f0fcd61ca7bc8d3ea9c4dd52b58503cfe042a3650ad4a6938c6f708b226216db03239410ddee102820101009686ab71705c873a381e3eb9ada1cbb2149788e3ab1f403dc4146b1a179938bbac521ff6286439f5938c1d5888a69dc3f1e3fef169dfc4ab285a9e7195576cdecf902eb0fa1fb62a8146e4a87aac8aec42842a5d972c659010dbde7384ebb666b14804ddf15445f04087c1afb38b9e576f74caf3f569d81d746ae2f2dfc827c071466e27b4f004eeb2be0962b2e5f5c731ac968023f5bafa9ad65067d29d96f515136b6fa4303979d5d82967d28996d7c9688d530e444a95797d68299fa92f3292101a42f08bb0f441fd7ff08f590645a0d86f2c5ae320e692bbd191a1725f3bd7c8faf3ac4a0c603452cc80fe19998680526e21736e39ec4ae4e263c0df3440'

    criptogram = 16601668630267949303255594344321264545900408807766060777196226779934432329855123280151504564693091189898219989061783660509409674732099957026063957959679722909701823424534423829796831537862086278819232926109549696636553857249838427032694474591464468599435253813817433859577286898368096100692719961206475848628423561180561953985413870601515166600321849016424489490169021537014509391431119896089797062111832564746119154566324265899879391935428885932892457150951386845380994007881818679169877150272136505785814798740189777384672190038665203535676244014664828156171717041592892803588020184794378781402624833421210134728420
    msg_erro = 'A chave não está no formato DER esperado!'

    with raises(PyAsn1Error) as error:
        result = rsa.dcript(private_key=private_key, criptogram=criptogram)

    assert msg_erro == error.value.args[0]
