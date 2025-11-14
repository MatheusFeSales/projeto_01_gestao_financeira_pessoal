from datetime import datetime, date
import os

# --------------------------------------------
# Estrutura de Dados Principal
# --------------------------------------------
# Manteremos todas as transações adicionadas pelo usuário nesse dicionário.
# Cada transação tem: tipo ('receita' | 'despesa'), descricao (str),
# valor (float, positivo), data (YYYY-MM-DD) e categoria (str ou None).

transacoes = []

# Nome do arquivo usado para persistência simples (formato texto)
arquivo_dados = 'transacoes.txt'

# ============================================
# FUNÇÕES DE TRANSAÇÕES
# ============================================

def adicionar_transacao(tipo, descricao, valor, data, categoria=None):
    """
    Cria e adiciona uma transação válida à lista global transações.
    Regras: 
    - Tipo: Receita ou despesa;
    - Descrição não pode ser vazia;
    - Valor deve ser número e maior que zero;
    - Data deve seguir o padrão YYYY-MM-DD;
    - Despesas devem ser obrigatório a categoria, se vier sem vira 'Sem categoria';
    - Para receitas, categoria = None.
    Retorna o dicionário da transação adicionada, ou None em caso de erro (com prints).
    """

    # Normaliza e valida o tipo
    tipo = str(tipo).lower().strip()
    if tipo not in ('receita', 'despesa'):
        print('Você não colocou um tipo válido (use "receita" ou "despesa").')
        return None
    
    # Tenta converter o valor para float
    try:
        valor = float(valor)
    except ValueError:
        print("Valor inválido. Digite um número.")
        return None

    if valor <= 0:
        print('Digite um valor positivo.')
        return None

    # Valida a descrição
    if not isinstance(descricao, str) or not descricao.strip():
        print("Descrição não pode ser vazia.")
        return None
    descricao = descricao.strip()

    # Valida data e lança um ValueError se formato for inválido
    try:
        data_obj = datetime.strptime(data, '%Y-%m-%d').date()
        if data_obj < date(2000, 1, 1) or data_obj > date.today():
            # Não aceita data antiga ou futura.
            print('Data deve estar entre 2000-01-01 e hoje.')
            return None
    except ValueError:
        print('Digite uma data válida - YYYY-MM-DD.')
        return None

    # Regras de categoria por tipo
    if tipo == 'despesa' and not categoria:
        categoria = 'Sem categoria'
    if tipo == 'receita':
        categoria = None

    # Dicionário com a transação já adicionada
    transacao = {
        'tipo': tipo,
        'descricao': descricao,
        'valor': valor,
        'data': data,
        'categoria': categoria,
    }
    
    # Adicionando na lista global 'transação'
    transacoes.append(transacao)
    return transacao


def listar_transacoes(filtro_tipo=None, filtro_categoria=None):
    """
    Função que lista as transações inseridas pelo usuário por tipo (Receita ou despesa)
    e categoria. 
    """

    lista = transacoes.copy()

    # Filtra por tipo quando este é informado.
    if filtro_tipo is not None:
        filtro_tipo = str(filtro_tipo).lower().strip()
        if filtro_tipo not in ('receita', 'despesa'):
            return []
        lista = [t for t in lista if t['tipo'] == filtro_tipo]

    # Filtra por categoria, quando esta é informada.
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
    """
    Retorna o saldo atual = soma(receitas) - soma(despesas)
    """

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
    """
    Soma e retorna o total de `tipo` informado ('receita' ou 'despesa').
    Se o tipo for inválido, imprime aviso e retorna 0.0.
    """

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
    """
    Soma o total dos gastos por categoria, retornando um dicionário 
    """

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
    """
    Gera um resumo geral das finanças:
    - quantidade de transações
    - total de receitas e despesas
    - saldo final
    - gastos por categoria
    """

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
    """
    Exibe todas as transações registradas, formatadas em tabela.
    """

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
# Essas funções salvam e carregam as transações em um arquivo de texto local.


def salvar_arquivo():
    """
    Salva todas as transações no arquivo `transacoes.txt`.
    Cada linha segue o formato: tipo|descricao|valor|data|categoria
    """
    try:
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
        return True
    except IOError as e:
        print(f'ERRO ao salvar arquivo: {e}')
        print('Verifique se você tem permissão para escrever neste local.')
        return False


def carregar_arquivo():
    """
    Carrega as transações do arquivo, se existir.
    Valida os dados e adiciona à lista global `transacoes`.
    """
    if not os.path.exists(arquivo_dados):
        return

    try:
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
                
                # Restaura a barra original (salva com /, carrega com /)
                descricao = descricao.replace('/', '|')
                categoria = categoria.replace('/', '|')

                if tipo == 'receita':
                    categoria = None
                elif categoria == '-' or not categoria.strip():
                    categoria = 'Sem categoria'

                try:
                    valor = float(valor_str)
                    datetime.strptime(data_str, '%Y-%m-%d')
                except Exception:
                    continue

                adicionar_transacao(tipo, descricao, valor, data_str, categoria)
    
    except IOError as e:
        print(f'ERRO ao carregar arquivo: {e}')
        return


# ============================================
# MENU / MAIN
# ============================================
# Essa é a parte interativa do sistema, que roda no terminal.
# O usuário escolhe opções no menu para adicionar, listar e salvar transações.

def main():
    carregar_arquivo()

    dados_salvos = True

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
            if not dados_salvos:
                resposta = input('Há mudanças não salvas. Salvar antes de sair? (s/n): ')
                if resposta.lower() == 's':
                    if salvar_arquivo():
                        print('Dados salvos com sucesso!')
            print('Saindo do sistema, até logo')
            break

        elif opcao == '1':
            # Adicionar receita
            descricao = input('Descrição de receita: ').strip()
            try:
                valor = float(input('Valor: ').replace(',', '.'))
            except ValueError:
                print("Valor inválido.")
                continue
            data = input('Data (YYYY-MM-DD): ').strip()
            if adicionar_transacao("receita", descricao, valor, data):
                print("Receita adicionada com sucesso!")
                dados_salvos = False
                if salvar_arquivo():
                    dados_salvos = True

        elif opcao == '2':
            # Adicionar despesa
            descricao = input('Descrição de despesa: ').strip()
            try:
                valor = float(input('Valor: ').replace(',', '.'))
            except ValueError:
                print("Valor inválido.")
                continue
            data = input('Data (YYYY-MM-DD): ').strip()
            categoria = input('Categoria: ').strip()

            if adicionar_transacao('despesa', descricao, valor, data, categoria):
                print('Despesa adicionada com sucesso!')
                dados_salvos = False
                if salvar_arquivo():
                    dados_salvos = True

        elif opcao == '3':
            # Lista transações com filtros
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
            # Exibe extrato completo
            exibir_extrato()

        elif opcao == '5':
            # Gera o relatório resumido
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
            # Salvar em arquivo manualmente
            if salvar_arquivo():
                print(f"Transações salvas no arquivo '{arquivo_dados}' com sucesso!")
                dados_salvos = True

        else:
            print("Opção inválida, tente novamente")


# O ponto de entrada do programa: só roda o menu se for executado diretamente.
if __name__ == "__main__":
    main()