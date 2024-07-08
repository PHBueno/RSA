from pyasn1.type.namedtype import NamedType, NamedTypes
from pyasn1.type.univ import Integer, Sequence


class PublicKey(Sequence):
    componentType = NamedTypes(
        NamedType('modulus', Integer()),
        NamedType('public_expoent', Integer()),
    )
