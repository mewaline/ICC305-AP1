import itertools
import numpy as np

def gerar_tabela_sinais(num_fatores):
    combinacoes = list(itertools.product(*[[-1, 1] for _ in range(num_fatores)][::-1]))
    tabela = []
    for linha in combinacoes:
        linha = linha[::-1]
        efeitos_linha = [1]
        efeitos_linha.extend(linha)
        for ordem in range(2, num_fatores + 1):
            for combinacao in itertools.combinations(range(num_fatores), ordem):
                produto = 1
                for indice in combinacao:
                    produto *= linha[indice]
                efeitos_linha.append(produto)
        tabela.append(efeitos_linha)
    return np.array(tabela)

def gerar_nomes_efeitos(num_fatores):
    from itertools import combinations
    nomes_fatores = [chr(65 + i) for i in range(num_fatores)]
    nomes_efeitos = nomes_fatores.copy()
    for ordem in range(2, num_fatores + 1):
        for combinacao in combinations(nomes_fatores, ordem):
            nomes_efeitos.append(''.join(combinacao))
    return nomes_efeitos

def obter_respostas(num_execucoes, num_replicacoes):
    todas_respostas = []
    for i in range(num_execucoes):
        respostas_execucao = []
        for j in range(num_replicacoes):
            valor = float(input(f"Digite y para execução {i + 1}, repetição {j + 1}: "))
            respostas_execucao.append(valor)
        todas_respostas.append(respostas_execucao)
    return todas_respostas

def calcular_medias_respostas(respostas):
    return [np.mean(replicacoes) for replicacoes in respostas]

def calcular_efeitos(tabela_sinais, medias_respostas):
    X = np.array(tabela_sinais)
    y = np.array(medias_respostas)
    n = len(y)
    efeitos = (X.T @ y) / n
    return efeitos

def calcular_variacao(efeitos, num_replicacoes, num_fatores, respostas, nomes_efeitos):
    soma_total_quadrados = 0
    media_geral = np.mean([y for execucao in respostas for y in execucao])
    for execucao in respostas:
        for valor in execucao:
            soma_total_quadrados += (valor - media_geral) ** 2

    soma_quadrados_efeitos = [(2 ** num_fatores * num_replicacoes) * efeitos[i] ** 2 for i in range(1, len(efeitos))]
    soma_quadrados_erro = soma_total_quadrados - sum(soma_quadrados_efeitos)
    porcentagens_explicadas = [ss / soma_total_quadrados * 100 for ss in soma_quadrados_efeitos]

    return (
        dict(zip(nomes_efeitos, soma_quadrados_efeitos)),
        soma_quadrados_erro,
        soma_total_quadrados,
        dict(zip(nomes_efeitos, porcentagens_explicadas))
    )

def calcular_respostas_estimadas(tabela_sinais, efeitos):
    return tabela_sinais @ efeitos

def imprimir_tabela_completa(tabela_sinais, nomes_efeitos, respostas, y_estimado):
    print("\nTabela Final Completa:")
    num_reps = len(respostas[0])
    colunas = ['I'] + nomes_efeitos + ['ŷi']
    colunas += [f"y{j+1}" for j in range(num_reps)]
    colunas += [f"e{j+1}" for j in range(num_reps)]

    col_width = max(len(c) for c in colunas + ['-99.99']) + 2
    print("".join(c.ljust(col_width) for c in colunas))

    for i, linha in enumerate(tabela_sinais):
        sinais_formatados = [f"{int(val)}" if val in [-1, 1] else f"{val:.2f}" for val in linha[1:]]
        y_hat = y_estimado[i]
        y_vals = respostas[i]
        e_vals = [y - y_hat for y in y_vals]

        linha_completa = (
            ['1'] + sinais_formatados + [f"{y_hat:.2f}"] +
            [f"{y:.2f}" for y in y_vals] +
            [f"{e:.2f}" for e in e_vals]
        )

        print("".join(val.ljust(col_width) for val in linha_completa))
    
def main():
    num_fatores = int(input("Digite o número de fatores (2 a 5): "))
    num_replicacoes = int(input("Digite o número de replicações (1 a 3): "))
    assert 2 <= num_fatores <= 5 and 1 <= num_replicacoes <= 3

    nomes_efeitos = gerar_nomes_efeitos(num_fatores)
    tabela_sinais = gerar_tabela_sinais(num_fatores)

    respostas = obter_respostas(len(tabela_sinais), num_replicacoes)
    medias = calcular_medias_respostas(respostas)
    efeitos = calcular_efeitos(tabela_sinais, medias)
    y_estimado = calcular_respostas_estimadas(tabela_sinais, efeitos)

    imprimir_tabela_completa(tabela_sinais, nomes_efeitos, respostas, y_estimado)


    print("\nEfeitos calculados:")
    print(f"Efeito 0: {efeitos[0]:.2f}")
    for i, nome in enumerate(nomes_efeitos):
        print(f"{nome}: {efeitos[i + 1]:.2f}")

    ss_efeitos, ss_erro, ss_total, explicacoes = calcular_variacao(
        efeitos, num_replicacoes, num_fatores, respostas, nomes_efeitos
    )



    print("\nPorcentagem da variação explicada por cada efeito:")
    for nome in nomes_efeitos:
        print(f"SS{nome} = {ss_efeitos[nome]:.2f} ({explicacoes[nome]:.2f}%)")
    
    print(f"\nSSE = {ss_erro:.2f}")

    print(f"SST = {ss_total:.2f}")

   

if __name__ == "__main__":
    main()