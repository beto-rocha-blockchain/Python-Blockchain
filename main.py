import hashlib
import datetime as date
import random

# Definição de usuário com autenticação e permissões
class User:
    def __init__(self, user_id, name, permission_level, email, phone, password):
        self.user_id = user_id
        self.name = name
        self.permission_level = permission_level  # Ex.: 'admin', 'user'
        self.email = email
        self.phone = phone
        self.password = password
        self.is_verified = False

    def verify_email(self):
        print(f"E-mail de confirmação enviado para {self.email}.")
        return True

    def verify_sms(self):
        print(f"Mensagem de texto enviada para {self.phone}.")
        return True

# Definição de um bloco
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

# Definição da Blockchain
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.users = {}

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), 'Genesis Block', '0')

    def register_user(self, user_id, name, permission_level, email, phone, password):
        self.users[user_id] = User(user_id, name, permission_level, email, phone, password)

    def authenticate_user(self, user_id, password):
        user = self.users.get(user_id)
        if user and user.password == password:
            email_verified = user.verify_email()
            sms_verified = user.verify_sms()
            if email_verified and sms_verified:
                user.is_verified = True
                print("Autenticação completa.")
                return True
        print("Falha na autenticação.")
        return False

    def has_permission(self, user_id):
        user = self.users.get(user_id)
        return user and user.permission_level in ['admin', 'user'] and user.is_verified

    def convert_to_usd(self, value):
        return value / 10000  # 10000 unidades = 1 dólar

    def add_block(self, user_id, new_block):
        if not self.has_permission(user_id):
            raise PermissionError("Usuário não tem permissão ou não está autenticado para adicionar blocos.")
        new_block.previous_hash = self.chain[-1].hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def print_blockchain(self):
        for block in self.chain:
            print(f'Bloco: {block.index}')
            print(f'Timestamp: {block.timestamp}')
            print(f'Dados salvos: {block.data}')
            print(f'Hash: {block.hash}')
            print(f'Hash do bloco anterior: {block.previous_hash}')
            print(20 * '-----')

# Criando a blockchain e registrando usuários
my_Blockchain = Blockchain()
my_Blockchain.register_user('1', 'Admin User', 'admin', 'admin@example.com', '+123456789', 'adminpass')
my_Blockchain.register_user('2', 'Regular User', 'user', 'user@example.com', '+987654321', 'userpass')

# Autenticação do usuário antes de transações
if my_Blockchain.authenticate_user('1', 'adminpass'):
    # Dados de teste com conversão para dólar
    compra1 = {
        'item': 'Ford Mustang',
        'valor_em_unidades': 100000,  # Valor original
        'valor_em_dolares': my_Blockchain.convert_to_usd(100000),
        'comprador': '@beu_io',
        'vendedor': '@vendedor'
    }

    # Adicionando blocos com permissões
    my_Blockchain.add_block('1', Block(1, date.datetime.now(), compra1, my_Blockchain.chain[-1].hash))

# Verificação de validade e impressão dos blocos
print(f'Essa blockchain está válida? {str(my_Blockchain.is_valid())}')
my_Blockchain.print_blockchain()