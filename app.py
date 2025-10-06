from functions import run

user_input = input("Digite os IDs separados por vírgula: \n")
ids = [int(i.strip()) for i in user_input.split(",")]

run(ids)
