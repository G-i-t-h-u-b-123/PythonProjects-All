def calculate_parity(bits, positions):
    parity = 0
    for pos in positions:
        parity ^= int(bits[pos - 1])  # XOR all selected bits
    return parity

def hamming_encode(data_bits):
    # Ensure input is 4 bits
    if len(data_bits) != 4 or not all(bit in '01' for bit in data_bits):
        raise ValueError("Input must be 4-bit binary string.")

    # Initialize 7-bit list with placeholders
    codeword = ['0'] * 7

    # Place data bits into positions 3, 5, 6, 7 (1-based indexing)
    codeword[2] = data_bits[0]  # D1
    codeword[4] = data_bits[1]  # D2
    codeword[5] = data_bits[2]  # D3
    codeword[6] = data_bits[3]  # D4

    # Calculate parity bits
    codeword[0] = str(calculate_parity(codeword, [1, 3, 5, 7]))  # P1
    codeword[1] = str(calculate_parity(codeword, [2, 3, 6, 7]))  # P2
    codeword[3] = str(calculate_parity(codeword, [4, 5, 6, 7]))  # P4

    return ''.join(codeword)

def hamming_decode(codeword):
    if len(codeword) != 7 or not all(bit in '01' for bit in codeword):
        raise ValueError("Codeword must be 7-bit binary string.")

    bits = list(codeword)
    # Recalculate parity checks
    p1 = calculate_parity(bits, [1, 3, 5, 7])
    p2 = calculate_parity(bits, [2, 3, 6, 7])
    p4 = calculate_parity(bits, [4, 5, 6, 7])

    # Find error position
    error_pos = p1 * 1 + p2 * 2 + p4 * 4

    if error_pos != 0:
        print(f"Error detected at position: {error_pos}")
        # Correct the bit
        bits[error_pos - 1] = '1' if bits[error_pos - 1] == '0' else '0'
        print("Corrected Codeword:", ''.join(bits))
    else:
        print("No error detected.")

    # Extract original data bits: positions 3, 5, 6, 7
    data_bits = bits[2] + bits[4] + bits[5] + bits[6]
    return data_bits

# --- MAIN PROGRAM ---
data = input("Enter 4-bit data (e.g., 1011): ")
encoded = hamming_encode(data)
print("Encoded Hamming Code (7,4):", encoded)

received = input("Enter received 7-bit codeword: ")
decoded = hamming_decode(received)
print("Decoded original 4-bit data:", decoded)
