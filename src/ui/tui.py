import webbrowser
from textual import work, on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Input, Static, Button, Footer
from textual.binding import Binding

from src.scrapers.pci import PCIScraper
from src.scrapers.ibfc import IBFCScraper
from src.scrapers.cebraspe import CebraspeScraper
from src.scrapers.fcc import FCCScraper
from src.scrapers.quadrix import QuadrixScraper
from src.core.filter import processar_e_filtrar

REGIOES = [
    ("Nordeste", "nordeste"), ("Norte", "norte"), ("C-Oeste", "centrooeste"),
    ("Sudeste", "sudeste"), ("Sul", "sul"), ("Nacional", "nacional")
]

# Gato laranja estático alinhado (todas as linhas começam com braille blank)
GATO_ESTATICO = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠏⡆⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣀⡀
⠀⠀⠀⠀⠀⡟⢦⡀ ⠀⠀⣀⠞⠀⠀⠘⡀⢀⡠⠚⣉⠤⠂⠀⠀⠀⠈⠙⢦⡀
⠀⠀⠀⠀⠀⡇⠀⠉⠒⠊⠁⠀⠀⠀⠀⠀⠘⢧⠔⣉⠤⠒⠒⠉⠉⠀⠀⠀⠀⠹⣆
⠀⠀⠀⠀⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠀⠀⣤⠶⠶⢶⡄⠀⠀⠀⠀⢹⡆
⠀⣀⠤⠒⠒⢺⠒⠀⠀⠀⠀⠀⠀⠀⠀⠤⠊⠀⢸⠀⡿⠀⡀⠀⣀⡟⠀⠀⠀⠀⢸⡇
⠈⠀⠀⠀⠣⠴⠚⢯⡀⠐⠒⠚⠉⠀⢶⠂⠀⣀⠜⠀⢿⡀⠉⠚⠉⠀⠀⠀⠀⣠⠟
⠀⠠⠊⠀⠀⠀⠀⠀⠙⠂⣴⠒⠒⣲⢔⠉⠉⣹⣞⣉⣈⠿⢦⣀⣀⣀⣠⡴⠟

"""


class RadarTUI(App):
    COMMANDS = set()
    ENABLE_COMMAND_PALETTE = False
    regiao_atual = "nordeste"

    CSS = """
    * {
        scrollbar-background: #1e1d1d;
        scrollbar-color: #3b3937;
        scrollbar-color-hover: #d97757;
        scrollbar-color-active: #d97757;
    }

    Screen {
        background: #1e1d1d;
        color: #e6e4e0;
    }

    #top-panel {
        height: auto;
        min-height: 9;
        background: #1e1d1d;
        border-bottom: solid #3b3937;
        padding: 1 2;
    }

    /* Caixa com largura otimizada para o gato estático */
    #cat-box {
        width: 44;
        height: 8;
        content-align: center middle;
    }

    .cat-art {
        color: #d97757;
        text-style: bold;
    }

    #controls-box {
        width: 1fr;
        height: auto;
        padding-left: 2;
    }

    .app-title {
        color: #d97757;
        text-style: bold;
        margin-bottom: 1;
    }

    #region-tabs {
        height: auto;
        margin-bottom: 1;
    }

    .region-tab {
        width: auto;
        min-width: 8;
        height: 1;
        background: #1e1d1d;
        color: #8c8885;
        border: none;
        margin-right: 2;
        text-align: center;
    }

    .region-tab:hover {
        color: #e6e4e0;
        text-style: bold;
    }

    .region-tab.active {
        color: #d97757;
        text-style: bold;
        background: #2a2828;
    }

    #search-bar {
        height: auto;
    }

    Input {
        width: 1fr;
        height: 1;
        background: #2a2828;
        border: none;
        padding: 0 1;
        color: #e6e4e0;
        margin-right: 2;
    }

    Input:focus {
        background: #3b3937;
        border: none;
    }

    #btn-varrer {
        width: 12;
        height: 1;
        background: #d97757;
        color: #1e1d1d;
        text-style: bold;
        border: none;
        margin-right: 2;
    }

    #btn-varrer:hover {
        background: #e6e4e0;
    }

    #status-badge {
        width: 18;
        height: 1;
        content-align: center middle;
    }

    .status-idle { color: #8c8885; }
    .status-running { color: #d97757; text-style: bold; }

    DataTable {
        height: 1fr;
        border: none;
        background: #1e1d1d;
    }

    DataTable > .datatable--cursor {
        background: #2a2828;
        color: #d97757;
        text-style: bold;
    }

    Footer {
        background: #1e1d1d;
        color: #8c8885;
        border-top: solid #3b3937;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Sair", show=True),
        Binding("r", "atualizar", "Varrer", show=True),
        Binding("enter", "abrir_link", "Abrir Edital", show=True),
    ]

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id="top-panel"):
                with Vertical(id="cat-box"):
                    yield Static(GATO_ESTATICO.strip(), classes="cat-art")

                with Vertical(id="controls-box"):
                    yield Static("RADAR CLI", classes="app-title")

                    with Horizontal(id="region-tabs"):
                        for label, val in REGIOES:
                            classes = "region-tab active" if val == self.regiao_atual else "region-tab"
                            yield Button(label, id=f"reg-{val}", classes=classes)

                    with Horizontal(id="search-bar"):
                        yield Input(value="", id="input-filtros", placeholder=">> filtros: ce, fortaleza, ti...")
                        yield Button("Varrer", id="btn-varrer")
                        yield Static("[ IDLE ]", id="status-badge", classes="status-idle")

            yield DataTable(id="tabela-concursos")

        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns("Status", "Banca", "Concurso / Vagas", "Link")
        self.action_atualizar()

    def _atualizar_badge_status(self, texto: str, is_running: bool) -> None:
        try:
            badge = self.query_one("#status-badge", Static)
            badge.update(texto)
            if is_running:
                badge.remove_class("status-idle")
                badge.add_class("status-running")
            else:
                badge.remove_class("status-running")
                badge.add_class("status-idle")
        except Exception:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "btn-varrer":
            self.action_atualizar()
        elif btn_id and btn_id.startswith("reg-"):
            nova_regiao = btn_id.replace("reg-", "")
            self.regiao_atual = nova_regiao

            for btn in self.query(".region-tab"):
                if btn.id == btn_id:
                    btn.add_class("active")
                else:
                    btn.remove_class("active")

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
        self.call_from_thread(self._atualizar_badge_status, "[ VARRENDO... ]", True)

        def get_inputs():
            filtros_raw = self.query_one("#input-filtros", Input).value
            return self.regiao_atual, [f.strip() for f in filtros_raw.split(",") if f.strip()]

        regiao, filtros = self.call_from_thread(get_inputs)

        dados_brutos = []
        dados_brutos.extend(PCIScraper().extrair(regiao_url=regiao))
        dados_brutos.extend(IBFCScraper().extrair())
        dados_brutos.extend(CebraspeScraper().extrair())
        dados_brutos.extend(FCCScraper().extrair())
        dados_brutos.extend(QuadrixScraper().extrair())

        df = processar_e_filtrar(dados_brutos, filtros, regiao)
        self.call_from_thread(self._atualizar_tabela, df)

    def _atualizar_tabela(self, df) -> None:
        table = self.query_one(DataTable)
        table.clear()

        if df is not None and not df.empty:
            for _, row in df.iterrows():
                table.add_row(row['status'], row['fonte'], row['titulo'], row['link'])

        self._atualizar_badge_status("[ IDLE ]", False)
