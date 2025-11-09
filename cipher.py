#Task 1: Encryption Function
def encrypt(inputText, N, D):
    encryptedText = ""
    
    # Define ASCII printable range excluding space (32) and '!' (33)
    ASCII_START = 34
    ASCII_END = 126
    
    if N < 1 or D not in (1, -1):
        raise ValueError("Invalid N or D")
    
    # Reverse the input text
    reversed_text = inputText[::-1]
    for c in reversed_text:
        code = ord(c)
        if code < ASCII_START or code > ASCII_END:
            raise ValueError(f"Invalid character '{c}' in inputText")
        # Shift
        shifted = code + D * N
        # Wrap around
        while shifted > ASCII_END:
            shifted = ASCII_START + (shifted - ASCII_END - 1)
        while shifted < ASCII_START:
            shifted = ASCII_END - (ASCII_START - shifted - 1)
        encryptedText += chr(shifted)
        
    return encryptedText

#Task 2: Decryption Function
def decrypt(inputText, N, D):
    decryptedText = ""
    # Define ASCII printable range excluding space (32) and '!' (33)
    ASCII_START = 34
    ASCII_END = 126

    if N < 1 or D not in (1, -1):
        raise ValueError("Invalid N or D")

    shifted_chars = []
    for c in inputText:
        code = ord(c)
        if code < ASCII_START or code > ASCII_END:
            raise ValueError(f"Invalid character '{c}' in inputText")
        # Reverse the shift
        shifted = code - D * N
        # Wrap around
        while shifted > ASCII_END:
            shifted = ASCII_START + (shifted - ASCII_END - 1)
        while shifted < ASCII_START:
            shifted = ASCII_END - (ASCII_START - shifted - 1)
        shifted_chars.append(chr(shifted))
    # Reverse the shifted result to get the original text
    decryptedText = ''.join(shifted_chars)[::-1]
    
    return decryptedText