# DailyPush 🚀

**DailyPush** é uma ferramenta Python que automatiza commits diários no GitHub, mantendo suas estatísticas sempre ativas e verdes! 

## ✨ Características

- 🤖 **Commits automáticos** todos os dias
- 📝 **Mensagens variadas** e criativas para cada commit
- 📊 **Arquivos de atualização** com timestamp e estatísticas
- ⏰ **Agendamento flexível** para execução automática
- 📋 **Logging completo** de todas as operações
- 🔄 **Push automático** para o repositório remoto

## 🚀 Instalação

### Pré-requisitos

- Python 3.7+
- Git configurado no sistema
- Repositório Git inicializado

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd DailyPush
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o repositório Git

```bash
# Se ainda não tiver um repositório Git
git init
git remote add origin <URL-DO-SEU-REPOSITORIO>

# Configure suas credenciais Git
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"
```

## 📖 Como usar

### Uso básico

Execute o script principal para fazer um commit imediato:

```bash
python daily_push.py
```

### Agendamento automático

Para executar commits automáticos em horários específicos:

```bash
python scheduler.py
```

O scheduler está configurado para executar:
- **09:00** - Commit matinal
- **18:00** - Commit vespertino

## ⚙️ Configuração

### Variáveis de ambiente (opcional)

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações do Git (se necessário)
GIT_USERNAME=seu_usuario
GIT_EMAIL=seu_email@exemplo.com
```

### Personalização das mensagens

Edite o arquivo `daily_push.py` e modifique a lista `activities` na função `get_random_activity_message()` para personalizar as mensagens dos commits.

## 📁 Estrutura do projeto

```
DailyPush/
├── daily_push.py      # Script principal
├── scheduler.py       # Agendador automático
├── requirements.txt   # Dependências Python
├── README.md         # Esta documentação
├── daily_updates/    # Arquivos de atualização diária
└── *.log            # Arquivos de log
```

## 🔧 Funcionamento

1. **Verificação**: O script verifica se há mudanças no repositório
2. **Criação**: Se não houver mudanças, cria um arquivo de atualização
3. **Commit**: Faz o commit com uma mensagem aleatória
4. **Push**: Envia as mudanças para o repositório remoto
5. **Logging**: Registra todas as operações em arquivos de log

## 🌐 Opções de hospedagem

### 1. GitHub Actions (Recomendado)

Crie um arquivo `.github/workflows/daily-push.yml`:

```yaml
name: Daily Push

on:
  schedule:
    - cron: '0 9 * * *'  # Executa às 9:00 AM UTC
  workflow_dispatch:      # Permite execução manual

jobs:
  daily-push:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Configure Git
      run: |
        git config user.name "GitHub Action"
        git config user.email "action@github.com"
    
    - name: Run Daily Push
      run: python daily_push.py
```

### 2. Servidor VPS/Local

Use o scheduler com systemd ou cron:

```bash
# Com systemd (Linux)
sudo systemctl enable daily-push
sudo systemctl start daily-push

# Com cron
crontab -e
# Adicione: 0 9 * * * cd /caminho/para/DailyPush && python daily_push.py
```

### 3. Serviços de nuvem

- **Heroku**: Deploy como app Python
- **Railway**: Deploy automático
- **Render**: Serviço gratuito com cron jobs

## 🐛 Solução de problemas

### Erro: "Não é um repositório Git válido"

```bash
git init
git remote add origin <URL-DO-REPOSITORIO>
```

### Erro: "Falha na autenticação"

Configure suas credenciais Git:

```bash
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"
```

### Erro: "Falha no push"

Verifique se o remote está configurado:

```bash
git remote -v
git remote add origin <URL-DO-REPOSITORIO>
```

## 📝 Logs

O projeto gera logs detalhados:

- `daily_push.log` - Logs do script principal
- `scheduler.log` - Logs do agendador

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

- 🐛 Reportar bugs
- 💡 Sugerir melhorias
- 📝 Melhorar a documentação
- 🚀 Adicionar novas funcionalidades

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## ⚠️ Aviso importante

**DailyPush** é uma ferramenta para manter atividade no GitHub de forma lúdica e educacional. Use com responsabilidade e respeite as políticas do GitHub.

---

**Mantenha seu GitHub sempre ativo com DailyPush! 🚀✨**
