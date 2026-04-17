import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from database import Database
from interface import Interface
from relatorios import Relatorios
from chatbot import ChatbotLean

class LeanFlow:
    def __init__(self, root):
        self.root = root
        self.root.title("LeanFlow - Sistema de Melhoria Contínua")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        
        # ⬇️⬇️⬇️ CÓDIGO DO ÍCONE ADICIONADO AQUI ⬇️⬇️⬇️
        try:
            self.root.iconbitmap("icon.ico")
        except Exception as e:
            print(f"Ícone não encontrado: {e}")
            # Continua com ícone padrão sem erro
        # ⬆️⬆️⬆️ FIM DO CÓDIGO DO ÍCONE ⬆️⬆️⬆️
        
        # Configurar estilos primeiro
        self.configurar_estilos()
        
        # Centralizar janela
        self.centralizar_janela()
        
        # Inicializar banco de dados
        self.db = Database()
        
        # Criar abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Aba de Registro de Melhorias
        self.frame_registro = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_registro, text="📝 Registro de Melhorias")
        
        # Aba de Acompanhamento
        self.frame_acompanhamento = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_acompanhamento, text="📊 Acompanhamento")
        
        # Aba de Relatórios
        self.frame_relatorios = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_relatorios, text="📋 Relatórios e DDS")
        
        # Aba Chatbot Lean
        self.frame_chatbot = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_chatbot, text="🎓 Aprendizado Lean")
        
        # Inicializar módulos
        self.interface = Interface(self.frame_registro, self.frame_acompanhamento, self.db)
        self.relatorios = Relatorios(self.frame_relatorios, self.db)
        self.chatbot = ChatbotLean(self.frame_chatbot)
        
        # Menu
        self.criar_menu()
        
        # Status bar
        self.criar_status_bar()

    def configurar_estilos(self):
        """Configura estilos para botões de perigo"""
        style = ttk.Style()
        style.configure('Danger.TButton', 
                       foreground='white',
                       background='#dc3545',
                       font=('Arial', 9, 'bold'))
        
        style.map('Danger.TButton',
                 background=[('active', '#c82333'),
                           ('pressed', '#bd2130')])

    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = 1400
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def criar_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Limpar Histórico Concluídas", command=self.limpar_historico_concluidas)
        menu_arquivo.add_command(label="Limpar Todo o Histórico", command=self.limpar_historico_completo)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.root.quit)
        
        # Menu Relatórios
        menu_relatorios = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Relatórios", menu=menu_relatorios)
        menu_relatorios.add_command(label="Gerar DDS", command=self.abrir_dds)
        menu_relatorios.add_command(label="Exportar CSV", command=self.exportar_csv)
        menu_relatorios.add_command(label="Relatório Estatístico", command=self.gerar_relatorio_estatistico)
        
        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)
        menu_ajuda.add_command(label="Manual do Usuário", command=self.mostrar_manual)

    def criar_status_bar(self):
        status_bar = ttk.Label(self.root, text="LeanFlow - Sistema de Melhoria Contínua | Pronto para uso", 
                              relief='sunken', anchor='w')
        status_bar.pack(side='bottom', fill='x')

    def limpar_historico_concluidas(self):
        """Limpa apenas as melhorias concluídas"""
        if messagebox.askyesno("Confirmar", 
                              "Deseja realmente limpar o histórico de melhorias CONCLUÍDAS?\n\n"
                              "Esta ação manterá as melhorias pendentes e em andamento."):
            try:
                cursor = self.db.conn.cursor()
                cursor.execute('DELETE FROM melhorias WHERE status = "Concluído"')
                self.db.conn.commit()
                
                messagebox.showinfo("Sucesso", "Histórico de melhorias concluídas limpo com sucesso!")
                self.interface.atualizar_tabela()
                self.relatorios.carregar_melhorias()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar histórico: {str(e)}")

    def limpar_historico_completo(self):
        """Limpa TODO o histórico do banco de dados"""
        if messagebox.askyesno("CONFIRMAR EXCLUSÃO TOTAL", 
                              "⚠️  ATENÇÃO: Esta ação irá apagar TODAS as melhorias do sistema!\n\n"
                              "• Todas as melhorias registradas\n"
                              "• Todo o histórico de acompanhamento\n"
                              "• Todos os dados para relatórios\n\n"
                              "Esta ação NÃO PODE ser desfeita!\n\n"
                              "Confirma que deseja continuar?"):
            try:
                cursor = self.db.conn.cursor()
                cursor.execute('DELETE FROM melhorias')
                self.db.conn.commit()
                
                messagebox.showinfo("Sucesso", "Todo o histórico foi apagado com sucesso!")
                self.interface.atualizar_tabela()
                self.relatorios.carregar_melhorias()
                self.relatorios.limpar_preview()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao apagar histórico: {str(e)}")

    def abrir_dds(self):
        """Abre a aba de relatórios"""
        self.notebook.select(2)  # Seleciona aba de relatórios

    def exportar_csv(self):
        """Exporta dados para CSV"""
        self.relatorios.exportar_csv_excel()

    def gerar_relatorio_estatistico(self):
        """Gera relatório estatístico"""
        self.notebook.select(2)  # Seleciona aba de relatórios
        self.relatorios.gerar_relatorio_estatistico()

    def mostrar_sobre(self):
        messagebox.showinfo("Sobre LeanFlow", 
                           "LeanFlow v2.0\n\n"
                           "Sistema Completo de Melhoria Contínua\n"
                           "Desenvolvido para implementação Lean\n"
                           "em qualquer tipo de empresa.\n\n"
                           "Recursos:\n"
                           "• Registro de melhorias\n"
                           "• Acompanhamento de status\n" 
                           "• Relatórios PDF e CSV\n"
                           "• DDS automatizado\n"
                           "• Chatbot educativo Lean\n\n"
                           "📊 Gestão de Histórico:\n"
                           "• Limpeza seletiva de concluídas\n"
                           "• Limpeza completa do banco\n"
                           "• Controle de dados otimizado")

    def mostrar_manual(self):
        manual_text = """
        MANUAL DO USUÁRIO - LEANFLOW v2.0

        1. 📝 REGISTRO DE MELHORIAS:
           • Preencha todos os campos do formulário
           • Selecione turno (Manhã/Tarde/Noite)
           • Descreva detalhadamente a sugestão

        2. 📊 ACOMPANHAMENTO:
           • Visualize todas as melhorias
           • Filtre por status (Pendente/Andamento/Concluído)
           • Atualize status e responsável
           • 🗑️ Apague histórico de concluídas

        3. 📋 RELATÓRIOS E DDS:
           • Selecione melhorias para DDS
           • Gere PDF para reuniões
           • Exporte dados em CSV
           • Relatórios estatísticos
           • 🗑️ Opções de limpeza de histórico

        4. 🎓 APRENDIZADO LEAN:
           • Chatbot interativo educativo
           • 11 temas completos sobre Lean
           • Imagens organizadas por assunto
           • Navegação por menus numéricos

        🗂️ GESTÃO DE HISTÓRICO:

        • LIMPAR CONCLUÍDAS: Remove apenas melhorias finalizadas
        • LIMPAR COMPLETO: Apaga TODOS os dados (cuidado!)

        💡 DICAS IMPORTANTES:
        • Use 'Limpar Concluídas' periodicamente para otimização
        • Use 'Limpar Completo' apenas quando necessário
        • Gere DDS semanais para reuniões de equipe
        • Explore todos os 11 temas do chatbot
        • Exporte CSV para backup dos dados

        🔄 NAVEGAÇÃO NO CHATBOT:
        • Digite números de 1-11 para temas
        • Digite 0 para voltar ao menu
        • Digite 'sair' para finalizar
        • Sempre pode reiniciar a conversa
        """
        # Criar janela maior para o manual
        manual_window = tk.Toplevel(self.root)
        manual_window.title("Manual do Usuário - LeanFlow")
        manual_window.geometry("600x500")
        manual_window.transient(self.root)
        manual_window.grab_set()
        
        text_area = scrolledtext.ScrolledText(manual_window, wrap=tk.WORD, width=70, height=30)
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text_area.insert(tk.END, manual_text)
        text_area.config(state=tk.DISABLED)
        
        ttk.Button(manual_window, text="Fechar", command=manual_window.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = LeanFlow(root)
    root.mainloop()