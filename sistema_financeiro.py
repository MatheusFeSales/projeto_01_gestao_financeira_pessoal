from datetime import datetime
import os

transacoes = []
arquivo_dados = 'transacoes.txt'

# ============================================
# FUNÇÕES DE TRANSAÇÕES
# ============================================
def adicionar_transacao(tipo, descricao, valor, data, categoria=None):
    tipo = str(tipo).lower().strip()
    if tipo not in ('receita', 'despesa'):
        print('Você não colocou um tipo válido (use "receita" ou "despesa").')
        return

    try:
        valor = float(valor)
    except ValueError:
        print("Valor inválido. Digite um número.")
        return

    if valor <= 0:
        print('Digite um valor positivo.')
        return

    if not isinstance(descricao, str) or not descricao.strip():
        print("Descrição não pode ser vazia.")
        return
    descricao = descricao.strip()

    try:
        datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        print('Digite uma data válida - YYYY-MM-DD.')
        return

    if tipo == 'despesa' and not categoria:
        categoria = 'Sem categoria'
    if tipo == 'receita':
        categoria = None

    transacao = {
        'tipo': tipo,
        'descricao': descricao,
        'valor': valor,
        'data': data,
        'categoria': categoria,
    }
    transacoes.append(transacao)
    return transacao


def listar_transacoes(filtro_tipo=None, filtro_categoria=None):
    lista = transacoes

    if filtro_tipo is not None:
        filtro_tipo = str(filtro_tipo).lower().strip()
        if filtro_tipo not in ('receita', 'despesa'):
            return []
        lista = [t for t in lista if t['tipo'] == filtro_tipo]

    if filtro_categoria is not None:
        alvo = str(filtro_categoria).strip().casefold()
        lista = [
            t for t in lista
            if (t.get('categoria') or "").casefold() == alvo
        ]
    return lista


# ============================================
# FUNÇÕES DE CÁLCULOS
# ============================================
"""
As funções abaixo calculam:
- saldo total (receitas - despesas)
- total por tipo
- gastos por categoria
"""

def calcular_saldo():
    total_receitas = 0.0
    total_despesas = 0.0

    for t in transacoes:
        if t['tipo'] == 'receita':
            total_receitas += t['valor']
        elif t['tipo'] == 'despesa':
            total_despesas += t['valor']

    saldo = total_receitas - total_despesas
    return saldo


def calcular_total_por_tipo(tipo):
    tipo = str(tipo).lower().strip()
    if tipo not in ('receita', 'despesa'):
        print('Tipo inválido, use receita ou despesa')
        return 0.0

    total = 0.0
    for t in transacoes:
        if t['tipo'] == tipo:
            total += t['valor']
    return total


def calcular_gastos_por_categoria():
    gastos_por_categoria = {}
    for t in transacoes:
        if t['tipo'] == 'despesa':
            categoria = t.get('categoria') or 'Sem categoria'
            if categoria in gastos_por_categoria:
                gastos_por_categoria[categoria] += t['valor']
            else:
                gastos_por_categoria[categoria] = t['valor']
    return gastos_por_categoria


# ============================================
# RELATÓRIOS
# ============================================
def gerar_relatorio():
    total_receita = calcular_total_por_tipo('receita')
    total_despesa = calcular_total_por_tipo('despesa')
    saldo = calcular_saldo()
    gastos_cat = calcular_gastos_por_categoria()

    relatorio = {
        'quantidade_transacoes': len(transacoes),
        'total_receitas': total_receita,
        'total_despesas': total_despesa,
        'saldo': saldo,
        'gastos_por_categoria': gastos_cat
    }
    return relatorio


def exibir_extrato():
    if not transacoes:
        print('Não há transações para exibir')
        return

    print(f"{'Data':10} | {'Tipo':8} | {'Valor':>10} | {'Categoria':15} | Descrição")
    print("-" * 65)
    for t in transacoes:
        data = t['data']
        tipo = t['tipo']
        valor = t['valor']
        categoria = t['categoria'] if t['categoria'] else '-'
        descricao = t['descricao']
        print(f"{data:10} | {tipo:8} | R$ {valor:8.2f} | {categoria[:15]:15} | {descricao}")


