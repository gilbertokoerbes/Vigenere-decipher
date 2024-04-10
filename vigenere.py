import time

class Vigenere:
    def __init__(self, cipher_text) -> None:
        self.cipher_text = cipher_text
    #     self.language_shift = language_shift
    # def set_language_shift(self, language):
    #      self.language_shift =  language 


    def count_letter_in_substring(self, substring):
        letter_counts = {}
        for letter in substring:
            if letter in letter_counts:
                letter_counts[letter] += 1
            else:
                letter_counts[letter] = 1
        return letter_counts
            

    def calculate_friedman_coincidence_index(self,  max_key_length):
        self.tuple_letter_ic_values = [] # [(key_length, ic)]

        for key_length in range(1, max_key_length + 1):
            coincidences = 0
            total_pairs = 0

            for i in range(key_length):
                substring = self.cipher_text[i::key_length]
                n_substring_size = len(substring)

                letter_counts = self.count_letter_in_substring(substring)

                # Calculate the index of coincidence for this substring
                for letter, count in letter_counts.items():
                    coincidences += count * (count - 1)
                total_pairs += n_substring_size * (n_substring_size - 1)

            ic = coincidences / total_pairs
            self.tuple_letter_ic_values.append((key_length, ic))

        return self.tuple_letter_ic_values
    
    def find_best_key_length(self, ic_values):
        # Find the key length with the highest coincidence index

        sorted_ic = sorted(ic_values, key=lambda x: x[1])
        print("...IC para cada tamanho de chave...")
        for ic in sorted_ic:
            print("Key Length: {}, Index of Coincidence: {}".format(ic[0], ic[1]))

        print("......")
        
        return sorted_ic
    
    def frequency_index_letter(self, string):
        n_substring_size = len(string)
        letter_counts = self.count_letter_in_substring(string)
        
        # Calcular o índice de frequência de cada letra
        indice_frequencia_letras = {}
        for letra, freq in letter_counts.items():
            indice_frequencia_letras[letra] = freq / n_substring_size
        # Encontre a letra com o maior índice de frequência
        reversed_indice_frequencia_letras = sorted(indice_frequencia_letras.items(), key=lambda x: x[1], reverse=True)
        return reversed_indice_frequencia_letras


    def decrypted_text(self,text, shift):
        C = ord(text) - ord('a')
        K = ord(shift) - ord('a')
        P = (C - K + 26) % 26

        P_plain_text = chr(P + ord('a'))

        return P_plain_text
    


if __name__ == "__main__":

    TEST_MAX_KEY_LENGTH = 21

    file_open = open("./ciphertext.txt", "r")
    ciphertext = file_open.read()

    vigenere = Vigenere(ciphertext)
    print("calculate_friedman_coincidence_index()")
    ic_values = vigenere.calculate_friedman_coincidence_index(TEST_MAX_KEY_LENGTH)
    sorted_ic = vigenere.find_best_key_length(ic_values)

    use_key_length = int(input("Digite o tamanho de chave a ser utilizado\n> "))

    print("......")
    
    linha_index = ""
    linha_1 = ""
    linha_2 = ""
    KEY = ""
    for i in range(use_key_length):

        frequency_index_letter = vigenere.frequency_index_letter(ciphertext[i::use_key_length])

        linha_index += "{} ".format(i)
        linha_1 += "{} ".format(frequency_index_letter[0][0])
        linha_2 += "{} ".format(frequency_index_letter[1][0])

        KEY += frequency_index_letter[0][0]


    print("'key_idx/primeira/segunda' letra mais frequente em linhas")
    print(linha_index)
    print(linha_1)
    print(linha_2)
    print("......")
    print("chave sugerida ", KEY)
    input_key = input("prosseguir com a chave segurida (y/ digitar_chave)\n> ")

    if input_key != "y" and len(input_key)!=0:
        KEY = input_key
    print(f'decifrando com "{KEY}"')
    
    print("......")


    decipher_plain_text = ""
    for i in range(len(ciphertext)):
        key_index = i % len(KEY)
        key_letter = KEY[key_index]
        cipher_letter = ciphertext[i]
        decipher_plain_text += vigenere.decrypted_text(cipher_letter, key_letter)
        
    print("......")
    print("gerado arquivo output_deciphertext.txt")
    fouput = open("output_deciphertext.txt", "w") 
    fouput.write("".join(decipher_plain_text))