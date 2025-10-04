"""Custom decoding functions."""

import bitstring


def _reorder_bytes_by_significance(
    data: list[bitstring.Bits], significance_list: list[int]
) -> list[bitstring.Bits]:
    """Rearrange a list of byte-sized Bits chunks into MSB-first order based on a significance list."""
    num_bytes = len(data)
    result: list[bitstring.Bits | None] = [None] * num_bytes

    for stream_index, significance in enumerate(significance_list):
        final_position = num_bytes - 1 - significance
        result[final_position] = data[stream_index]

    return [chunk for chunk in result if chunk is not None]


def _physically_transform_bits(
    bits_obj: bitstring.BitStream,
    reverse_bits: bool = False,
    byte_significance_list: list[int] | None = None,
) -> bitstring.BitStream:
    """Apply physical transformations to a BitStream."""
    processed_bits = bits_obj

    if byte_significance_list:
        padded_len = (len(processed_bits) + 7) // 8 * 8
        if padded_len > len(processed_bits):
            processed_bits = (
                bitstring.BitStream(f"uint:{padded_len - len(processed_bits)}=0")
                + processed_bits
            )

        byte_chunks = list(processed_bits.cut(8))
        reordered_chunks = _reorder_bytes_by_significance(
            byte_chunks, byte_significance_list
        )
        processed_bits = bitstring.BitStream().join(reordered_chunks)

    if reverse_bits:
        bit_length = len(processed_bits)
        initial_int = processed_bits.uint
        binary_str = format(initial_int, f"0{bit_length}b")
        reversed_binary_str = binary_str[::-1]
        processed_bits = bitstring.BitStream(bin=reversed_binary_str)

    return processed_bits


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
        result += digit * power
        power *= 10
        value >>= 4
    return result


def _decode_unpacked_bcd(raw_value: int, bits: int) -> int:
    """Convert a raw integer from Unpacked Binary-Coded Decimal format."""
    result = 0
    power = 1
    num_bytes = bits // 8
    for _ in range(num_bytes):
        digit = raw_value & 0xFF
        result += digit * power
        power *= 10
        raw_value >>= 8
    return result
