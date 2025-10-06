from functions import run

while True:
    user_input = input("Digite os IDs separados por vírgula (ou 0 para sair): \n").strip()
    
    if user_input == "0":        
        break

    id_strings = [i.strip() for i in user_input.split(",")]
    if all(i.isdigit() for i in id_strings):
        ids = [int(i) for i in id_strings]
        run(ids)
        print("\n")
    else:
        print("Entrada inválida! Digite apenas números separados por vírgula.\n")
