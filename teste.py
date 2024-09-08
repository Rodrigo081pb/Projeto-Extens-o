from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFormLayout,
    QMessageBox,
    QInputDialog,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pandas as pd
import sys


class CalculadoraFinanceira(QWidget):
    def __init__(self):
        super().__init__()

        self.transacoes = []
        self.saldo_atual = 0

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Calculadora Financeira")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Título e estilo
        title = QLabel("Calculadora Financeira", self)
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Saldo Atual
        self.label = QLabel(f"Saldo Atual: R${self.saldo_atual:.2f}", self)
        self.label.setFont(QFont("Arial", 16))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Layout de Formulário
        form_layout = QFormLayout()

        # Botões
        btn_gasto = QPushButton("Inserir Gasto", self)
        btn_gasto.setStyleSheet("background-color: #ffcccc;")
        btn_gasto.clicked.connect(self.inserir_gasto)
        form_layout.addRow(btn_gasto)

        btn_receita = QPushButton("Inserir Receita", self)
        btn_receita.setStyleSheet("background-color: #ccffcc;")
        btn_receita.clicked.connect(self.inserir_receita)
        form_layout.addRow(btn_receita)

        btn_saldo = QPushButton("Exibir Saldo", self)
        btn_saldo.setStyleSheet("background-color: #ccccff;")
        btn_saldo.clicked.connect(self.exibir_saldo)
        form_layout.addRow(btn_saldo)

        btn_salvar = QPushButton("Salvar em Excel", self)
        btn_salvar.setStyleSheet("background-color: #ffffcc;")
        btn_salvar.clicked.connect(self.salvar_excel)
        form_layout.addRow(btn_salvar)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def inserir_gasto(self):
        valor, ok1 = QInputDialog.getText(self, "Inserir Gasto", "Valor:")
        descricao, ok2 = QInputDialog.getText(self, "Inserir Gasto", "Descrição:")

        if ok1 and ok2:
            try:
                valor = float(valor)
                self.transacoes.append(
                    {"Tipo": "Gasto", "Descrição": descricao, "Valor": -valor}
                )
                self.saldo_atual -= valor
                self.label.setText(f"Saldo Atual: R${self.saldo_atual:.2f}")
                QMessageBox.information(
                    self, "Sucesso", f"Gasto de R${valor:.2f} registrado."
                )
            except ValueError:
                QMessageBox.warning(
                    self, "Erro", "Valor inválido. Por favor, insira um número."
                )

    def inserir_receita(self):
        valor, ok1 = QInputDialog.getText(self, "Inserir Receita", "Valor:")
        descricao, ok2 = QInputDialog.getText(self, "Inserir Receita", "Descrição:")

        if ok1 and ok2:
            try:
                valor = float(valor)
                self.transacoes.append(
                    {"Tipo": "Receita", "Descrição": descricao, "Valor": valor}
                )
                self.saldo_atual += valor
                self.label.setText(f"Saldo Atual: R${self.saldo_atual:.2f}")
                QMessageBox.information(
                    self, "Sucesso", f"Receita de R${valor:.2f} registrada."
                )
            except ValueError:
                QMessageBox.warning(
                    self, "Erro", "Valor inválido. Por favor, insira um número."
                )

    def exibir_saldo(self):
        QMessageBox.information(
            self, "Saldo Atual", f"Seu saldo atual é: R${self.saldo_atual:.2f}"
        )

    def salvar_excel(self):
        try:
            df = pd.DataFrame(self.transacoes)
            df.to_excel("transacoes.xlsx", index=False)
            QMessageBox.information(
                self, "Sucesso", "Transações salvas no arquivo transacoes.xlsx."
            )
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao salvar arquivo: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CalculadoraFinanceira()
    ex.show()
    sys.exit(app.exec_())
