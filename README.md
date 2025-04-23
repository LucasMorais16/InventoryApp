
# 📦 InventoryApp v0.2

## 👤 Autor / Contato

**Lucas Morais**  
📧 Email: lucas.santoslima.morais@hotmail.com

---

## 📖 Sobre o Aplicativo

Este é um aplicativo de inventário com interface gráfica moderna e intuitiva, desenvolvido em Python utilizando o framework Tkinter.

### Funcionalidades principais:

- ✅ Registro de novos usuários com verificação por e-mail  
- ✅ Login seguro com senha criptografada  
- ✅ Recuperação de senha por e-mail  
- ✅ Organização de usuários por continente, cidade e departamento  
- ✅ Integração com banco de dados PostgreSQL  
- ✅ Interface adaptável com estilo moderno (botões estilizados, placeholders, fontes limpas)

A aplicação é ideal para controle de acesso e cadastro de usuários em sistemas administrativos internos, especialmente em empresas com estrutura global ou multi-regional.

---

## ⚙️ Instruções para Executar

### 🔧 Pré-requisitos

1. **Python 3.10 ou superior**
2. **PostgreSQL** instalado e rodando localmente ou em um servidor
3. **Arquivo `.env`** com credenciais de banco de dados e e-mail

---

### 📦 1. Instale as dependências Python

Use o `pip` para instalar os pacotes necessários:

```bash
pip install -r requirements.txt
```

---

### 🛠️ 2. Configure o Banco de Dados PostgreSQL

Crie o banco de dados com o seguinte comando:

```sql
CREATE DATABASE inventory_db;
```

---

### 🔐 3. Crie um arquivo `.env` na raiz do projeto

```env
# Configurações de e-mail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_de_app

```

> 💡 A senha do e-mail precisa ser uma **senha de aplicativo**, não sua senha pessoal, se estiver usando Gmail.

---

### ▶️ 4. Rode o programa

No terminal, siga esta ordem para o primeiro uso:

```bash
python main.py     # Executa o setup inicial (opcional, caso necessário)
python server.py   # Sobe o servidor local (se houver backend separado)
python main.py     # Inicia o app com interface gráfica
```