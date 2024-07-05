import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QInputDialog, QMessageBox
from queue import Queue

class Restaurante:
    def __init__(self):
        #Dicionário que armazena o cardápio com nome e preço de cada item
        self.cardapio = {
            1: {"nome": "Hambúrguer Carne 250g", "preco": 25.00},
            2: {"nome": "Pizza Calabresa", "preco": 35.00},
            3: {"nome": "Salada colorida com repolho roxo", "preco": 15.00},
            4: {"nome": "Refrigerante", "preco": 8.00},
            5: {"nome": "Suco", "preco": 7.00}
        }
        #Fila para armazenar pedidos que estão aguardando processamento
        self.pedidos = Queue()
        #Fila para armazenar pedidos que estão em preparação
        self.preparando = Queue()
        #Lista para armazenar pedidos que foram entregues
        self.entregues = []

    def adicionar_pedido(self, codigo_item, quantidade):
        if codigo_item in self.cardapio:
            item = self.cardapio[codigo_item]
            pedido = {"item": item, "quantidade": quantidade, "status": "Pedido"}
            #Adiciona o pedido à fila de pedidos
            self.pedidos.put(pedido)
            return f"Adicionado {quantidade} x {item['nome']} ao pedido."
        else:
            return "Código do item inválido!"

    def processar_pedido(self):
        if not self.pedidos.empty():
            #Move um pedido da fila de pedidos para a fila de preparação
            pedido = self.pedidos.get()
            pedido["status"] = "Em preparação"
            self.preparando.put(pedido)
            return f"Pedido de {pedido['quantidade']} x {pedido['item']['nome']} está agora em preparação."
        else:
            return "Nenhum pedido para processar."

    def finalizar_preparacao(self):
        if not self.preparando.empty():
            #Move um pedido da fila de preparação para a lista de pedidos entregues
            pedido = self.preparando.get()
            pedido["status"] = "Entregue"
            self.entregues.append(pedido)
            return f"Pedido de {pedido['quantidade']} x {pedido['item']['nome']} foi entregue."
        else:
            return "Nenhum pedido em preparação para finalizar."

    def calcular_faturamento_e_vendas(self):
        faturamento_total = 0
        #Dicionário para armazenar a quantidade de cada item vendido
        vendas_por_item = {codigo: {"nome": item["nome"], "quantidade": 0} for codigo, item in self.cardapio.items()}
        
        #Calcula o faturamento total e a quantidade de cada item vendido
        for pedido in self.entregues:
            item = pedido["item"]
            quantidade = pedido["quantidade"]
            faturamento_total += item["preco"] * quantidade
            codigo_item = [codigo for codigo, info in self.cardapio.items() if info["nome"] == item["nome"]][0]
            vendas_por_item[codigo_item]["quantidade"] += quantidade
        
        return faturamento_total, vendas_por_item

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.restaurante = Restaurante()
        self.initUI()

    
    #Inicializa a interface do usuário. Configura o layout, cria botões, labels, listas,e conecta os botões às funções correspondentes
    def initUI(self):
        self.setWindowTitle('Gerenciamento de Pedidos')

        #Layout principal vertical
        self.layout = QVBoxLayout()

        #Layout horizontal para os botões
        self.button_layout = QHBoxLayout()

        #Botões
        self.btn_mostrar_cardapio = QPushButton('Mostrar Cardápio')
        self.btn_adicionar_pedido = QPushButton('Adicionar Pedido')
        self.btn_processar_pedido = QPushButton('Processar Pedido')
        self.btn_finalizar_preparacao = QPushButton('Finalizar Preparação')
        self.btn_mostrar_pedidos = QPushButton('Mostrar Pedidos')
        self.btn_mostrar_relatorio = QPushButton('Mostrar Relatório')

        
        self.button_layout.addWidget(self.btn_mostrar_cardapio)
        self.button_layout.addWidget(self.btn_adicionar_pedido)
        self.button_layout.addWidget(self.btn_processar_pedido)
        self.button_layout.addWidget(self.btn_finalizar_preparacao)
        self.button_layout.addWidget(self.btn_mostrar_pedidos)
        self.button_layout.addWidget(self.btn_mostrar_relatorio)

        #Adição do layout horizontal ao layout principal vertical
        self.layout.addLayout(self.button_layout)

        #Labels e listas
        self.label_cardapio = QLabel('Cardápio:')
        self.list_cardapio = QListWidget()

        self.label_pedidos = QLabel('Pedidos:')
        self.list_pedidos = QListWidget()

        #Adição dos labels e listas ao layout principal
        self.layout.addWidget(self.label_cardapio)
        self.layout.addWidget(self.list_cardapio)
        self.layout.addWidget(self.label_pedidos)
        self.layout.addWidget(self.list_pedidos)

        self.setLayout(self.layout)

        #Botões
        self.btn_mostrar_cardapio.clicked.connect(self.mostrar_cardapio)
        self.btn_adicionar_pedido.clicked.connect(self.adicionar_pedido)
        self.btn_processar_pedido.clicked.connect(self.processar_pedido)
        self.btn_finalizar_preparacao.clicked.connect(self.finalizar_preparacao)
        self.btn_mostrar_pedidos.clicked.connect(self.mostrar_pedidos)
        self.btn_mostrar_relatorio.clicked.connect(self.mostrar_relatorio)

    def mostrar_cardapio(self):
        self.list_cardapio.clear()
        #Exibe o cardápio na lista
        for codigo, item in self.restaurante.cardapio.items():
            self.list_cardapio.addItem(f"{codigo} - {item['nome']} - R$ {item['preco']:.2f}")

    def adicionar_pedido(self):
        #Coleta os dados do pedido do usuário
        codigo_item, ok1 = QInputDialog.getInt(self, 'Adicionar Pedido', 'Digite o código do item:')
        quantidade, ok2 = QInputDialog.getInt(self, 'Adicionar Pedido', 'Digite a quantidade:')
        if ok1 and ok2:
            resultado = self.restaurante.adicionar_pedido(codigo_item, quantidade)
            QMessageBox.information(self, 'Adicionar Pedido', resultado)

    def processar_pedido(self):
        resultado = self.restaurante.processar_pedido()
        QMessageBox.information(self, 'Processar Pedido', resultado)

    def finalizar_preparacao(self):
        resultado = self.restaurante.finalizar_preparacao()
        QMessageBox.information(self, 'Finalizar Preparação', resultado)

    def mostrar_pedidos(self):
        self.list_pedidos.clear()

        #Exibe os pedidos em fila
        self.list_pedidos.addItem("Pedidos em fila:")
        if self.restaurante.pedidos.empty():
            self.list_pedidos.addItem("Nenhum pedido em fila.")
        else:
            for pedido in list(self.restaurante.pedidos.queue):
                self.list_pedidos.addItem(f"{pedido['quantidade']} x {pedido['item']['nome']} - Status: {pedido['status']}")

        #Exibe os pedidos em preparação
        self.list_pedidos.addItem("\nPedidos em preparação:")
        if self.restaurante.preparando.empty():
            self.list_pedidos.addItem("Nenhum pedido em preparação.")
        else:
            for pedido in list(self.restaurante.preparando.queue):
                self.list_pedidos.addItem(f"{pedido['quantidade']} x {pedido['item']['nome']} - Status: {pedido['status']}")

        #Exibe os pedidos entregues
        self.list_pedidos.addItem("\nPedidos entregues:")
        if not self.restaurante.entregues:
            self.list_pedidos.addItem("Nenhum pedido entregue.")
        else:
            for pedido in self.restaurante.entregues:
                self.list_pedidos.addItem(f"{pedido['quantidade']} x {pedido['item']['nome']} - Status: {pedido['status']}")

    def mostrar_relatorio(self):
        faturamento_total, vendas_por_item = self.restaurante.calcular_faturamento_e_vendas()
        #Gera o relatório de vendas
        relatorio = f"Faturamento total: R$ {faturamento_total:.2f}\n\n"
        relatorio += "Quantidade de itens vendidos:\n"
        for item in vendas_por_item.values():
            relatorio += f"{item['nome']}: {item['quantidade']}\n"
        QMessageBox.information(self, 'Relatório de Vendas', relatorio)

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
