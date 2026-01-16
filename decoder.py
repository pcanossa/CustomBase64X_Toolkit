import json

alphabet=input(
    "Informe o alfabeto custom a ser utilizado\n"
    "(exemplo: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=),\n"
    "ou pressione Enter para o alfabeto padrão RFC4648: "
    )

if alphabet=="":
    alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

data = input("\nInforme o arquivo com o texto codificado em base64: ")

decoded_bytes = bytearray()
decoded_dict = {}

with open(data, "r") as file:
    for line in file:
        token = line.strip()

        # Remove lixo estrutural comum em arrays JS/JSON
        token = token.strip('",[]')

        # Filtro 1: tamanho mínimo
        if len(token) < 6:
            continue

        # Filtro 2: caracteres válidos no alfabeto
        if any(char not in alphabet for char in token):
            continue

        # Base64 custom decode
        bits = ""
        try:
            for char in token:
                index = alphabet.index(char)
                bits += f"{index:06b}"
        except ValueError:
            # caractere fora do alfabeto (fallback de segurança)
            continue

        current_token_bytes = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                break
            val = int(byte, 2)
            decoded_bytes.append(val)
            current_token_bytes.append(val)

        decoded_dict[token] = current_token_bytes.decode("utf-8", errors="ignore")

with open("decoded_output.bin", "wb") as output_file:
    output_file.write(decoded_bytes)

with open("decoded_formatted.json", "w") as out:
    json.dump(decoded_dict, out, indent=4, ensure_ascii=False)

print("\n[+] Decodificação concluída.")
print("[+] Arquivo binário salvo como decoded_output.bin")
print("[+] Arquivo formatado salvo como decoded_formatted.json")