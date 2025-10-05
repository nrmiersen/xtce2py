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


def _transform_bits(
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


def _decode_milstd_1750a(bits_obj: bitstring.BitStream, bits: int) -> float:
    """Convert a raw BitStream from MIL-STD-1750A floating-point format."""
    if bits == 32:
        # 32-bit Format: Sign (1) | Mantissa (23) | Exponent (8)
        sign_bit = bits_obj[0]
        mantissa_bits = bits_obj[1:24].uint
        exponent = bits_obj[24:32].int  # Exponent is a signed 8-bit integer

        # Handle special case of zero first
        # "A special case of mantissa and exponent both equal to zero is also allowed"
        # This only applies when sign is positive (0.0, not -0.0 or other cases)
        if not sign_bit and mantissa_bits == 0 and exponent == 0:
            return 0.0

        # MIL-STD-1750A uses 2's complement mantissa representation
        # The 23 bits represent the fractional part of a 24-bit 2's complement number
        # Format: 0.F where F is the 23-bit fraction

        # Reconstruct the full 24-bit mantissa with implicit leading bit
        if sign_bit:
            # For negative numbers: implicit leading bit is 1
            # Full 24-bit value: 1.{23 bits} in 2's complement
            full_mantissa_bits = (1 << 23) | mantissa_bits
            # Convert from 2's complement 24-bit to float in range [-1, -0.5)
            mantissa_val = -(2**24 - full_mantissa_bits) / (2**23)
        else:
            # For positive numbers: implicit leading bit is 0
            # Full 24-bit value: 0.{23 bits} in 2's complement
            # This gives us values in range [0, 1), but we need [0.5, 1)
            # So the MSB of the 23 bits must be 1 for normalization
            mantissa_val = mantissa_bits / (2**23)
    else:
        raise ValueError(f"Unsupported MIL-STD-1750A size: {bits} bits. Must be 32.")

    return mantissa_val * (2**exponent)


def _decode_float128(bits_obj: bitstring.BitStream, bits: int) -> float:
    """Convert a raw BitStream from IEEE 754 quad-precision (128-bit) format."""
    if bits != 128:
        raise ValueError(f"float128 decoder only supports 128-bit format, got {bits}")

    # Extract IEEE 754 binary128 components: Sign (1) | Exponent (15) | Mantissa (112)
    int_val = int.from_bytes(bits_obj.bytes, byteorder="big")
    sign = (int_val >> 127) & 1
    exponent = (int_val >> 112) & 0x7FFF
    mantissa = int_val & ((1 << 112) - 1)

    # Handle special cases
    if exponent == 0x7FFF:
        return float("-inf" if sign else "inf") if mantissa == 0 else float("nan")
    if exponent == 0 and mantissa == 0:
        return -0.0 if sign else 0.0

    # Convert to float
    if exponent == 0:
        # Subnormal number
        value = mantissa * (2 ** (-16382 - 112))
    else:
        # Normal number
        actual_exp = exponent - 16383
        mantissa_val = 1.0 + (mantissa / (1 << 112))
        value = mantissa_val * (2**actual_exp)

    return -value if sign else value
