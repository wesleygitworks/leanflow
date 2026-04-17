import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

class Interface:
    def __init__(self, frame_registro, frame_acompanhamento, db):
        self.db = db
        self.criar_interface_registro(frame_registro)
        self.criar_interface_acompanhamento(frame_acompanhamento)

    def criar_interface_registro(self, frame):
        # Frame principal
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Título
        titulo = ttk.Label(main_frame, text="Registro de Melhorias", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Formulário
        labels = ['Turno:', 'Operador:', 'Departamento:', 'Tipo de Melhoria:', 'Descrição:']
        self.widgets = {}

        for i, label in enumerate(labels):
            ttk.Label(main_frame, text=label).grid(row=i+1, column=0, sticky='w', pady=5)
            
            if label == 'Turno:':
                # Apenas Manhã, Tarde, Noite
                self.widgets['turno'] = ttk.Combobox(main_frame, 
                    values=['Manhã', 'Tarde', 'Noite'])
                self.widgets['turno'].grid(row=i+1, column=1, sticky='ew', pady=5, padx=(10,0))
            
            elif label == 'Tipo de Melhoria:':
                self.widgets['tipo_melhoria'] = ttk.Combobox(main_frame,
                    values=['Segurança', 'Qualidade', 'Produtividade', 'Custo', 'Organização', 'Outros'])
                self.widgets['tipo_melhoria'].grid(row=i+1, column=1, sticky='ew', pady=5, padx=(10,0))
            
            elif label == 'Descrição:':
                self.widgets['descricao'] = tk.Text(main_frame, height=5, width=40)
                self.widgets['descricao'].grid(row=i+1, column=1, sticky='ew', pady=5, padx=(10,0))
            
            else:
                self.widgets[label.lower().replace(':', '')] = ttk.Entry(main_frame, width=30)
                self.widgets[label.lower().replace(':', '')].grid(row=i+1, column=1, sticky='ew', pady=5, padx=(10,0))

        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Registrar Melhoria", 
                  command=self.registrar_melhoria).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpar Campos", 
                  command=self.limpar_campos).pack(side='left', padx=5)

        # REMOVIDO: Todo o código da logo foi excluído
        # A área abaixo dos botões ficará em branco/limpa

        # Configurar grid
        main_frame.columnconfigure(1, weight=1)

    def criar_interface_acompanhamento(self, frame):
        # Frame principal
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Controles de filtro
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(filter_frame, text="Filtrar por Status:").pack(side='left', padx=5)
        self.filtro_status = ttk.Combobox(filter_frame, 
            values=['Todos', 'Pendente', 'Em Andamento', 'Concluído'])
        self.filtro_status.set('Todos')
        self.filtro_status.pack(side='left', padx=5)
        ttk.Button(filter_frame, text="Aplicar Filtro", 
                  command=self.atualizar_tabela).pack(side='left', padx=5)

        # Botão para apagar histórico
        ttk.Button(filter_frame, text="🗑️ Apagar Histórico", 
                  command=self.apagar_historico,
                  style='Danger.TButton').pack(side='right', padx=5)

        # Tabela
        columns = ('ID', 'Turno', 'Operador', 'Departamento', 'Tipo', 'Descrição', 'Status', 'Data')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill='both', expand=True)

        # Controles de status
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill='x', pady=10)

        ttk.Label(status_frame, text="Alterar Status:").pack(side='left', padx=5)
        self.novo_status = ttk.Combobox(status_frame, 
            values=['Pendente', 'Em Andamento', 'Concluído'])
        self.novo_status.pack(side='left', padx=5)
        
        ttk.Label(status_frame, text="Responsável:").pack(side='left', padx=5)
        self.responsavel = ttk.Entry(status_frame, width=20)
        self.responsavel.pack(side='left', padx=5)
        
        ttk.Button(status_frame, text="Atualizar Status", 
                  command=self.atualizar_status_selecionado).pack(side='left', padx=5)

        self.atualizar_tabela()

    def apagar_historico(self):
        """Apaga o histórico de melhorias concluídas"""
        if messagebox.askyesno("Confirmar", 
                              "Deseja realmente apagar todo o histórico de melhorias CONCLUÍDAS?\n\n"
                              "Esta ação não pode ser desfeita."):
            try:
                # Apaga apenas as concluídas para manter melhorias ativas
                cursor = self.db.conn.cursor()
                cursor.execute('DELETE FROM melhorias WHERE status = "Concluído"')
                self.db.conn.commit()
                
                messagebox.showinfo("Sucesso", "Histórico de melhorias concluídas apagado com sucesso!")
                self.atualizar_tabela()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao apagar histórico: {str(e)}")

    def registrar_melhoria(self):
        try:
            dados = (
                self.widgets['turno'].get(),
                self.widgets['operador'].get(),
                self.widgets['departamento'].get(),
                self.widgets['tipo_melhoria'].get(),
                self.widgets['descricao'].get("1.0", tk.END).strip(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Pendente',
                'Média'
            )

            # Validar campos obrigatórios
            if not all([dados[0], dados[1], dados[2], dados[3], dados[4]]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return

            self.db.inserir_melhoria(dados)
            messagebox.showinfo("Sucesso", "Melhoria registrada com sucesso!")
            self.limpar_campos()
            self.atualizar_tabela()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar melhoria: {str(e)}")

    def limpar_campos(self):
        for widget in self.widgets.values():
            if isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
            else:
                widget.set('') if hasattr(widget, 'set') else widget.delete(0, tk.END)

    def atualizar_tabela(self):
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obter dados filtrados
        filtro = self.filtro_status.get()
        status_filtro = None if filtro == 'Todos' else filtro
        melhorias = self.db.obter_melhorias(status_filtro)

        # Popular tabela
        for melhoria in melhorias:
            self.tree.insert('', 'end', values=(
                melhoria[0], melhoria[1], melhoria[2], melhoria[3],
                melhoria[4], melhoria[5][:50] + '...' if len(melhoria[5]) > 50 else melhoria[5],
                melhoria[7], melhoria[6]
            ))

    def atualizar_status_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma melhoria da tabela!")
            return

        id_melhoria = self.tree.item(selecionado[0])['values'][0]
        novo_status = self.novo_status.get()
        responsavel = self.responsavel.get()

        if not novo_status:
            messagebox.showwarning("Aviso", "Selecione um status!")
            return

        self.db.atualizar_status(id_melhoria, novo_status, responsavel)
        messagebox.showinfo("Sucesso", "Status atualizado com sucesso!")
        self.atualizar_tabela()