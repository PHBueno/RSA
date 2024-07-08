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
