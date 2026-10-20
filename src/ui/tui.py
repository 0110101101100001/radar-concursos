import webbrowser
from textual import work, on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Input, Static, Label, Select, Button, Footer, Header
from textual.binding import Binding

from src.scrapers.pci import PCIScraper
from src.scrapers.ibfc import IBFCScraper
from src.scrapers.cebraspe import CebraspeScraper
from src.scrapers.fcc import FCCScraper
from src.scrapers.quadrix import QuadrixScraper
from src.core.filter import processar_e_filtrar

REGIOES = [
    ("Norte", "norte"), ("Nordeste", "nordeste"), ("Centro-Oeste", "centrooeste"),
    ("Sudeste", "sudeste"), ("Sul", "sul"), ("Nacional", "nacional")
]

CAT_FRAMES = [
    r"""
   /\_/\  
  ( o.o ) 
   > ^ <  
""",
    r"""
   /\_/\  
  ( -.o ) 
   > ^ <  
""",
    r"""
   /\_/\  
  ( o.o ) 
   > ^ <  
""",
    r"""
   /\_/\  
  ( o.- ) 
   > ^ <  
""",
    r"""
   /\_/\  
  ( -.- ) 
   > ^ <  
""",
]

CAT_DELAYS = [0.6, 0.2, 0.6, 0.2, 0.8]


class RadarTUI(App):
    # Desativa totalmente a paleta nativa e opções de tema
    COMMANDS = set()
    ENABLE_COMMAND_PALETTE = False

    CSS = """
    Screen {
        background: #1e1e1e;
        color: #cccccc;
    }

    Header {
        background: #1e1e1e;
        color: #cccccc;
        border-bottom: solid #333333;
    }

    Footer {
        background: #1e1e1e;
        color: #cccccc;
        border-top: solid #333333;
    }

    #sidebar {
        width: 32;
        height: 100%;
        border-right: solid #333333;
        padding: 1 2;
        background: #1e1e1e;
    }

    #main-content {
        width: 1fr;
        height: 100%;
        padding: 0;
        background: #1e1e1e;
    }

    .cat-art {
        text-align: center;
        color: #6a9955;
        text-style: bold;
        margin-top: 1;
        margin-bottom: 1;
    }

    .app-title {
        text-align: center;
        text-style: bold;
        color: #cccccc;
        margin-bottom: 2;
    }

    .section-label {
        color: #888888;
        margin-bottom: 1;
    }

    Select, Input {
        width: 100%;
        background: #252526;
        border: solid #333333;
        margin-bottom: 2;
        padding: 0 1;
    }

    Select:focus, Input:focus {
        border: solid #6a9955;
    }

    Button {
        width: 100%;
        background: #333333;
        color: #cccccc;
        border: none;
        text-style: none;
        margin-top: 1;
        margin-bottom: 2;
    }

    Button:hover {
        background: #6a9955;
        color: #1e1e1e;
        text-style: bold;
    }

    .help-text {
        color: #555555;
        text-align: center;
    }

    DataTable {
        height: 100%;
        border: none;
        background: #1e1e1e;
    }

    DataTable > .datatable--cursor {
        background: #2a2d2e;
        color: #cccccc;
        text-style: bold;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Sair", show=True),
        Binding("r", "atualizar", "Varrer", show=True),
        Binding("enter", "abrir_link", "Abrir", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Static(CAT_FRAMES[0], id="cat-frame", classes="cat-art")
                yield Static("RADAR CLI v2.1", classes="app-title")

                yield Static("Região:", classes="section-label")
                yield Select([(n, s) for n, s in REGIOES], value="nordeste", id="select-regiao")
                yield Static(id="regiao-info", classes="section-label")

                yield Static("Filtros (vírgula):", classes="section-label")
                yield Input(value="", id="input-filtros", placeholder="opcional: ce, fortaleza...")

                yield Button("Executar Varredura", id="btn-varrer")

                yield Static("q: Sair | r: Varrer", classes="help-text")
                yield Static("tab: Navegar | enter: Abrir", classes="help-text")

            with Vertical(id="main-content"):
                yield DataTable(id="tabela-concursos")

        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns("Banca", "Concurso / Vagas", "Status", "Link")
        self._cat_index = 0
        self._animate_cat_next()
        self.action_atualizar()

    def _animate_cat_next(self) -> None:
        """Avança para o próximo frame da animação do gato com delay individual."""
        try:
            self.query_one("#cat-frame", Static).update(CAT_FRAMES[self._cat_index])
            delay = CAT_DELAYS[self._cat_index]
            self._cat_index = (self._cat_index + 1) % len(CAT_FRAMES)
            self.set_timer(delay, self._animate_cat_next)
        except Exception:
            # Previne erros caso a janela seja fechada a meio de um timer
            pass

    def _atualizar_info_regiao(self, regiao_nome: str) -> None:
        """Atualiza a linha de informação da região na tela."""
        try:
            info = self.query_one("#regiao-info", Static)
            info.update(f"Região: {regiao_nome}")
        except Exception:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-varrer":
            self.action_atualizar()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "input-filtros":
            self.action_atualizar()

    @on(DataTable.RowSelected)
    def abrir_link_da_tabela(self, event: DataTable.RowSelected) -> None:
        table = event.data_table
        url = table.get_row_at(event.cursor_row)[3]
        if url.startswith("http"):
            webbrowser.open(url)

    def action_abrir_link(self) -> None:
        table = self.query_one(DataTable)
        if table.cursor_row is not None:
            url = table.get_row_at(table.cursor_row)[3]
            if url.startswith("http"):
                webbrowser.open(url)

    @work(exclusive=True, thread=True)
    def action_atualizar(self) -> None:
        self.call_from_thread(self.notify, "Extraindo dados da web...", title="Processando")

        def get_inputs():
            regiao = self.query_one("#select-regiao", Select).value
            filtros_raw = self.query_one("#input-filtros", Input).value
            return regiao, [f.strip() for f in filtros_raw.split(",") if f.strip()]

        regiao, filtros = self.call_from_thread(get_inputs)

        # Atualiza a info de região na tela
        regiao_nome = next((n for n, s in REGIOES if s == regiao), regiao)
        self.call_from_thread(self._atualizar_info_regiao, regiao_nome)

        dados_brutos = []
        dados_brutos.extend(PCIScraper().extrair(regiao_url=regiao))
        dados_brutos.extend(IBFCScraper().extrair())
        dados_brutos.extend(CebraspeScraper().extrair())
        dados_brutos.extend(FCCScraper().extrair())
        dados_brutos.extend(QuadrixScraper().extrair())

        df = processar_e_filtrar(dados_brutos, filtros, regiao)
        
        self.call_from_thread(self._atualizar_tabela, df, filtros, regiao_nome)

    def _atualizar_tabela(self, df, filtros, regiao_nome: str) -> None:
        table = self.query_one(DataTable)
        table.clear()

        if df is not None and not df.empty:
            for _, row in df.iterrows():
                table.add_row(row['fonte'], row['titulo'], row['status'], row['link'])
            self.notify(f"{len(df)} editais listados ({regiao_nome}).", title="Concluído")
        else:
            filtros_str = ', '.join(filtros) if filtros else "sem filtro extra"
            self.notify(f"Sem resultados para '{filtros_str}' na região {regiao_nome}.", title="Concluído")