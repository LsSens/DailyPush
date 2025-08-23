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
        """Inicializa o repositório Git"""
        try:
            self.repo = git.Repo(self.repo_path)
            logger.info(f"Repositório inicializado: {self.repo_path}")
        except git.InvalidGitRepositoryError:
            logger.error(f"Diretório não é um repositório Git válido: {self.repo_path}")
            sys.exit(1)
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
            # SEMPRE cria um arquivo para commit (mesmo sem mudanças)
            logger.info("Criando arquivo para commit diario...")
            self.create_daily_file()
            
            # Adiciona todas as mudanças
            self.repo.index.add('*')
            
            # Cria a mensagem do commit
            message = self.get_random_activity_message()
            
            # Faz o commit
            commit = self.repo.index.commit(message)
            logger.info(f"Commit realizado: {commit.hexsha[:8]} - {message}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao fazer commit: {e}")
            return False
    
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
        """Rotina diária completa: commit + push"""
        logger.info("Iniciando rotina diária...")
        
        # SEMPRE faz o commit (para manter estatísticas ativas)
        if self.make_commit():
            # Tenta fazer o push (opcional)
            try:
                if self.push_to_remote():
                    logger.info("Rotina diária concluída com sucesso! 🎉")
                else:
                    logger.warning("Commit realizado, mas push falhou (pode ser configurado depois)")
            except:
                logger.warning("Commit realizado, mas push falhou (pode ser configurado depois)")
            return True
        else:
            logger.error("Falha ao fazer commit")
            return False

def main():
    """Função principal"""
    load_dotenv()
    
    # Verifica se estamos em um repositório Git
    try:
        git.Repo(".")
    except git.InvalidGitRepositoryError:
        logger.error("Este diretório não é um repositório Git!")
        logger.info("Por favor, inicialize um repositório Git primeiro:")
        logger.info("git init")
        logger.info("git remote add origin <seu-repositorio>")
        sys.exit(1)
    
    # Inicializa o DailyPush
    daily_push = DailyPush()
    
    # Executa a rotina diária
    success = daily_push.daily_routine()
    
    if success:
        logger.info("DailyPush executado com sucesso!")
        sys.exit(0)
    else:
        logger.error("DailyPush falhou!")
        sys.exit(1)

if __name__ == "__main__":
    main()
