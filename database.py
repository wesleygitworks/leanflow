import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('leanflow.db', check_same_thread=False)
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conn.cursor()
        
        # Tabela de melhorias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS melhorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                turno TEXT NOT NULL,
                operador TEXT NOT NULL,
                departamento TEXT NOT NULL,
                tipo_melhoria TEXT NOT NULL,
                descricao TEXT NOT NULL,
                data_criacao TEXT NOT NULL,
                status TEXT DEFAULT 'Pendente',
                prioridade TEXT DEFAULT 'Média',
                data_conclusao TEXT,
                responsavel TEXT
            )
        ''')
        
        # Tabela de configurações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                chave TEXT PRIMARY KEY,
                valor TEXT
            )
        ''')
        
        self.conn.commit()

    def inserir_melhoria(self, dados):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO melhorias 
            (turno, operador, departamento, tipo_melhoria, descricao, data_criacao, status, prioridade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', dados)
        self.conn.commit()
        return cursor.lastrowid

    def obter_melhorias(self, filtro_status=None):
        cursor = self.conn.cursor()
        if filtro_status:
            cursor.execute('SELECT * FROM melhorias WHERE status = ? ORDER BY data_criacao DESC', (filtro_status,))
        else:
            cursor.execute('SELECT * FROM melhorias ORDER BY data_criacao DESC')
        return cursor.fetchall()

    def atualizar_status(self, id_melhoria, novo_status, responsavel=None):
        cursor = self.conn.cursor()
        if novo_status == 'Concluído':
            cursor.execute('''
                UPDATE melhorias 
                SET status = ?, responsavel = ?, data_conclusao = ?
                WHERE id = ?
            ''', (novo_status, responsavel, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id_melhoria))
        else:
            cursor.execute('''
                UPDATE melhorias 
                SET status = ?, responsavel = ?
                WHERE id = ?
            ''', (novo_status, responsavel, id_melhoria))
        self.conn.commit()

    def limpar_historico(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM melhorias WHERE status = "Concluído"')
        self.conn.commit()

    def obter_estatisticas(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT status, COUNT(*) FROM melhorias GROUP BY status')
        return dict(cursor.fetchall())