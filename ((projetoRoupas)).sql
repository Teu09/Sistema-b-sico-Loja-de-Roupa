CREATE DATABASE prjetoRoupas;

USE projetoRoupas;

CREATE TABLE Clientes (
    cliente_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    endereco VARCHAR(255),
    cidade VARCHAR(100),
    estado VARCHAR(100),
    cep VARCHAR(20),
    data_criacao DATE NOT NULL
);

CREATE TABLE Fornecedores (
    fornecedor_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    contato VARCHAR(100),
    email VARCHAR(100),
    endereco VARCHAR(255),
    cidade VARCHAR(100),
    estado VARCHAR(100),
    cep VARCHAR(20)
);

CREATE TABLE Telefones (
    telefone_id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20) NOT NULL,
    tipo VARCHAR(20),
    cliente_id INT,
    fornecedor_id INT,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id) ON DELETE CASCADE,
    FOREIGN KEY (fornecedor_id) REFERENCES Fornecedores(fornecedor_id) ON DELETE CASCADE
);

CREATE TABLE Logins (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    data_criacao DATE NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id) ON DELETE CASCADE
);

CREATE TABLE Formas_Pagamento (
    forma_pagamento_id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL
);

CREATE TABLE Categorias (
    categoria_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

CREATE TABLE Produtos (
    produto_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    quantidade_estoque INT NOT NULL,
    categoria_id INT,
    fornecedor_id INT,
    FOREIGN KEY (categoria_id) REFERENCES Categorias(categoria_id),
    FOREIGN KEY (fornecedor_id) REFERENCES Fornecedores(fornecedor_id)
);

CREATE TABLE Pedidos (
    pedido_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    data_pedido DATE NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    forma_pagamento_id INT,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id),
    FOREIGN KEY (forma_pagamento_id) REFERENCES Formas_Pagamento(forma_pagamento_id)
);

CREATE TABLE Itens_Pedido (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    produto_id INT,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    preco_total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(pedido_id),
    FOREIGN KEY (produto_id) REFERENCES Produtos(produto_id)
);
use projetoRoupas
INSERT INTO Clientes (nome, email, endereco, cidade, estado, cep, data_criacao)
VALUES ('João da Silva', 'joao@example.com', 'Rua A, 123', 'São Paulo', 'SP', '01000-000', CURDATE());

INSERT INTO Fornecedores (nome, contato, email, endereco, cidade, estado, cep)
VALUES ('Fornecedor XYZ', 'Maria', 'maria@fornecedorxyz.com', 'Avenida B, 456', 'Rio de Janeiro', 'RJ', '20000-000');

INSERT INTO Telefones (numero, tipo, cliente_id)
VALUES ('11987654321', 'Celular', 1);

INSERT INTO Telefones (numero, tipo, fornecedor_id)
VALUES ('21987654321', 'Comercial', 1);

INSERT INTO Logins (cliente_id, usuario, senha, data_criacao)
VALUES (1, 'joaosilva', 'senha123', CURDATE());

INSERT INTO Formas_Pagamento (descricao)
VALUES ('Cartão de Crédito');

INSERT INTO Categorias (nome, descricao)
VALUES ('Roupas', 'Vestuário em geral');

INSERT INTO Produtos (nome, descricao, preco, quantidade_estoque, categoria_id, fornecedor_id)
VALUES ('Camiseta', 'Camiseta de algodão', 29.90, 100, 1, 1);

INSERT INTO Pedidos (cliente_id, data_pedido, valor_total, forma_pagamento_id)
VALUES (1, CURDATE(), 59.80, 1);

INSERT INTO Itens_Pedido (pedido_id, produto_id, quantidade, preco_unitario, preco_total)
VALUES (1, 1, 2, 29.90, 59.80);
select * from logins

CREATE TABLE Marcas (
    marca_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Tamanhos (
    tamanho_id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL UNIQUE
);

ALTER TABLE Produtos
ADD marca_id INT,
ADD tamanho_id INT,
ADD FOREIGN KEY (marca_id) REFERENCES Marcas(marca_id),
ADD FOREIGN KEY (tamanho_id) REFERENCES Tamanhos(tamanho_id);