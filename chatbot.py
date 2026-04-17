import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import os
from datetime import datetime
import sys  # NOVO IMPORT

class ChatbotLean:
    def __init__(self, frame):
        self.frame = frame
        self.usuario = {}
        self.estado = "inicio"
        self.historico = []
        self.imagens_carregadas = {}
        
        # ⬇️⬇️⬇️ NOVO: Determinar caminho base antes de carregar imagens ⬇️⬇️⬇️
        self.caminho_base = self.obter_caminho_imagens()
        print(f"📁 Caminho base das imagens: {self.caminho_base}")
        
        self.carregar_todas_imagens()
        self.carregar_conteudos_completos()
        self.criar_interface()
        self.iniciar_conversa()

    def obter_caminho_imagens(self):
        """Solução robusta para encontrar imagens em desenvolvimento e executável"""
        try:
            # Método 1: Se for executável PyInstaller
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
                images_path = os.path.join(base_path, 'images')
                print(f"🔍 Tentando executável: {images_path}")
                if os.path.exists(images_path):
                    return images_path
            
            # Método 2: Diretório do script atual
            script_dir = os.path.dirname(os.path.abspath(__file__))
            images_path = os.path.join(script_dir, 'images')
            print(f"🔍 Tentando script dir: {images_path}")
            if os.path.exists(images_path):
                return images_path
            
            # Método 3: Diretório de trabalho atual
            cwd = os.getcwd()
            images_path = os.path.join(cwd, 'images')
            print(f"🔍 Tentando diretório atual: {images_path}")
            if os.path.exists(images_path):
                return images_path
            
            # Método 4: Subpasta images no diretório atual
            images_path = 'images'
            print(f"🔍 Tentando subpasta: {images_path}")
            if os.path.exists(images_path):
                return images_path
                
            # Se nenhum funcionar, retorna o mais provável
            return os.path.join(os.path.dirname(__file__), 'images')
            
        except Exception as e:
            print(f"❌ Erro ao encontrar caminho: {e}")
            return 'images'

    def carregar_todas_imagens(self):
        """Carrega TODAS as imagens disponíveis incluindo o troféu"""
        # Lista completa das suas imagens
        todas_imagens = [
            'lean_principle1.jpg', 'lean_principle2.jpg', 'lean_principle3.jpg',
            'lean_principle4.jpg', 'lean_principle5.jpg', 'lean_principle6.jpg',
            'lean_principle7.jpg', 'kaizen.jpg', 'pdca.jpg', 
            'ferramentas_lean.jpg', 'importancia_lean.jpg', 'trofeu.jpg'
        ]
        
        print(f"🖼️ Iniciando carregamento de {len(todas_imagens)} imagens...")
        
        for imagem in todas_imagens:
            try:
                # ⬇️⬇️⬇️ ATUALIZADO: Usar caminho_base em vez de caminho fixo ⬇️⬇️⬇️
                caminho_completo = os.path.join(self.caminho_base, imagem)
                print(f"🔍 Procurando: {caminho_completo}")
                
                if os.path.exists(caminho_completo):
                    img = Image.open(caminho_completo)
                    # Tamanho maior para o troféu
                    if imagem == 'trofeu.jpg':
                        img = img.resize((350, 300), Image.Resampling.LANCZOS)
                    else:
                        img = img.resize((400, 250), Image.Resampling.LANCZOS)
                    self.imagens_carregadas[imagem] = ImageTk.PhotoImage(img)
                    print(f"✅ Imagem carregada: {imagem}")
                else:
                    print(f"❌ Imagem não encontrada: {caminho_completo}")
                    # Criar imagem placeholder
                    self.criar_imagem_placeholder(imagem)
                    
            except Exception as e:
                print(f"Erro ao carregar {imagem}: {e}")
                # Criar imagem placeholder em caso de erro
                self.criar_imagem_placeholder(imagem)

    def criar_imagem_placeholder(self, nome_imagem):
        """Cria uma imagem placeholder quando a original não é encontrada"""
        try:
            # Cria uma imagem colorida com texto
            if 'trofeu' in nome_imagem:
                img = Image.new('RGB', (350, 300), color='gold')
            else:
                img = Image.new('RGB', (400, 250), color='lightblue')
            
            self.imagens_carregadas[nome_imagem] = ImageTk.PhotoImage(img)
            print(f"🔄 Placeholder criado para: {nome_imagem}")
        except Exception as e:
            print(f"❌ Erro ao criar placeholder: {e}")

    def carregar_conteudos_completos(self):
        """Carrega conteúdos completos com TODAS as imagens"""
        self.conteudos = {
            '1': {
                'titulo': '🎯 INTRODUÇÃO AO LEAN MANUFACTURING',
                'texto': """🤔 O QUE É LEAN MANUFACTURING?

Sistema de produção enxuta desenvolvido pela Toyota que revolucionou a indústria mundial!

📚 HISTÓRIA:
• Desenvolvido no Japão pós-guerra (1950)
• Criado por Taiichi Ohno na Toyota
• Conhecido como Sistema Toyota de Produção
• Expandido para o mundo como "Lean"

🎯 OBJETIVO PRINCIPAL:
Eliminar TODOS os desperdícios do processo produtivo enquanto se entrega valor máximo ao cliente.

💡 CONCEITO CHAVE:
"Valor é definido pelo cliente - tudo que não agrega valor é desperdício"

🏭 ONDE SE APLICA:
• Manufatura e produção
• Serviços e escritórios  
• Saúde e hospitais
• Tecnologia e TI
• Construção civil
• Qualquer processo!""",
                'imagem': 'lean_principle1.jpg'
            },
            '2': {
                'titulo': '🔍 OS 5 PRINCÍPIOS FUNDAMENTAIS DO LEAN',
                'texto': """📋 OS 5 PRINCÍPIOS QUE TRANSFORMAM EMPRESAS:

1️⃣ DEFINIR VALOR 
   - O que o cliente realmente está disposto a pagar?
   - Entender necessidades específicas
   - Eliminar supérfluos

2️⃣ MAPEAR O FLUXO DE VALOR
   - Identificar TODAS as etapas do processo
   - Mapear fluxo atual (Value Stream Mapping)
   - Visualizar gargalos e desperdícios

3️⃣ CRIAR FLUXO CONTÍNUO  
   - Produto flui sem interrupções
   - Eliminar esperas e estoques
   - Reduzir lead time drasticamente

4️⃣ ESTABELECER SISTEMA PUXADA
   - Produzir APENAS sob demanda do cliente
   - Sistema Just-in-Time (JIT)
   - Reduzir estoques a quase zero

5️⃣ BUSCAR A PERFEIÇÃO
   - Melhoria contínua constante (Kaizen)
   - Nunca estar satisfeito
   - Evolução permanente""",
                'imagem': 'lean_principle2.jpg'
            },
            '3': {
                'titulo': '🚫 OS 7 TIPOS DE DESPERDÍCIOS (MUDA)',
                'texto': """📊 OS 7 INIMIGOS DA PRODUTIVIDADE:

1️⃣ SUPERPRODUÇÃO
   - Produzir mais que o necessário
   - Antes do momento certo
   - Maior desperdício de todos!

2️⃣ ESPERA
   - Pessoas esperando processos
   - Máquinas paradas
   - Tempo ocioso = dinheiro perdido

3️⃣ TRANSPORTE
   - Movimentação desnecessária
   - Layout inadequado
   - Deslocamentos sem valor

4️⃣ PROCESSAMENTO INADEQUADO
   - Métodos ineficientes
   - Ferramentas inadequadas
   - Processos desnecessários

5️⃣ ESTOQUE
   - Matéria-prima em excesso
   - Produtos em processo
   - Produtos acabados parados

6️⃣ MOVIMENTO
   - Deslocamentos desnecessários
   - Busca por ferramentas
   - Posturas inadequadas

7️⃣ DEFEITOS
   - Retrabalho constante
   - Inspeções excessivas
   - Produtos rejeitados

💡 IMPACTO: Eliminar estes 7 pode aumentar produtividade em 30-50%!""",
                'imagem': 'lean_principle3.jpg'
            },
            '4': {
                'titulo': '📈 KAIZEN - FILOSOFIA DA MELHORIA CONTÍNUA',
                'texto': """🎯 SIGNIFICADO PROFUNDO:
"Kai" = Mudança | "Zen" = Melhor
"Mudança para melhor - todos os dias!"

🔧 COMO FUNCIONA NA PRÁTICA:
• Pequenas melhorias DIÁRIAS
• Envolvimento de TODOS os colaboradores
• Foco no PROCESSO, não nas pessoas
• Baseado em DADOS e FATOS reais
• Baixo custo ou custo zero

📊 RESULTADOS COMPROVADOS:
• +30-50% em Produtividade
• -20-40% em Custos operacionais  
• +40-60% em Qualidade
• +70% em Engajamento da equipe
• -50-90% em Lead time

🛠️ FERRAMENTAS KAIZEN:
• Gemba Walk (vá até o local real)
• 5 Porquês (análise de causa raiz)
• Diagrama de Ishikawa
• PDCA (ciclo de melhoria)

💬 FRASE FAMOSA DO KAIZEN:
"Hoje melhor que ontem, amanhã melhor que hoje - SEMPRE!"

🏆 EMPRESAS QUE USAM KAIZEN:
Toyota, Sony, Honda, Nissan, 3M, Amazon e milhares!""",
                'imagem': 'kaizen.jpg'
            },
            '5': {
                'titulo': '🔄 CICLO PDCA - RODA DA MELHORIA CONTÍNUA',
                'texto': """📋 PLAN (PLANEJAR) - FASE DA ESTRATÉGIA:
• Identificar problema/oportunidade claramente
• Analisar causas raiz (método 5 Porquês)
• Desenvolver plano de ação DETALHADO
• Estabelecer metas SMART
• Definir indicadores de performance (KPIs)

⚡ DO (EXECUTAR) - FASE DA AÇÃO:
• Implementar plano PASSO A PASSO
• Coletar dados SISTEMATICAMENTE
• Treinar TODAS as pessoas envolvidas
• Documentar TODO o processo
• Comunicar progresso constantemente

🔍 CHECK (VERIFICAR) - FASE DA ANÁLISE:
• Analisar resultados OBTIDOS
• Comparar com metas ESTABELECIDAS
• Identificar desvios e GAPS
• Validar EFICÁCIA das ações
• Aprender com os RESULTADOS

🎯 ACT (AGIR) - FASE DA PADRONIZAÇÃO:
• Padronizar soluções BEM-SUCEDIDAS
• Corrigir desvios IDENTIFICADOS
• Documentar APRENDIZADOS
• Compartilhar MELHORES PRÁTICAS
• REINICIAR o ciclo com novo plano

🔄 PDCA É CONTÍNUO: Planejar → Fazer → Verificar → Agir → REPETIR!""",
                'imagem': 'pdca.jpg'
            },
            '6': {
                'titulo': '🧹 5S - PROGRAMA DE ORGANIZAÇÃO E QUALIDADE',
                'texto': """1️⃣ SEIRI - SENSO DE UTILIZAÇÃO:
• Separar útil do inútil RADICALMENTE
• Eliminar itens DESNECESSÁRIOS
• Liberar ESPAÇO físico e mental
• Reduzir CUSTOS de armazenamento

2️⃣ SEITON - SENSO DE ORGANIZAÇÃO:
• Um lugar para CADA coisa
• Cada coisa em SEU lugar
• Identificação VISUAL clara
• Facilidade de ENCONTRO

3️⃣ SEISO - SENSO DE LIMPEZA:
• Limpar e INSPECIONAR
• Manter ambiente IMACULADO
• Identificar problemas POTENCIAIS
• Prevenir sujeira na FONTE

4️⃣ SEIKETSU - SENSO DE SAÚDE/PADRONIZAÇÃO:
• Padronizar os 3S ANTERIORES
• Manter condições IDEAIS
• Criar padrões VISUAIS
• Estabelecer PROCEDIMENTOS

5️⃣ SHITSUKE - SENSO DE AUTODISCIPLINA:
• Tornar HÁBITO natural
• Manter padrões CONSISTENTEMENTE
• Respeitar REGRAS estabelecidas
• Melhorar CONTINUAMENTE

🏆 RESULTADOS DO 5S:
• +40% em Segurança no trabalho
• +30% em Produtividade
• +50% em Organização visual
• -60% em Tempos de busca
• +80% em Satisfação da equipe""",
                'imagem': 'lean_principle4.jpg'
            },
            '7': {
                'titulo': '📊 BENEFÍCIOS TANGÍVEIS DO LEAN',
                'texto': """🎯 PARA A EMPRESA - RESULTADOS FINANCEIROS:
• Redução de custos: 20-40%
• Aumento de produtividade: 30-50%
• Melhoria de qualidade: 40-80%
• Redução de lead time: 50-90%
• Aumento de capacidade: 25-40%
• Melhor utilização de espaço: 30-50%
• Redução de estoques: 50-80%

👥 PARA OS COLABORADORES - QUALIDADE DE VIDA:
• Ambiente de trabalho 70% mais seguro
• Maior satisfação no trabalho (+60%)
• Desenvolvimento profissional CONTÍNUO
• Participação ativa nas melhorias
• Reconhecimento pelas contribuições
• Clima organizacional positivo

📈 PARA OS CLIENTES - VALOR PERCEBIDO:
• Produtos com MELHOR qualidade
• Entregas mais RÁPIDAS e confiáveis
• Preços mais COMPETITIVOS
• Melhor atendimento e suporte
• Maior variedade de opções
• Prazos cumpridos rigorosamente

🌍 IMPACTO SUSTENTÁVEL - MEIO AMBIENTE:
• Redução de 40% em desperdícios ambiental
• Uso 50% mais eficiente de recursos
• Operações mais SUSTENTÁVEIS
• Menor impacto ecológico
• Consumo consciente de energia

🏆 LEAN É GANHA-GANHA: Todos saem beneficiados - empresa, colaboradores, clientes e sociedade!""",
                'imagem': 'importancia_lean.jpg'
            },
            '8': {
                'titulo': '🛠️ FERRAMENTAS LEAN AVANÇADAS',
                'texto': """🔧 PRINCIPAIS FERRAMENTAS DE IMPLEMENTAÇÃO:

📋 VALUE STREAM MAPPING (VSM)
- Mapeamento completo do fluxo de valor
- Identificação visual de desperdícios
- Análise do estado atual vs. estado futuro

🎯 KANBAN - SISTEMA VISUAL
- Controle visual da produção
- Sistema puxado eficiente
- Cartões para sinalização de demanda

⚡ JIDOKA - AUTONOMAÇÃO
- "Autonomia com toque humano"
- Máquinas param automaticamente em defeitos
- Qualidade built-in no processo

🔧 TPM - MANUTENÇÃO PRODUTIVA TOTAL
- Manutenção preventiva sistemática
- Envolvimento de todos os operadores
- Zero quebras, zero defeitos

🎯 POKA-YOKE - A PROVA DE ERROS
- Dispositivos à prova de erros
- Prevenção de defeitos na fonte
- Simplicidade e eficácia

📊 HEIJUNKA - NIVELAMENTO DA PRODUÇÃO
- Suavização do mix e volume
- Redução de picos e vales
- Estabilidade operacional""",
                'imagem': 'ferramentas_lean.jpg'
            },
            '9': {
                'titulo': '🏭 CASOS DE SUCESSO LEAN',
                'texto': """🚗 TOYOTA - O PIONEIRO:
- Criador do Sistema Toyota de Produção
- Referência mundial em Lean Manufacturing
- Modelo estudado por todas as indústrias

🏢 TOYOTA DO BRASIL:
- Fábrica em Sorocaba/SP
- Prêmios de qualidade e produtividade
- Exportação para toda América Latina

⚡ GENERAL ELECTRIC (GE):
- Implementação do Lean Six Sigma
- Revolução nos processos administrativos
- Bilhões em economia

🏥 HOSPITAL SIRIO-LIBANÊS:
- Lean Healthcare no Brasil
- Redução de 60% no tempo de espera
- Melhoria na segurança do paciente

✈️ EMBRAER - AERONÁUTICA:
- Lean Aerospace aplicado
- Redução de 40% no ciclo de produção
- Competitividade internacional

📦 AMAZON - LOGÍSTICA:
- Sistema de picking e packing Lean
- Entregas ultra-rápidas
- Otimização de centros de distribuição

🏭 INDÚSTRIA NACIONAL:
- Centenas de empresas brasileiras
- Setores: automotivo, alimentos, têxtil
- Resultados comprovados!""",
                'imagem': 'lean_principle5.jpg'
            },
            '10': {
                'titulo': '📈 COMO IMPLEMENTAR LEAN NA SUA EMPRESA',
                'texto': """🎯 PASSO A PASSO DA IMPLEMENTAÇÃO:

1️⃣ DIAGNÓSTICO INICIAL
   - Análise da situação atual
   - Identificação de oportunidades
   - Engajamento da liderança

2️⃣ FORMAÇÃO DA EQUIPE
   - Seleção de multiplicadores
   - Treinamento intensivo
   - Definição de papéis

3️⃣ PROJETOS PILOTO
   - Escolha de áreas estratégicas
   - Implementação controlada
   - Primeiros resultados rápidos

4️⃣ EXPANSÃO GRADUAL
   - Replicação de sucessos
   - Ajustes baseados em learning
   - Engajamento de toda empresa

5️⃣ CONSOLIDAÇÃO
   - Padronização de processos
   - Medição contínua de resultados
   - Cultura de melhoria contínua

⏱️ TIMELINE TÍPICA:
- Meses 1-3: Diagnóstico e treinamento
- Meses 4-6: Projetos piloto
- Meses 7-12: Expansão inicial
- Ano 2: Consolidação e crescimento

💡 DICAS DE SUCESSO:
- Comece PEQUENO e cresça
- Comemore CADA vitória
- Envolva TODOS os níveis
- Seja PERSISTENTE""",
                'imagem': 'lean_principle6.jpg'
            },
            '11': {
                'titulo': '🌟 O FUTURO DO LEAN - INDÚSTRIA 4.0',
                'texto': """🔮 LEAN 4.0 - A EVOLUÇÃO:

🤖 INTELIGÊNCIA ARTIFICIAL + LEAN
- Análise preditiva de dados
- Otimização automática de processos
- Manutenção preventiva inteligente

📱 IOT (INTERNET DAS COISAS)
- Sensores em tempo real
- Coleta automática de dados
- Monitoramento contínuo

☁️ BIG DATA & ANALYTICS
- Análise de grandes volumes
- Identificação de padrões
- Tomada de decisão baseada em dados

🤝 LEAN + DIGITAL TRANSFORMATION
- Processos digitais enxutos
- Automação inteligente
- Eficiência exponencial

🌍 SUSTENTABILIDADE 4.0
- Lean Green Manufacturing
- Eficiência energética
- Economia circular

🎯 COMPETITIVIDADE GLOBAL
- Empresas mais ágeis
- Adaptação rápida a mudanças
- Inovação constante

🚀 O FUTURO É LEAN: A metodologia que revolucionou o século 20 continuará essencial no século 21!""",
                'imagem': 'lean_principle7.jpg'
            }
        }

    def criar_interface(self):
        """Cria a interface do chatbot"""
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Título
        titulo = ttk.Label(main_frame, text="🤖 Chatbot Lean - Seu Professor de Melhoria Contínua", 
                          font=('Arial', 14, 'bold'), foreground='darkblue')
        titulo.pack(pady=(0, 10))

        # Frame principal
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill='both', expand=True)

        # Área de conversa (esquerda)
        conversa_frame = ttk.LabelFrame(content_frame, text="💬 Conversa Interativa", padding=5)
        conversa_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Área de chat
        self.area_chat = scrolledtext.ScrolledText(conversa_frame, height=15, 
                                                  wrap=tk.WORD, font=('Arial', 10),
                                                  state='disabled')
        self.area_chat.pack(fill='both', expand=True, pady=(0, 10))

        # Frame de entrada
        entrada_frame = ttk.Frame(conversa_frame)
        entrada_frame.pack(fill='x')

        ttk.Label(entrada_frame, text="Digite sua resposta:", 
                 font=('Arial', 9)).pack(anchor='w')

        self.entrada_mensagem = ttk.Entry(entrada_frame, font=('Arial', 11))
        self.entrada_mensagem.pack(fill='x', pady=5)
        self.entrada_mensagem.bind('<Return>', self.enviar_mensagem)

        btn_enviar = ttk.Button(entrada_frame, text="Enviar Mensagem", 
                               command=self.enviar_mensagem)
        btn_enviar.pack(pady=5)

        # Área educacional (direita)
        educacao_frame = ttk.LabelFrame(content_frame, text="📚 Conteúdo Educacional", padding=5)
        educacao_frame.pack(side='right', fill='both', expand=True)

        self.titulo_conteudo = ttk.Label(educacao_frame, text="Escolha um tema no chat!", 
                                       font=('Arial', 11, 'bold'), foreground='darkgreen',
                                       wraplength=350)
        self.titulo_conteudo.pack(pady=(0, 5))

        self.label_imagem = ttk.Label(educacao_frame, background='white', 
                                     relief='solid', borderwidth=1,
                                     text="Imagem aparecerá aqui\n\n💡 Escolha um tema de 1 a 11")
        self.label_imagem.pack(fill='both', expand=True, pady=5)

        self.texto_educacional = scrolledtext.ScrolledText(educacao_frame, height=10,
                                                          wrap=tk.WORD, font=('Arial', 9),
                                                          state='disabled')
        self.texto_educacional.pack(fill='both', expand=True)

    def iniciar_conversa(self):
        """Inicia a conversa com o usuário"""
        self.adicionar_mensagem_bot("""🤖 OLÁ! Eu sou o Assistente Lean!

Vou te guiar no aprendizado sobre Lean Manufacturing e Melhoria Contínua.

Para começarmos, por favor me diga:
👉 Qual é o seu nome?""")
        
        self.entrada_mensagem.focus()
        self.estado = "aguardando_nome"

    def enviar_mensagem(self, event=None):
        """Processa a mensagem do usuário"""
        mensagem = self.entrada_mensagem.get().strip()
        
        if not mensagem:
            return

        self.entrada_mensagem.delete(0, tk.END)
        self.adicionar_mensagem_usuario(mensagem)

        # Se estiver finalizado, volta para o menu
        if self.estado == "finalizado":
            self.voltar_ao_menu()
            return

        if self.estado == "aguardando_nome":
            self.processar_nome(mensagem)
        elif self.estado == "aguardando_turno":
            self.processar_turno(mensagem)
        elif self.estado == "aguardando_cargo":
            self.processar_cargo(mensagem)
        elif self.estado == "aguardando_tema":
            self.processar_tema(mensagem)

    def voltar_ao_menu(self):
        """Volta para o menu principal"""
        self.adicionar_mensagem_bot("""🔁 Voltando ao menu principal!

📚 ESCOLHA UM TEMA PARA APRENDER:

1️⃣ 🎯 Introdução ao Lean
2️⃣ 🔍 5 Princípios Fundamentais  
3️⃣ 🚫 7 Desperdícios (Muda)
4️⃣ 📈 Kaizen - Melhoria Contínua
5️⃣ 🔄 Ciclo PDCA
6️⃣ 🧹 Metodologia 5S
7️⃣ 📊 Benefícios do Lean
8️⃣ 🛠️ Ferramentas Lean Avançadas
9️⃣ 🏭 Casos de Sucesso
🔟 📈 Como Implementar
1️⃣1️⃣ 🌟 Futuro do Lean

0️⃣ 🔄 Reiniciar Conversa

👉 Digite o número do tema (0-11):""")
        
        self.estado = "aguardando_tema"
        self.entrada_mensagem.focus()

    def processar_nome(self, nome):
        """Processa o nome do usuário"""
        self.usuario['nome'] = nome
        self.adicionar_mensagem_bot(f"👋 Prazer em conhecê-lo, {nome}!")
        
        self.adicionar_mensagem_bot("""Agora me conta:
👉 Em qual turno você trabalha?
1 - Manhã
2 - Tarde  
3 - Noite
4 - Administrativo

Digite o número:""")
        
        self.estado = "aguardando_turno"
        self.entrada_mensagem.focus()

    def processar_turno(self, turno):
        """Processa o turno do usuário"""
        turnos = {
            '1': 'Manhã', '2': 'Tarde', '3': 'Noite', '4': 'Administrativo',
            'manhã': 'Manhã', 'manha': 'Manhã', 'tarde': 'Tarde', 
            'noite': 'Noite', 'adm': 'Administrativo'
        }
        
        turno = turno.lower()
        if turno in turnos:
            self.usuario['turno'] = turnos[turno]
            self.adicionar_mensagem_bot(f"⏰ Turno da {turnos[turno]} - excelente!")
        else:
            self.usuario['turno'] = turno
            self.adicionar_mensagem_bot(f"⏰ {turno.capitalize()} - entendido!")
        
        self.adicionar_mensagem_bot("""Agora me diga:
👉 Qual é o seu cargo/função?
(ex: Operador, Supervisor, Gerente, Analista, etc.)""")
        
        self.estado = "aguardando_cargo"
        self.entrada_mensagem.focus()

    def processar_cargo(self, cargo):
        """Processa o cargo do usuário"""
        self.usuario['cargo'] = cargo
        self.adicionar_mensagem_bot(f"💼 {cargo} - função muito importante!")
        
        self.mostrar_menu_principal()

    def mostrar_menu_principal(self):
        """Mostra o menu principal completo"""
        boas_vindas = f"""🎉 PERFEITO, {self.usuario['nome']}!

Agora vamos explorar o mundo do Lean Manufacturing!

📚 ESCOLHA UM TEMA PARA COMEÇAR:

1️⃣ 🎯 Introdução ao Lean
2️⃣ 🔍 5 Princípios Fundamentais  
3️⃣ 🚫 7 Desperdícios (Muda)
4️⃣ 📈 Kaizen - Melhoria Contínua
5️⃣ 🔄 Ciclo PDCA
6️⃣ 🧹 Metodologia 5S
7️⃣ 📊 Benefícios do Lean
8️⃣ 🛠️ Ferramentas Lean Avançadas
9️⃣ 🏭 Casos de Sucesso
🔟 📈 Como Implementar
1️⃣1️⃣ 🌟 Futuro do Lean

0️⃣ 🔄 Reiniciar Conversa

👉 Digite o número do tema (0-11):"""
        
        self.adicionar_mensagem_bot(boas_vindas)
        self.estado = "aguardando_tema"
        self.entrada_mensagem.focus()

    def processar_tema(self, opcao):
        """Processa a escolha do tema"""
        if opcao == '0':
            self.reiniciar_conversa()
            return
            
        if opcao in self.conteudos:
            conteudo = self.conteudos[opcao]
            self.mostrar_conteudo_educacional(conteudo)
            
            self.adicionar_mensagem_bot(f"📖 {conteudo['titulo']}")
            
            continuar = """💡 Gostou do conteúdo?

📚 Quer explorar outro tema?

Digite 1-11 para outro tema
Digite 0 para voltar ao menu
Digite 'sair' para finalizar

👉 Sua escolha:"""
            
            self.adicionar_mensagem_bot(continuar)
            self.entrada_mensagem.focus()
            
        elif opcao.lower() in ['sair', 'exit', 'quit']:
            self.mostrar_mensagem_final()
        else:
            self.adicionar_mensagem_bot("""❌ Número inválido. 

📚 Temas disponíveis:

1️⃣ 🎯 Introdução ao Lean
2️⃣ 🔍 5 Princípios  
3️⃣ 🚫 7 Desperdícios
4️⃣ 📈 Kaizen
5️⃣ 🔄 PDCA
6️⃣ 🧹 5S
7️⃣ 📊 Benefícios
8️⃣ 🛠️ Ferramentas
9️⃣ 🏭 Casos de Sucesso
🔟 📈 Implementação
1️⃣1️⃣ 🌟 Futuro do Lean

0️⃣ 🔄 Menu Principal

👉 Digite um número de 0 a 11:""")
            self.entrada_mensagem.focus()

    def mostrar_mensagem_final(self):
        """Mostra mensagem final personalizada com troféu"""
        nome = self.usuario.get('nome', 'Colaborador')
        turno = self.usuario.get('turno', 'seu turno')
        cargo = self.usuario.get('cargo', 'sua função')
        
        mensagem_final = f"""
🏆 PARABÉNS, {nome.upper()}! 🏆

📊 CERTIFICADO DE CONCLUSÃO - FORMAÇÃO LEAN

👤 DADOS DO PARTICIPANTE:
• Nome: {nome}
• Turno: {turno}
• Cargo: {cargo}
• Data: {self.obter_data_atual()}

🎯 SUA JORNADA LEAN:

Você completou com sucesso o programa de aprendizado em 
Lean Manufacturing e Melhoria Contínua!

💡 MENSAGEM FINAL:

"A jornada Lean não termina aqui - ela apenas começa. 
Cada dia é uma nova oportunidade para eliminar desperdícios, 
melhorar processos e criar mais valor. 

Lembre-se: pequenas melhorias diárias levam a grandes 
resultados no longo prazo. Seja um agente de mudança 
em sua área e inspire outros com seu exemplo."

🏭 RECONHECIMENTO TÉCNICO:

Em nome de toda a organização, reconhecemos seu comprometimento 
com o aprendizado contínuo e desenvolvimento profissional. 
Suas novas habilidades em Lean serão valiosas para:

• Otimização de processos no turno {turno}
• Contribuições significativas como {cargo}
• Fortalecimento da cultura de melhoria contínua
• Geração de resultados tangíveis para a empresa

🚀 PRÓXIMOS PASSOS:

1. Aplique pelo menos UMA melhoria esta semana
2. Compartilhe seu conhecimento com a equipe
3. Continue buscando oportunidades de melhoria
4. Participe ativamente dos DDS e reuniões Lean

🌟 VOCÊ FAZ A DIFERENÇA!

O sucesso da transformação Lean depende de colaboradores 
comprometidos como você. Continue sendo referência em 
melhoria contínua!

🔁 Volte sempre que quiser revisitar os conceitos!

🤖 Assistente Lean - Parceiro da sua evolução profissional
        """
        
        self.adicionar_mensagem_bot(mensagem_final)
        
        # Mostrar imagem do troféu
        self.mostrar_trofeu()
        
        self.estado = "finalizado"

    def mostrar_trofeu(self):
        """Mostra a imagem do troféu na área educacional"""
        if 'trofeu.jpg' in self.imagens_carregadas:
            self.titulo_conteudo.configure(text="🏆 CERTIFICADO DE CONCLUSÃO 🏆")
            self.label_imagem.configure(image=self.imagens_carregadas['trofeu.jpg'])
            
            texto_certificado = f"""🎉 PARABÉNS PELA CONCLUSÃO!

{self.usuario.get('nome', 'Colaborador')}
{self.usuario.get('cargo', 'Função')}
Turno: {self.usuario.get('turno', 'Turno')}

✅ Concluiu com sucesso o programa
de aprendizado em Lean Manufacturing

📅 {self.obter_data_atual()}

🌟 Continue sua jornada de melhoria!"""
            
            self.texto_educacional.config(state='normal')
            self.texto_educacional.delete(1.0, tk.END)
            self.texto_educacional.insert(1.0, texto_certificado)
            self.texto_educacional.config(state='disabled')
        else:
            self.label_imagem.configure(text="🏆 Parabéns pela Conclusão!")

    def obter_data_atual(self):
        """Retorna a data atual formatada"""
        return datetime.now().strftime("%d/%m/%Y")

    def reiniciar_conversa(self):
        """Reinicia a conversa do zero"""
        self.usuario = {}
        self.estado = "inicio"
        self.area_chat.config(state='normal')
        self.area_chat.delete(1.0, tk.END)
        self.area_chat.config(state='disabled')
        
        self.titulo_conteudo.configure(text="Escolha um tema no chat!")
        self.label_imagem.configure(text="Imagem aparecerá aqui\n\n💡 Escolha um tema de 1 a 11")
        self.texto_educacional.config(state='normal')
        self.texto_educacional.delete(1.0, tk.END)
        self.texto_educacional.config(state='disabled')
        
        self.iniciar_conversa()

    def mostrar_conteudo_educacional(self, conteudo):
        """Mostra o conteúdo educacional"""
        self.titulo_conteudo.configure(text=conteudo['titulo'])

        if conteudo['imagem'] in self.imagens_carregadas:
            self.label_imagem.configure(image=self.imagens_carregadas[conteudo['imagem']])
        else:
            self.label_imagem.configure(text=f"📷 {conteudo['titulo']}\n\n(Imagem ilustrativa)")

        self.texto_educacional.config(state='normal')
        self.texto_educacional.delete(1.0, tk.END)
        self.texto_educacional.insert(1.0, conteudo['texto'])
        self.texto_educacional.config(state='disabled')

    def adicionar_mensagem_bot(self, mensagem):
        """Adiciona mensagem do bot"""
        self.area_chat.config(state='normal')
        self.area_chat.insert(tk.END, f"\n🤖 ASSISTENTE LEAN:\n{mensagem}\n" + "─"*50 + "\n")
        self.area_chat.config(state='disabled')
        self.area_chat.see(tk.END)

    def adicionar_mensagem_usuario(self, mensagem):
        """Adiciona mensagem do usuário"""
        self.area_chat.config(state='normal')
        self.area_chat.insert(tk.END, f"\n👤 {self.usuario.get('nome', 'Você')}: {mensagem}\n")
        self.area_chat.config(state='disabled')
        self.area_chat.see(tk.END)