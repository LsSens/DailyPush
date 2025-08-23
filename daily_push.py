#!/usr/bin/env python3
"""
DailyPush - Script para fazer commits automáticos diários no GitHub
Mantém as estatísticas do GitHub sempre ativas com commits regulares
"""

import os
import sys
import time
import random
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import git
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daily_push.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DailyPush:
    def __init__(self, repo_path: str = "."):
        """
        Inicializa o DailyPush
        
        Args:
            repo_path: Caminho para o repositório Git
        """
        self.repo_path = Path(repo_path).resolve()
        self.repo = None
        self.initialize_repo()
        
    def initialize_repo(self):
        """Inicializa o repositório Git ou cria um novo se necessário"""
        try:
            # Tenta abrir um repositório existente
            self.repo = git.Repo(self.repo_path)
            logger.info(f"Repositório existente inicializado: {self.repo_path}")
        except git.InvalidGitRepositoryError:
            # Cria um novo repositório Git
            logger.info("Criando novo repositório Git...")
            self.repo = git.Repo.init(self.repo_path)
            
            # Configura usuário Git (pode ser sobrescrito por variáveis de ambiente)
            try:
                self.repo.config_writer().set_value("user", "name", "DailyPush Bot").release()
                self.repo.config_writer().set_value("user", "email", "dailypush@github.com").release()
                logger.info("Configuração Git padrão definida")
            except:
                logger.warning("Não foi possível configurar usuário Git padrão")
            
            logger.info(f"Novo repositório Git criado: {self.repo_path}")
        except Exception as e:
            logger.error(f"Erro ao inicializar repositório: {e}")
            sys.exit(1)
    
    def get_random_activity_message(self) -> str:
        """Retorna uma mensagem aleatória para o commit"""
        activities = [
            "Atualizando documentacao",
            "Melhorias no codigo",
            "Novas funcionalidades",
            "Correcoes de bugs",
            "Atualizacoes diarias",
            "Otimizacoes de performance",
            "Melhorias na interface",
            "Atualizacao de dados",
            "Refatoracao de codigo",
            "Melhorias na arquitetura",
            "Ajustes finos",
            "Manutencao preventiva",
            "Otimizacoes gerais",
            "Preparacao para deploy",
            "Atualizacoes de seguranca"
        ]
        return random.choice(activities)
    
    def create_daily_file(self) -> str:
        """Cria um arquivo com timestamp para o commit diário"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Verifica se é o primeiro commit
        try:
            commit_id = self.repo.head.commit.hexsha[:8]
            branch_name = self.repo.active_branch.name
            total_commits = len(list(self.repo.iter_commits()))
        except:
            # Primeiro commit
            commit_id = "FIRST"
            branch_name = "master"
            total_commits = 0
        
        content = f"""# Daily Update - {timestamp}

Este é um commit automático gerado pelo DailyPush.

## Atividade do dia
- Timestamp: {timestamp}
- Commit ID: {commit_id}
- Branch: {branch_name}

## Estatísticas
- Total de commits: {total_commits}
- Última atualização: {timestamp}