# ============================================
# PERSISTÊNCIA
# ============================================
def salvar_arquivo():
    with open(arquivo_dados, 'w', encoding='utf-8') as f:
        for t in transacoes:
            tipo = t['tipo']
            descricao = str(t['descricao']).replace('|', '/')
            valor = float(t['valor'])
            data = t['data']
            categoria = t['categoria'] if tipo == 'despesa' else '-'
            categoria = (categoria or '-').replace('|', '/')
            linha = f"{tipo}|{descricao}|{valor}|{data}|{categoria}\n"
            f.write(linha)


def carregar_arquivo():
    if not os.path.exists(arquivo_dados):
        return

    transacoes.clear()
    with open(arquivo_dados, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split('|')
            if len(partes) != 5:
                continue

            tipo, descricao, valor_str, data_str, categoria = partes

            if tipo == 'receita':
                categoria = None
            elif categoria == '-' or not categoria.strip():
                categoria = 'Sem categoria'   # (era '==' por engano)

            try:
                valor = float(valor_str)
                datetime.strptime(data_str, '%Y-%m-%d')
            except Exception:
                continue

            adicionar_transacao(tipo, descricao, valor, data_str, categoria)


# ============================================
# MENU / MAIN
# ============================================
def main():
    carregar_arquivo()

    while True:
        print("\n===== SISTEMA DE GESTÃO FINANCEIRA =====")
        print("1 - Adicionar RECEITA")
        print("2 - Adicionar DESPESA")
        print("3 - Listar transações")
        print("4 - Exibir extrato")
        print("5 - Gerar relatório")
        print("6 - Salvar em arquivo")
        print("0 - Sair")
        print("========================================")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == '0':
            print('Saindo do sistema, até logo')
            break

        elif opcao == '1':
            descricao = input('Descrição de receita: ').strip()
            try:
                valor = float(input('Valor: ').replace(',', '.'))
            except ValueError:
                print("Valor inválido.")
                continue
            data = input('Data (YYYY-MM-DD): ').strip()
            adicionar_transacao("receita", descricao, valor, data)
            print("Receita adicionada com sucesso!")

        elif opcao == '2':
            descricao = input('Descrição de despesa: ').strip()
            try:
                valor = float(input('Valor: ').replace(',', '.'))
            except ValueError:
                print("Valor inválido.")
                continue
            data = input('Data (YYYY-MM-DD): ').strip()
            categoria = input('Categoria: ').strip()
            adicionar_transacao('despesa', descricao, valor, data, categoria)
            print('Despesa adicionada com sucesso')

        elif opcao == '3':
            tipo = input('Filtrar por tipo (receita/despesa) ou Enter para todos: ').strip().lower() or None
            categoria = input('Filtrar por categoria ou Enter para todas: ').strip() or None
            lista = listar_transacoes(tipo, categoria)
            if not lista:
                print('Nenhuma transação encontrada.')
            else:
                print(f"\n--- {len(lista)} transações encontradas ---")
                print(f"{'Data':10} | {'Tipo':8} | {'Valor':>10} | {'Categoria':15} | Descrição")
                print("-" * 65)
                for t in lista:
                    print(f"{t['data']:10} | {t['tipo']:8} | R$ {t['valor']:8.2f} | {(t['categoria'] or '-')[:15]:15} | {t['descricao']}")

        elif opcao == '4':
            exibir_extrato()

        elif opcao == '5':
            relatorio = gerar_relatorio()
            print("\n===== RELATÓRIO FINANCEIRO =====")
            print(f"Total de transações: {relatorio['quantidade_transacoes']}")
            print(f"Total de receitas:   R$ {relatorio['total_receitas']:.2f}")
            print(f"Total de despesas:   R$ {relatorio['total_despesas']:.2f}")
            print(f"Saldo atual:         R$ {relatorio['saldo']:.2f}")
            print("Gastos por categoria:")
            for cat, val in relatorio['gastos_por_categoria'].items():
                print(f" - {cat}: R$ {val:.2f}")

        elif opcao == '6':
            salvar_arquivo()
            print(f"Transações salvas no arquivo '{arquivo_dados}' com sucesso")

        else:
            print("Opção inválida, tente novamente")


if __name__ == "__main__":
    main()