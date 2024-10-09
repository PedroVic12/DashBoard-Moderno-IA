class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}: R${self.price:.2f}"


class Menu:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def display_menu(self):
        print("Menu:")
        for item in self.items:
            print(item)


class Order:
    def __init__(self):
        self.items = []
        self.total = 0.0

    def add_item(self, item):
        self.items.append(item)
        self.total += item.price

    def display_order(self):
        print("Seu pedido:")
        for item in self.items:
            print(item)
        print(f"Total: R${self.total:.2f}")


class Chatbot:
    def __init__(self):
        self.menu = Menu()
        self.order = Order()
        self.populate_menu()

    def populate_menu(self):
        self.menu.add_item(MenuItem("Pizza", 29.90))
        self.menu.add_item(MenuItem("Hambúrguer", 19.90))
        self.menu.add_item(MenuItem("Refrigerante", 5.00))

    def start_chat(self):
        print("Bem-vindo ao Delivery Chatbot!")
        self.menu.display_menu()

        while True:
            user_input = input(
                "Digite o nome do item que deseja adicionar ao pedido ou 'sair' para finalizar: "
            )

            if user_input.lower() == "sair":
                break

            item_found = False
            for item in self.menu.items:
                if item.name.lower() == user_input.lower():
                    self.order.add_item(item)
                    print(f"{item.name} adicionado ao pedido.")
                    item_found = True
                    break

            if not item_found:
                print("Item não encontrado no menu. Tente novamente.")

        self.order.display_order()


# Executando o Chatbot
if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.start_chat()
