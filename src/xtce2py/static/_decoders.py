"""Custom decoders."""


def _reverse_bits(n: int, bit_length: int) -> int:
    """Reverses the order of the first `bit_length` bits of an integer."""
    binary_str = format(n, f"0{bit_length}b")
    reversed_binary_str = binary_str[::-1]
    return int(reversed_binary_str, 2)


def _decode_ones_complement(value: int, bits: int) -> int:
    """Convert a raw integer from ones' complement format."""
    if (value >> (bits - 1)) & 1:  # Check if the sign bit is 1
        return -((1 << bits) - 1 - value)
    return value


def _decode_sign_magnitude(value: int, bits: int) -> int:
    """Convert a raw integer from sign-magnitude format."""
    sign_bit = (value >> (bits - 1)) & 1
    magnitude = value & ((1 << (bits - 1)) - 1)
    return -magnitude if sign_bit else magnitude


def _decode_packed_bcd(value: int, bits: int) -> int:
    """Convert a raw integer from Packed Binary-Coded Decimal format."""
    result = 0
    power = 1
    # Number of 4-bit nibbles
    num_nibbles = bits // 4
    for _ in range(num_nibbles):
        digit = value & 0x0F
        if digit > 9:
            # This would typically be an error condition
            return -1  # Invalid BCD digit
        result += digit * power
        power *= 10
        value >>= 4
    return result
