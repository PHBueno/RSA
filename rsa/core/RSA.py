from typing import Dict, Tuple

from pyasn1.codec.der.decoder import decode
from pyasn1.codec.der.encoder import encode
from pyasn1.error import PyAsn1Error

from rsa.utils.der.DataTypes.PrivateKey import PrivateKey
from rsa.utils.der.DataTypes.PublicKey import PublicKey
from rsa.utils.GenPrimeNumber import generate_prime
from rsa.utils.JBR import JBR
from rsa.utils.logging.config import log


class RSA:
    def __init__(self, key_size: int = 1024):
        self.key_size = key_size

    def __generate_private_exp(self, phi: int, public_exp: int) -> int:
        """
        Método privado para calcular o valor do expoente privado.

        Arguments:
            phi (int): O valor do Totiente de Euler para 'n'
            public_exp (int): O expoente público

        Returns:
            O valor do expoente privado
        """
        jbr = JBR(mod=phi)
        d = jbr.invMod(num=public_exp)
        return d

    def der_public_key(self, public_infos: Dict[str, int]) -> str:
        """
        Método estático utilizado para converter as informações da chave pública par o formato DER

        Arguments:
            public_infos (Dict[str, int]): Um dicionário com as informações da chave pública

        Returns:
            Um hexadecimal com a chave codificada com DER
        """
        pub_key = PublicKey()

        pub_key['modulus'] = public_infos['n']
        pub_key['public_expoent'] = public_infos['e']

        public_key_encode = encode(pub_key)

        return public_key_encode.hex()

    def der_private_key(self, private_infos: Dict[str, int]) -> str:
        """
        Método estático utilizado para converter as informações da chave privada para o formato DER

        Arguments:
            private_infos (Dict[str, int]): Um dicionário com as informações da chave privada

        Returns:
           Um hexadecimal com a chave codificada com DER
        """
        priv_key = PrivateKey()

        priv_key['modulus'] = private_infos['n']
        priv_key['private_expoent'] = private_infos['d']
        priv_key['p'] = private_infos['p']
        priv_key['q'] = private_infos['q']
        priv_key['phi'] = private_infos['phi']

        private_key_encode = encode(priv_key)

        return private_key_encode.hex()

    def generate_keys(self, public_exp: int = 65537) -> Tuple[str, str]:
        """
        Método utilizado para gerar as chaves pública e privada do RSA.

        Arguments:
            public_exp (int): O valor para o expoente público

        Returns:
            Tuple[str, str]: Os pares de chaves pública e privada, codificadas em hexadecimal.
        """

        # Gera números primos
        p = generate_prime(nbit=self.key_size)
        q = generate_prime(nbit=self.key_size)

        n = p * q  # Calcula o módulo
        phi = (p - 1) * (q - 1)

        e = public_exp  # TODO: Adicionar verificação via MDC;

        d = self.__generate_private_exp(
            phi=phi, public_exp=e
        )  # Calcula o expoente privado

        # Converte chaves para o formato DER
        public_key = self.der_public_key(public_infos={'e': e, 'n': n})
        private_key = self.der_private_key(
            private_infos={'d': d, 'n': n, 'p': p, 'q': q, 'phi': phi}
        )

        # TODO: estudar o retorno de um dict ao invés de tupla
        return private_key, public_key

    def cript(self, public_key: str, msg: str) -> int:
        """
        Método utilizado para realizar a cifração de uma mensagem

        Attributes:
            public_key (str): Uma string hexadecimal com a chave codificada em DER
            msg (str): A mensagem que se deseja cifrar

        Returns:
            O Criptograma resultante da cifração
        """
        # Converte a mensagem para hexadecimal
        msg_to_hex = msg.encode().hex()
        _pub_key = bytes.fromhex(public_key)

        try:
            pub_key, _ = decode(_pub_key, asn1Spec=PublicKey())
        except PyAsn1Error:
            log.error('A chave não está no formato DER esperado!')
            raise PyAsn1Error('A chave não está no formato DER esperado!')

        public_exp, mod = (
            int(pub_key['public_expoent']),
            int(pub_key['modulus']),
        )

        return pow(base=int(msg_to_hex, 16), exp=public_exp, mod=mod)

    def dcript(self, private_key: str, criptogram: int) -> str:
        """
        Método utilizado para realizar a decifração de um criptograma

        Attributes:
            private_key (str): Uma string hexadecimal com a chave codificada em DER
            criptogram (int): O Criptograma que se deseja decifrar

        Returns:
            O texto plano
        """
        _priv_key = bytes.fromhex(private_key)

        try:
            priv_key, _ = decode(_priv_key, asn1Spec=PrivateKey())
        except PyAsn1Error:
            log.error('A chave não está no formato DER esperado!')
            raise PyAsn1Error('A chave não está no formato DER esperado!')

        private_exp, mod = (
            int(priv_key['private_expoent']),
            int(priv_key['modulus']),
        )

        msg_dcript = pow(base=criptogram, exp=private_exp, mod=mod)
        msg_to_hex = hex(msg_dcript)[2:]

        return bytes.fromhex(msg_to_hex).decode()
