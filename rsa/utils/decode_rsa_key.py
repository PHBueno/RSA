from pyasn1.codec.der.decoder import decode

from rsa.utils.der.DataTypes.PrivateKey import PrivateKeyRSA


def decode_private_key(private_key_bytes: bytes):
    """
    Função utilizada para fazer o Decode de uma chave RSA privada.

    Arguments:
        private_key_bytes (bytes): A chave privada, em bytes.

    Returns:
        A chave privada decodificada.
    """
    decoded_priv_key, _ = decode(
        substrate=private_key_bytes, asn1Spec=PrivateKeyRSA()
    )
    return decoded_priv_key
