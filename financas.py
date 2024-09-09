import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os


# Classe da Calculadora Financeira
class CalculadoraFinanceira:
    def __init__(self):
        self.transacoes = pd.DataFrame(
            columns=["Data", "Tipo", "Descrição", "Valor", "Saldo", "Categoria"]
        )
        self.saldo_atual = 0

    def inserir_gasto(self, valor, descricao, categoria="Outros"):
        data_atual = datetime.now().strftime("%Y-%m-%d")
        self.saldo_atual -= valor
        nova_transacao = pd.DataFrame(
            {
                "Data": [data_atual],
                "Tipo": ["Gasto"],
                "Descrição": [descricao],
                "Valor": [-valor],
                "Saldo": [self.saldo_atual],
                "Categoria": [categoria],
            }
        )
        self.transacoes = pd.concat(
            [self.transacoes, nova_transacao], ignore_index=True
        )
        print(f"Gasto de R${valor:.2f} inserido com sucesso.")

    def inserir_receita(self, valor, descricao):
        data_atual = datetime.now().strftime("%Y-%m-%d")
        self.saldo_atual += valor
        nova_transacao = pd.DataFrame(
            {
                "Data": [data_atual],
                "Tipo": ["Receita"],
                "Descrição": [descricao],
                "Valor": [valor],
                "Saldo": [self.saldo_atual],
                "Categoria": ["Receita"],
            }
        )
        self.transacoes = pd.concat(
            [self.transacoes, nova_transacao], ignore_index=True
        )
        print(f"Receita de R${valor:.2f} inserida com sucesso.")

    def exibir_saldo(self):
        print(f"Seu saldo atual é: R${self.saldo_atual:.2f}")

    def salvar_excel(self, nome_arquivo="transacoes_financeiras.xlsx"):
        self.transacoes.to_excel(nome_arquivo, index=False)
        print(f"Transações salvas em {nome_arquivo}")

    def listar_transacoes(self):
        if self.transacoes.empty:
            print("Nenhuma transação registrada.")
        else:
            print(self.transacoes)

    def filtrar_por_data(self, data_inicio, data_fim):
        data_inicio = pd.to_datetime(data_inicio)
        data_fim = pd.to_datetime(data_fim)
        filtradas = self.transacoes[
            (pd.to_datetime(self.transacoes["Data"]) >= data_inicio)
            & (pd.to_datetime(self.transacoes["Data"]) <= data_fim)
        ]
        if filtradas.empty:
            print("Nenhuma transação no período especificado.")
        else:
            print(filtradas)

    def saldo_por_periodo(self, data_inicio, data_fim):
        data_inicio = pd.to_datetime(data_inicio)
        data_fim = pd.to_datetime(data_fim)
        filtradas = self.transacoes[
            (pd.to_datetime(self.transacoes["Data"]) >= data_inicio)
            & (pd.to_datetime(self.transacoes["Data"]) <= data_fim)
        ]
        if filtradas.empty:
            print("Nenhuma transação no período especificado.")
        else:
            saldo_periodo = filtradas["Valor"].sum()
            print(
                f"Saldo no período de {data_inicio.date()} a {data_fim.date()}: R${saldo_periodo:.2f}"
            )

    def gerar_grafico_despesas(self):
        despesas = self.transacoes[self.transacoes["Tipo"] == "Gasto"]
        if despesas.empty:
            print("Nenhuma despesa registrada.")
        else:
            plt.plot(despesas["Data"], despesas["Valor"], marker="o", color="r")
            plt.title("Gráfico de Despesas")
            plt.xlabel("Data")
            plt.ylabel("Valor (R$)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    def previsao_saldo_futuro(self, dias):
        media_despesas_diaria = self.transacoes[self.transacoes["Tipo"] == "Gasto"][
            "Valor"
        ].mean()
        saldo_futuro = self.saldo_atual + (media_despesas_diaria * dias)
        print(f"Previsão de saldo para os próximos {dias} dias: R${saldo_futuro:.2f}")

    def alerta_gastos(self, limite):
        total_gastos = self.transacoes[self.transacoes["Tipo"] == "Gasto"][
            "Valor"
        ].sum()
        if total_gastos > limite:
            print(f"Atenção! Seus gastos já ultrapassaram o limite de R${limite:.2f}.")
        else:
            print(f"Seus gastos estão dentro do limite de R${limite:.2f}.")

    def inserir_gasto_com_categoria(self, valor, descricao, categoria):
        self.inserir_gasto(valor, descricao, categoria)

    def resumo_mensal(self, mes, ano):
        transacoes_mes = self.transacoes[
            (pd.to_datetime(self.transacoes["Data"]).dt.month == mes)
            & (pd.to_datetime(self.transacoes["Data"]).dt.year == ano)
        ]
        total_receitas = transacoes_mes[transacoes_mes["Tipo"] == "Receita"][
            "Valor"
        ].sum()
        total_gastos = transacoes_mes[transacoes_mes["Tipo"] == "Gasto"]["Valor"].sum()
        saldo_mes = total_receitas + total_gastos
        print(
            f"Resumo do mês {mes}/{ano}:\nTotal de Receitas: R${total_receitas:.2f}\nTotal de Gastos: R${-total_gastos:.2f}\nSaldo Final: R${saldo_mes:.2f}"
        )

    def definir_objetivo(self, valor_meta):
        if self.saldo_atual >= valor_meta:
            print(f"Você já atingiu sua meta financeira de R${valor_meta:.2f}.")
        else:
            restante = valor_meta - self.saldo_atual
            print(f"Faltam R${restante:.2f} para atingir sua meta financeira.")

    def sugestao_poupanca(self):
        categoria_maior_gasto = self.transacoes[self.transacoes["Tipo"] == "Gasto"][
            "Categoria"
        ].mode()[0]
        print(
            f"Você está gastando mais em {categoria_maior_gasto}. Considere reduzir seus gastos nesta categoria."
        )

    def tendencias_consumo(self):
        dias_com_mais_gastos = self.transacoes[self.transacoes["Tipo"] == "Gasto"][
            "Data"
        ].mode()[0]
        print(
            f"Você tende a gastar mais nos dias {dias_com_mais_gastos}. Planeje-se para esses dias e evite gastos excessivos."
        )

    def comparativo_mensal(self, ano):
        transacoes_ano = self.transacoes[
            pd.to_datetime(self.transacoes["Data"]).dt.year == ano
        ]
        if transacoes_ano.empty:
            print(f"Nenhuma transação registrada para o ano {ano}.")
        else:
            transacoes_ano["Mes"] = pd.to_datetime(transacoes_ano["Data"]).dt.month
            comparativo = transacoes_ano.groupby("Mes")["Valor"].sum()
            comparativo.plot(kind="bar", color="b")
            plt.title(f"Comparativo Mensal de Gastos e Receitas - {ano}")
            plt.xlabel("Mês")
            plt.ylabel("Valor (R$)")
            plt.show()

    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear")


def main():
    calculadora = CalculadoraFinanceira()

    while True:
        calculadora.limpar_tela()

        print("=" * 100)
        print(f"{'Seja bem-vindo(a) à Calculadora Financeira!':^100}")
        print("=" * 100)
        print(f"{'MENU PRINCIPAL':^100}")
        print("=" * 100)
        print(f"{'1. Inserir Gasto':<50} {'2. Inserir Receita':<50}")
        print(f"{'3. Exibir Saldo Atual':<50} {'4. Listar Transações':<50}")
        print(
            f"{'5. Filtrar Transações por Data':<50} {'6. Exibir Saldo por Período':<50}"
        )
        print(
            f"{'7. Salvar Transações em Excel':<50} {'8. Gerar Gráfico de Despesas':<50}"
        )
        print(
            f"{'9. Previsão de Saldo Futuro':<50} {'10. Alerta de Gastos Excessivos':<50}"
        )
        print(
            f"{'11. Inserir Gasto com Categoria':<50} {'12. Resumo Financeiro Mensal':<50}"
        )
        print(
            f"{'13. Definir Objetivo Financeiro':<50} {'14. Sugestões de Poupança':<50}"
        )
        print(
            f"{'15. Análise de Tendências de Consumo':<50} {'16. Comparativo Mensal':<50}"
        )
        print(f"{'17. Sair':<50}")
        print("=" * 100)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            valor = float(input("Valor do gasto: R$"))
            descricao = input("Descrição do gasto: ")
            categoria = input("Categoria do gasto: ")
            calculadora.inserir_gasto_com_categoria(valor, descricao, categoria)
        elif opcao == "2":
            valor = float(input("Valor da receita: R$"))
            descricao = input("Descrição da receita: ")
            calculadora.inserir_receita(valor, descricao)
        elif opcao == "3":
            calculadora.exibir_saldo()
        elif opcao == "4":
            calculadora.listar_transacoes()
        elif opcao == "5":
            data_inicio = input("Data de início (YYYY-MM-DD): ")
            data_fim = input("Data de fim (YYYY-MM-DD): ")
            calculadora.filtrar_por_data(data_inicio, data_fim)
        elif opcao == "6":
            data_inicio = input("Data de início (YYYY-MM-DD): ")
            data_fim = input("Data de fim (YYYY-MM-DD): ")
            calculadora.saldo_por_periodo(data_inicio, data_fim)
        elif opcao == "7":
            nome_arquivo = input("Nome do arquivo (com extensão .xlsx): ")
            calculadora.salvar_excel(nome_arquivo)
        elif opcao == "8":
            calculadora.gerar_grafico_despesas()
        elif opcao == "9":
            dias = int(input("Número de dias para previsão: "))
            calculadora.previsao_saldo_futuro(dias)
        elif opcao == "10":
            limite = float(input("Defina o limite de gastos: R$"))
            calculadora.alerta_gastos(limite)
        elif opcao == "11":
            valor = float(input("Valor do gasto: R$"))
            descricao = input("Descrição do gasto: ")
            categoria = input("Categoria do gasto: ")
            calculadora.inserir_gasto_com_categoria(valor, descricao, categoria)
        elif opcao == "12":
            mes = int(input("Mês (1-12): "))
            ano = int(input("Ano (YYYY): "))
            calculadora.resumo_mensal(mes, ano)
        elif opcao == "13":
            valor_meta = float(input("Defina o valor do objetivo financeiro: R$"))
            calculadora.definir_objetivo(valor_meta)
        elif opcao == "14":
            calculadora.sugestao_poupanca()
        elif opcao == "15":
            calculadora.tendencias_consumo()
        elif opcao == "16":
            ano = int(input("Digite o ano para o comparativo: "))
            calculadora.comparativo_mensal(ano)
        elif opcao == "17":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
