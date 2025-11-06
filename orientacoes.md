# 📘 Orientações do Projeto

Este documento contém orientações práticas para configurar o ambiente de desenvolvimento e publicar o projeto no GitHub.

---

## 🐍 1. Configuração do Ambiente Virtual (venv)

O ambiente virtual Python permite isolar as dependências do projeto, evitando conflitos com outros projetos.

### 1.1. Criar o Ambiente Virtual

No terminal, navegue até a pasta do projeto e execute:

```bash
# Navegar até a pasta do projeto
cd projeto_01_gestao_financeira_pessoal

# Criar ambiente virtual
python3 -m venv venv

# No Windows (se o comando acima não funcionar):
# py -m venv venv
```

### 1.2. Ativar o Ambiente Virtual

**No macOS/Linux:**
```bash
source venv/bin/activate
```

**No Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**No Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

Após ativar, você verá `(venv)` no início da linha do terminal.

### 1.3. Instalar Dependências (se houver)

Se você criar um arquivo `requirements.txt` com as dependências:

```bash
pip install -r requirements.txt
```

Para este projeto (Módulo 1), não há dependências externas necessárias, apenas Python padrão.

### 1.4. Desativar o Ambiente Virtual

Quando terminar de trabalhar:

```bash
deactivate
```

---

## 📦 2. Criar Arquivo requirements.txt (Opcional)

Se você adicionar dependências futuras, crie um arquivo `requirements.txt`:

```bash
# Gerar requirements.txt a partir das bibliotecas instaladas
pip freeze > requirements.txt
```

**Exemplo de `requirements.txt` vazio para este projeto:**
```txt
# Este projeto utiliza apenas bibliotecas padrão do Python
# Não há dependências externas necessárias
```

---

## 🚀 3. Publicar no GitHub

### 3.1. Preparar o Projeto

Antes de publicar, certifique-se de ter:

1. **Arquivo `.gitignore`** (criar na raiz do projeto):
```bash
# Criar arquivo .gitignore
cat > .gitignore << EOF
# Ambiente Virtual
venv/
env/
ENV/

# Arquivos Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Arquivos de dados grandes (opcional)
*.csv
*.xlsx
*.json

# Arquivos do sistema
.DS_Store
Thumbs.db

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
EOF
```

2. **README.md** (já existe com a documentação do projeto)

### 3.2. Inicializar Repositório Git

```bash
# Certifique-se de estar na pasta do projeto
cd projeto_01_gestao_financeira_pessoal

# Inicializar repositório Git
git init

# Adicionar todos os arquivos
git add .

# Fazer primeiro commit
git commit -m "Initial commit: Sistema de Gestão Financeira Pessoal"
```

### 3.3. Criar Repositório no GitHub

1. **Acesse GitHub.com** e faça login
2. **Clique em "New repository"** (ou acesse: https://github.com/new)
3. **Configure o repositório:**
   - **Repository name**: `projeto_01_gestao_financeira_pessoal`
   - **Description**: "Sistema de Gestão Financeira Pessoal - Projeto do Módulo 1"
   - **Visibilidade**: Público ou Privado (sua escolha)
   - **NÃO marque** "Initialize with README" (já temos um)
4. **Clique em "Create repository"**

### 3.4. Conectar e Publicar

```bash
# Adicionar remote (substitua SEU_USUARIO pelo seu username do GitHub)
git remote add origin https://github.com/SEU_USUARIO/projeto_01_gestao_financeira_pessoal.git

# Verificar remote
git remote -v

# Renomear branch para main (se necessário)
git branch -M main

# Enviar código para GitHub
git push -u origin main
```

**Se solicitado credenciais:**
- Use seu **token de acesso pessoal** (não sua senha)
- Para criar um token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

### 3.5. Atualizar o Projeto (Futuras Alterações)

Sempre que fizer alterações:

```bash
# Verificar status
git status

# Adicionar arquivos modificados
git add .

# Fazer commit
git commit -m "Descrição das alterações realizadas"

# Enviar para GitHub
git push
```

---

## 📝 4. Estrutura Recomendada do Projeto

```
projeto_01_gestao_financeira_pessoal/
├── README.md                 # Documentação principal
├── orientacoes.md           # Este arquivo
├── .gitignore               # Arquivos ignorados pelo Git
├── requirements.txt         # Dependências (opcional)
├── sistema_financeiro.py      # Código principal
├── venv/                    # Ambiente virtual (não versionar)
├── dados/                   # Arquivos de dados
└── relatorios/              # Relatórios gerados
```

---

## 💡 5. Dicas Importantes

### 5.1. Boas Práticas com Git

- Faça commits frequentes e descritivos
- Use mensagens de commit claras:
  - ✅ `git commit -m "Adiciona função calcular_saldo()"`
  - ❌ `git commit -m "mudanças"`

### 5.2. Trabalhando com Branches

```bash
# Criar uma branch para nova funcionalidade
git checkout -b feature/nova-funcionalidade

# Trabalhar na branch...
# Fazer commits...

# Voltar para main
git checkout main

# Fazer merge da branch
git merge feature/nova-funcionalidade
```

### 5.3. Verificar Status

```bash
# Ver status do repositório
git status

# Ver histórico de commits
git log --oneline

# Ver diferenças
git diff
```

---

## 🔧 6. Solução de Problemas Comuns

### Problema: "fatal: not a git repository"
**Solução:** Execute `git init` na pasta do projeto

### Problema: "remote origin already exists"
**Solução:** 
```bash
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/projeto_01_gestao_financeira_pessoal.git
```

### Problema: "permission denied" ao fazer push
**Solução:** 
- Verifique se você está autenticado no GitHub
- Use token de acesso pessoal ao invés de senha
- Configure SSH keys (opcional, mais avançado)

---

## 📚 7. Recursos Adicionais

- **Documentação Git**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com
- **Python venv**: https://docs.python.org/3/library/venv.html

---

## ✅ Checklist de Publicação

- [ ] Ambiente virtual criado e ativado
- [ ] Arquivo `.gitignore` criado
- [ ] README.md completo
- [ ] Código funcionando e testado
- [ ] Repositório Git inicializado
- [ ] Primeiro commit realizado
- [ ] Repositório criado no GitHub
- [ ] Remote adicionado
- [ ] Código enviado para GitHub (`git push`)
- [ ] Repositório público e acessível

---

**Boa sorte com seu projeto! 🚀**

Se tiver dúvidas, consulte a documentação ou peça ajuda ao instrutor.
