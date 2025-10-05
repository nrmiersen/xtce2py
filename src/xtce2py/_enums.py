"""Common enumerations."""

from enum import Enum


class Endianness(str, Enum):
    """Enumeration for byte order (endianness)."""

    BIG = "be"
    LITTLE = "le"

    def __str__(self) -> str:
        """Return the string representation of the enum value."""
        return self.value


class FinalDataType(str, Enum):
    """Enumeration for the final Python data types a parameter can represent."""

    INT = "int"
    FLOAT = "float"
    STRING = "str"
    BINARY = "bytes"
    BOOLEAN = "bool"

    def __str__(self) -> str:
        """Return the string representation of the enum value."""
        return self.value


class BitstreamInterpretationToken(str, Enum):
    """Enumeration for bitstring property names used for reading values."""

    # Unsigned integers
    UINT = ".uint"
    UINTBE = ".uintbe"  # Big-endian unsigned integer
    UINTLE = ".uintle"  # Little-endian unsigned integer
    UINTNE = ".uintne"  # Native-endian unsigned integer

    # Signed integers
    INT = ".int"
    INTBE = ".intbe"  # Big-endian signed integer
    INTLE = ".intle"  # Little-endian signed integer
    INTNE = ".intne"  # Native-endian signed integer

    # Floating point
    FLOAT = ".float"  # IEEE 754 double (64-bit)
    FLOATBE = ".floatbe"  # Big-endian float (64-bit)
    FLOATLE = ".floatle"  # Little-endian float (64-bit)
    FLOATNE = ".floatne"  # Native-endian float (64-bit)

    # Binary data
    BITS = ".bits"  # Raw bits
    BYTES = ".bytes"  # Raw bytes
    BIN = ".bin"  # Binary string representation
    HEX = ".hex"  # Hexadecimal string representation
    OCT = ".oct"  # Octal string representation

    # Boolean
    BOOL = ".bool"  # Boolean value

    def __str__(self) -> str:
        """Return the string representation of the enum value."""
        return self.value
