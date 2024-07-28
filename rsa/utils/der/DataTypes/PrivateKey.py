from pyasn1.type.namedtype import NamedType, NamedTypes
from pyasn1.type.univ import Integer, Sequence


class PrivateKey(Sequence):
    componentType = NamedTypes(
        NamedType('modulus', Integer()),
        NamedType('private_expoent', Integer()),
        NamedType('p', Integer()),
        NamedType('q', Integer()),
        NamedType('phi', Integer()),
    )


class Version(Integer):
    pass


class PrivateKeyRSA(Sequence):
    componentType = NamedTypes(
        NamedType('version', Version()),
        NamedType('modulus', Integer()),
        NamedType('publicExponent', Integer()),
        NamedType('privateExponent', Integer()),
        NamedType('prime1', Integer()),
        NamedType('prime2', Integer()),
        NamedType('exponent1', Integer()),
        NamedType('exponent2', Integer()),
        NamedType('coefficient', Integer()),
    )