---
*Mantido por DailyPush - Mantendo o GitHub ativo! 🚀*
"""
        
        # Cria diretório para os arquivos diários se não existir
        daily_dir = self.repo_path / "daily_updates"
        daily_dir.mkdir(exist_ok=True)
        
        # Nome do arquivo baseado na data
        filename = daily_dir / f"update_{datetime.now().strftime('%Y%m%d')}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Arquivo criado: {filename}")
        return str(filename)
    
    def make_commit(self, force: bool = False) -> bool:
        """
        Faz o commit diário - SEMPRE cria um commit para manter as estatísticas ativas
        
        Args:
            force: Se True, força o commit mesmo sem mudanças
            
        Returns:
            True se o commit foi bem-sucedido, False caso contrário
        """
        try:
            # Verifica se é o primeiro commit
            is_first_commit = len(list(self.repo.iter_commits())) == 0
            
            # SEMPRE cria um arquivo para commit (mesmo sem mudanças)
            logger.info("Criando arquivo para commit diario...")
            self.create_daily_file()
            
            # Adiciona todos os arquivos exceto logs
            self.repo.index.add('*')
            
            # Remove arquivos de log do staging area
            try:
                # Lista todos os arquivos no staging area
                staged_files = [item.a_path for item in self.repo.index.diff('HEAD')]
                # Remove logs
                for file_path in staged_files:
                    if file_path.endswith('.log'):
                        self.repo.index.remove([file_path])
                        logger.info(f"Arquivo de log removido do commit: {file_path}")
            except Exception as e:
                logger.debug(f"Erro ao remover logs: {e}")
            
            # Cria a mensagem do commit
            if is_first_commit:
                message = "First commit - DailyPush setup"
                logger.info("Criando primeiro commit...")
            else:
                message = self.get_random_activity_message()
            
            # Faz o commit
            commit = self.repo.index.commit(message)
            logger.info(f"Commit realizado: {commit.hexsha[:8]} - {message}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao fazer commit: {e}")
            return False
    
    def should_push_to_github(self) -> tuple[bool, int, int]:
        """
        Verifica se deve fazer push para o GitHub
        
        Returns:
            (deve_fazer_push, total_commits, commits_restantes)
        """
        total_commits = len(list(self.repo.iter_commits()))
        
        # Define um limite aleatório entre 25 e 30 commits
        if not hasattr(self, '_push_threshold'):
            self._push_threshold = random.randint(1, 2)
            logger.info(f"🎯 Limite de commits definido: {self._push_threshold}")
        
        # Faz push quando atingir o limite
        if total_commits >= self._push_threshold:
            return True, total_commits, 0
        
        # Calcula quantos commits ainda precisa
        commits_needed = self._push_threshold - total_commits
        return False, total_commits, commits_needed
    
    def push_to_remote(self, remote_name: str = "origin") -> bool:
        """
        Faz push para o repositório remoto
        
        Args:
            remote_name: Nome do remote (padrão: origin)
            
        Returns:
            True se o push foi bem-sucedido, False caso contrário
        """
        try:
            remote = self.repo.remotes[remote_name]
            remote.push()
            logger.info(f"Push realizado para {remote_name}")
            return True
        except Exception as e:
            logger.error(f"Erro ao fazer push: {e}")
            return False
    
    def daily_routine(self):
        """Rotina diária completa: múltiplos commits + push"""
        logger.info("Iniciando rotina diária...")
        
        # Define quantos commits fazer (entre 25 e 30)
        commits_to_make = random.randint(25, 30)
        logger.info(f"🎯 Fazendo {commits_to_make} commits antes do push...")
        
        # Faz múltiplos commits
        for i in range(commits_to_make):
            logger.info(f"📝 Commit {i+1}/{commits_to_make}...")
            
            if self.make_commit():
                logger.info(f"✅ Commit {i+1} realizado com sucesso!")
            else:
                logger.error(f"❌ Falha no commit {i+1}")
                return False
        
        # Após todos os commits, faz o push
        total_commits = len(list(self.repo.iter_commits()))
        logger.info(f"🎉 Todos os {commits_to_make} commits realizados!")
        logger.info(f"📤 Fazendo push de {total_commits} commits para GitHub...")
        
        try:
            if self.push_to_remote():
                logger.info("🎉 Rotina diária concluída com sucesso!")
                logger.info(f"✅ {total_commits} commits enviados para o GitHub!")
                logger.info("📊 Suas estatísticas do GitHub estão atualizadas!")
            else:
                logger.warning("⚠️ Todos os commits realizados, mas push falhou")
                logger.info("💡 Execute novamente para tentar o push")
        except Exception as e:
            logger.warning(f"⚠️ Todos os commits realizados, mas push falhou: {e}")
            logger.info("💡 Execute novamente para tentar o push")
        
        return True

def main():
    """Função principal"""
    load_dotenv()
    
    # Inicializa o DailyPush (cria repositório Git se necessário)
    daily_push = DailyPush()
    
    # Executa a rotina diária
    success = daily_push.daily_routine()
    
    if success:
        logger.info("DailyPush executado com sucesso!")
        
        # Verifica se é o primeiro commit e dá instruções
        if len(list(daily_push.repo.iter_commits())) == 1:
            logger.info("")
            logger.info("🎉 Primeiro commit realizado com sucesso!")
            logger.info("📋 Próximos passos para sincronizar com GitHub:")
            logger.info("1. Crie um repositório no GitHub")
            logger.info("2. Execute: git remote add origin <URL-DO-REPOSITORIO>")
            logger.info("3. Execute: git push -u origin master")
            logger.info("4. Configure GitHub Actions para automação completa")
        
        sys.exit(0)
    else:
        logger.error("DailyPush falhou!")
        sys.exit(1)

if __name__ == "__main__":
    main()
