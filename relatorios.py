import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os

class Relatorios:
    def __init__(self, frame, db):
        self.db = db
        self.criar_interface(frame)

    def criar_interface(self, frame):
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Título
        titulo = ttk.Label(main_frame, text="Relatórios e DDS", 
                          font=('Arial', 16, 'bold'))
        titulo.pack(pady=(0, 20))

        # Frame de controles
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill='x', pady=10)

        # NOVO: Botão para apagar histórico
        ttk.Button(controls_frame, text="🗑️ Apagar Histórico Completo", 
                  command=self.apagar_historico_completo,
                  style='Danger.TButton').pack(side='right', padx=5)

        # Seleção de melhorias para DDS
        ttk.Label(controls_frame, text="Selecionar Melhorias para DDS:").pack(anchor='w')
        
        self.lista_melhorias = tk.Listbox(controls_frame, selectmode='multiple', height=6)
        self.lista_melhorias.pack(fill='x', pady=5)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=10)

        ttk.Button(btn_frame, text="Carregar Melhorias", 
                  command=self.carregar_melhorias).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Gerar DDS PDF", 
                  command=self.gerar_dds_pdf).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Exportar CSV Excel",
                  command=self.exportar_csv_excel).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Relatório Estatístico", 
                  command=self.gerar_relatorio_estatistico).pack(side='left', padx=5)

        # NOVO: Botão para limpar preview
        ttk.Button(btn_frame, text="Limpar Preview", 
                  command=self.limpar_preview).pack(side='left', padx=5)

        # Área de preview
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill='both', expand=True, pady=(10, 0))

        ttk.Label(preview_frame, text="Preview do Relatório:").pack(anchor='w', pady=(0,5))
        
        # Frame para preview com botão de limpar
        preview_header = ttk.Frame(preview_frame)
        preview_header.pack(fill='x')
        ttk.Button(preview_header, text="🗑️ Limpar Histórico Preview", 
                  command=self.limpar_historico_preview).pack(side='right')

        self.texto_preview = tk.Text(preview_frame, height=15, width=80)
        self.texto_preview.pack(fill='both', expand=True)

        self.carregar_melhorias()

    def exportar_csv_excel(self):
        """Exporta dados para CSV compatível com Excel"""
        try:
            filename = f"melhorias_leanflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Usar encoding UTF-8 com BOM para Excel
            with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file, delimiter=';')  # Usar ; como delimitador
                
                # Cabeçalho com nomes em português
                writer.writerow([
                    'ID', 'Turno', 'Operador', 'Departamento', 'Tipo_Melhoria', 
                    'Descricao', 'Status', 'Data_Criacao', 'Data_Conclusao', 'Responsavel'
                ])
                
                melhorias = self.db.obter_melhorias()
                
                for melhoria in melhorias:
                    # Formatar dados para evitar problemas no Excel
                    linha_formatada = []
                    for campo in melhoria:
                        if campo is None:
                            linha_formatada.append('')
                        elif isinstance(campo, str):
                            # Remover quebras de linha e caracteres problemáticos
                            campo_limpo = campo.replace('\n', ' ').replace('\r', ' ').replace(';', ',')
                            linha_formatada.append(campo_limpo)
                        else:
                            linha_formatada.append(str(campo))
                    
                    writer.writerow(linha_formatada)
            
            mensagem_sucesso = f"""✅ CSV exportado com sucesso: {filename}

📝 **Instruções para abrir no Excel:**
1. Abra o Excel
2. Vá em "Dados" > "Obter Dados" > "De Arquivo" > "De Texto/CSV"
3. Selecione o arquivo {filename}
4. Na importação, selecione:
   - Origem: Unicode (UTF-8)
   - Delimitador: Ponto e vírgula (;)
5. Clique em "Carregar"

💡 **Dica:** Ou simplesmente abra o arquivo normalmente e ignore o aviso - os dados estarão corretos!"""
            
            messagebox.showinfo("Sucesso - CSV Compatível com Excel", mensagem_sucesso)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar CSV: {str(e)}")

    def apagar_historico_completo(self):
        """Apaga todo o histórico do banco de dados"""
        if messagebox.askyesno("CONFIRMAR EXCLUSÃO", 
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
                self.carregar_melhorias()
                self.limpar_preview()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao apagar histórico: {str(e)}")

    def limpar_historico_preview(self):
        """Limpa o histórico exibido no preview"""
        if messagebox.askyesno("Confirmar", "Deseja limpar o preview do relatório?"):
            self.texto_preview.delete(1.0, tk.END)

    def limpar_preview(self):
        """Limpa o preview"""
        self.texto_preview.delete(1.0, tk.END)

    def carregar_melhorias(self):
        self.lista_melhorias.delete(0, tk.END)
        melhorias = self.db.obter_melhorias()
        
        if not melhorias:
            self.lista_melhorias.insert(tk.END, "Nenhuma melhoria registrada no momento")
            return
            
        for melhoria in melhorias:
            texto = f"ID {melhoria[0]}: {melhoria[4]} - {melhoria[5][:50]}..."
            self.lista_melhorias.insert(tk.END, texto)

    def gerar_dds_pdf(self):
        selecionados = self.lista_melhorias.curselection()
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione pelo menos uma melhoria!")
            return

        melhorias_selecionadas = []
        melhorias_completas = self.db.obter_melhorias()
        
        for index in selecionados:
            try:
                texto_item = self.lista_melhorias.get(index)
                id_melhoria = int(texto_item.split(':')[0].replace('ID ', ''))
                for melhoria in melhorias_completas:
                    if melhoria[0] == id_melhoria:
                        melhorias_selecionadas.append(melhoria)
                        break
            except:
                continue

        try:
            filename = f"DDS_Melhoria_Continua_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Título
            titulo_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("DDS - Diálogo Diário de Segurança", titulo_style))
            story.append(Paragraph("Foco: Melhoria Contínua", styles['Heading2']))
            story.append(Spacer(1, 20))

            # Data e informações gerais
            story.append(Paragraph(f"<b>Data do DDS:</b> {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
            story.append(Paragraph(f"<b>Total de Melhorias Selecionadas:</b> {len(melhorias_selecionadas)}", styles['Normal']))
            story.append(Spacer(1, 20))

            # Conteúdo do DDS - AGORA COM TODAS AS INFORMAÇÕES
            for i, melhoria in enumerate(melhorias_selecionadas, 1):
                # Cabeçalho da melhoria
                story.append(Paragraph(f"<b>Melhoria {i}: {melhoria[4]}</b>", styles['Heading3']))
                
                # Tabela com informações detalhadas
                dados_melhoria = [
                    ['<b>Turno:</b>', melhoria[1]],
                    ['<b>Operador:</b>', melhoria[2]],
                    ['<b>Departamento:</b>', melhoria[3]],
                    ['<b>Tipo de Melhoria:</b>', melhoria[4]],
                    ['<b>Status:</b>', melhoria[7]],
                    ['<b>Data de Criação:</b>', melhoria[6]]
                ]
                
                if melhoria[9]:  # Responsável
                    dados_melhoria.append(['<b>Responsável:</b>', melhoria[9]])
                if melhoria[8]:  # Data de Conclusão
                    dados_melhoria.append(['<b>Data de Conclusão:</b>', melhoria[8]])
                
                tabela = Table(dados_melhoria, colWidths=[120, 350])
                tabela.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('BOLD', (0, 0), (0, -1), 1),
                ]))
                
                story.append(tabela)
                story.append(Spacer(1, 10))
                
                # Descrição detalhada
                story.append(Paragraph("<b>Descrição Detalhada:</b>", styles['Normal']))
                descricao_style = ParagraphStyle(
                    'DescricaoStyle',
                    parent=styles['Normal'],
                    leftIndent=20,
                    spaceAfter=12
                )
                story.append(Paragraph(melhoria[5], descricao_style))
                
                # Texto DDS personalizado por tipo de melhoria
                texto_dds = self.gerar_texto_dds(melhoria)
                dds_style = ParagraphStyle(
                    'DDSStyle',
                    parent=styles['Normal'],
                    backColor=colors.lightblue,
                    borderPadding=10,
                    leftIndent=10,
                    spaceAfter=15
                )
                story.append(Paragraph(f"<b>Análise para DDS:</b> {texto_dds}", dds_style))
                
                story.append(Spacer(1, 15))

            # Ações e compromissos
            story.append(Paragraph("<b>Ações e Compromissos:</b>", styles['Heading2']))
            compromissos = [
                "• Analisar cada sugestão apresentada com a equipe",
                "• Definir responsáveis para acompanhamento das melhorias",
                "• Estabelecer prazos realistas para implementação",
                "• Comunicar resultados e progressos à equipe",
                "• Reconhecer e valorizar as contribuições dos colaboradores",
                "• Documentar aprendizados e melhores práticas",
                "• Revisar periodicamente o status das melhorias",
                "• Incentivar a participação de todos os turnos"
            ]
            
            for compromisso in compromissos:
                story.append(Paragraph(compromisso, styles['Normal']))

            # Rodapé
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"<i>Relatório gerado automaticamente pelo LeanFlow em {datetime.now().strftime('%d/%m/%Y às %H:%M')}</i>", styles['Italic']))

            doc.build(story)
            messagebox.showinfo("Sucesso", f"📋 DDS gerado com sucesso: {filename}\n\nO relatório inclui todas as informações detalhadas das melhorias!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")

    def gerar_texto_dds(self, melhoria):
        """Gera texto personalizado para o DDS baseado no tipo de melhoria"""
        tipo = melhoria[4]
        descricao = melhoria[5]
        operador = melhoria[2]
        departamento = melhoria[3]
        turno = melhoria[1]
        
        textos_dds = {
            'Segurança': f"Sugestão de segurança proposta por {operador} do turno {turno} no {departamento}. "
                        f"A ideia '{descricao}' visa melhorar as condições de trabalho e prevenir acidentes. "
                        f"Devemos analisar a viabilidade técnica e implementar medidas que garantam um ambiente mais seguro para todos.",
            
            'Qualidade': f"Melhoria de qualidade sugerida por {operador} do {departamento}. "
                        f"A proposta '{descricao}' tem potencial para elevar nossos padrões de qualidade e satisfação do cliente. "
                        f"Recomendamos estudar o impacto nos processos e produtos antes da implementação.",
            
            'Produtividade': f"Sugestão de produtividade do {departamento} (turno {turno}). "
                           f"A ideia '{descricao}' pode otimizar nossos processos e reduzir tempos de produção. "
                           f"Vamos avaliar os ganhos potenciais e planejar a implementação de forma gradual.",
            
            'Custo': f"Redução de custos proposta por {operador}. "
                    f"A sugestão '{descricao}' identifica oportunidade clara de economia sem comprometer a qualidade. "
                    f"Precisamos analisar o retorno sobre o investimento e impactos operacionais.",
            
            'Organização': f"Melhoria organizacional do {departamento} (turno {turno}). "
                          f"A proposta '{descricao}' contribui para um ambiente mais organizado e eficiente. "
                          f"Vamos implementar e padronizar onde for possível, replicando para outras áreas.",
            
            'Outros': f"Sugestão de melhoria geral de {operador} do turno {turno}. "
                     f"A ideia '{descricao}' demonstra engajamento com a melhoria contínua. "
                     f"Vamos analisar cuidadosamente e implementar quando viável."
        }
        
        return textos_dds.get(tipo, 
            f"Sugestão de melhoria de {operador} do {departamento}. Vamos analisar e implementar quando viável.")

    def gerar_relatorio_estatistico(self):
        estatisticas = self.db.obter_estatisticas()
        total = sum(estatisticas.values())
        
        relatorio = "RELATÓRIO ESTATÍSTICO - MELHORIAS CONTÍNUAS\n"
        relatorio += "=" * 50 + "\n\n"
        relatorio += f"Total de Melhorias Registradas: {total}\n\n"
        
        for status, quantidade in estatisticas.items():
            percentual = (quantidade / total * 100) if total > 0 else 0
            relatorio += f"{status}: {quantidade} ({percentual:.1f}%)\n"
        
        self.texto_preview.delete(1.0, tk.END)
        self.texto_preview.insert(1.0, relatorio)