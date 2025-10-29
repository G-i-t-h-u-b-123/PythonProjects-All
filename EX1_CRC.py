def xor(a, b):
    # Perform bitwise XOR on two binary strings
    result = ""
    for i in range(len(b)):
        result += '0' if a[i] == b[i] else '1'
    return result
def crc_encode(data, divisor):
    n = len(divisor)
    data += '0' * (n - 1)  # Append zeros
    temp = data[:n]
    for i in range(n, len(data)):
        if temp[0] == '1':
            temp = xor(temp, divisor)[1:] + data[i]
        else:
            temp = xor('0' * n, temp)[1:] + data[i]
    # Final XOR after loop
    if temp[0] == '1':
        temp = xor(temp, divisor)[1:]
    else:
        temp = xor('0' * n, temp)[1:]
    crc = temp
    codeword = data[:-len(crc)] + crc
    return codeword, crc
def crc_check(codeword, divisor):
    n = len(divisor)
    temp = codeword[:n]
    for i in range(n, len(codeword)):
        if temp[0] == '1':
            temp = xor(temp, divisor)[1:] + codeword[i]
        else:
            temp = xor('0' * n, temp)[1:] + codeword[i]
    # Final XOR after loop
    if temp[0] == '1':
        temp = xor(temp, divisor)[1:]
    else:
        temp = xor('0' * n, temp)[1:]
    return temp == '0' * (n - 1)
# --- Main Program Loop ---
while True:
    data = input("\nEnter binary data (or 0 to exit): ")
    if data == '0':
        print("Exited.")
        break
    divisor = input("Enter divisor (e.g. 1101): ")
    # Encoding
    codeword, crc = crc_encode(data, divisor)
    print("Generated CRC:", crc)
    print("Codeword to send:", codeword)
    # Checking
    received = input("Enter received codeword to check: ")
    if crc_check(received, divisor):
        print("No error in received data.")
    else:
        print(" Error detected in received data.")