import os
from pathlib import Path
import pandas as pd

if os.path.exists("Vendas.xlsx"):
    os.remove("Vendas.xlsx")

vendas = pd.DataFrame(columns=['Loja', 'Vendedor', 'Valor da Venda'])

def enterOnDir(pasta):
    os.chdir(pasta)
    return Path.cwd().iterdir()

os.chdir(input('Digite o caminho da pasta de vendas: '))
caminho = Path.cwd()
for pasta in caminho.iterdir():  # Pasta ano
    if not pasta.is_dir():
        break
    anoVenda = pasta.name
    for pasta in enterOnDir(pasta):  # Pasta mes
        if not pasta.is_dir():
            break
        mesVenda = pasta.name.split(".")[0]
        for pasta in enterOnDir(pasta):  # Pasta dia
            if not pasta.is_dir():
                break
            diaVenda = pasta.name
            for arquivo in enterOnDir(pasta):
                venda = pd.read_excel(arquivo,index_col=0)
                print(venda)
                venda['Data'] = f'{diaVenda}/{mesVenda}/{anoVenda}'
                vendas = pd.concat(
                    [vendas, venda], ignore_index=True)

os.chdir(r'C:\Users\Rafael\Documents\Python\Automação\PlanilhaDeVendas')

vendas.to_excel('Vendas.xlsx')