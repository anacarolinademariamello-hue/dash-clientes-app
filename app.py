"""
Gerenciar Clientes · Dash Digital
Plataforma independente de cadastro e gestão de clientes.
Dados salvos no Supabase e compartilhados com todas as plataformas da agência.
"""
import json
import base64
import requests
import streamlit as st

NICHES = [
    "Saúde & Bem-estar",
    "Educação & Capacitação",
    "Negócios & Empreendedorismo",
    "Moda & Beleza",
    "Alimentação & Gastronomia",
    "Casa & Decoração",
    "Tecnologia & Digital",
    "Imóveis",
    "Automotivo",
    "Turismo & Viagens",
    "Serviços Profissionais",
    "Pet & Animais",
    "Infantil & Família",
    "Finanças & Investimentos",
    "Religião & Espiritualidade",
    "Esportes & Lazer",
    "Arte & Entretenimento",
    "Agronegócio",
]

SUB_NICHES = {
    "Saúde & Bem-estar":           ["Nutrição e Emagrecimento","Personal Trainer","Academia / Fitness","Yoga e Pilates","Psicologia e Terapia","Medicina Estética","Odontologia","Suplementos e Nutracêuticos","Medicina Integrativa","Fisioterapia","Quiropraxia e Acupuntura","Massoterapia e Spa","Saúde Mental e Mindfulness","Dermatologia"],
    "Educação & Capacitação":      ["Cursos Online / Infoprodutos","Idiomas","Concursos Públicos","Pós-graduação / MBA","Reforço Escolar","Cursos Profissionalizantes","Coaching e Mentoria","Programação e TI","Design e Criatividade","Música e Artes","Culinária e Gastronomia","Finanças Pessoais / Investimentos"],
    "Negócios & Empreendedorismo": ["Consultoria Empresarial","Marketing Digital para Empresas","Gestão e Liderança","Franquias","E-commerce e Dropshipping","Negócios Locais","Startups e Inovação","Contabilidade e Finanças Empresariais","Recursos Humanos","Logística e Supply Chain"],
    "Moda & Beleza":               ["Moda Feminina","Moda Masculina","Moda Plus Size","Moda Fitness","Cosméticos e Skincare","Cabelos (Salão / Produtos)","Nail Art / Unhas","Perfumaria","Joias e Acessórios","Moda Infantil","Moda Praia","Lingerie e Moda Íntima"],
    "Alimentação & Gastronomia":   ["Restaurante","Delivery / iFood","Confeitaria e Doces","Cafeteria","Alimentação Saudável","Marmitex / Quentinha","Bebidas Especiais","Food Truck","Pizzaria","Hamburgueria","Padaria e Açougue","Catering e Eventos"],
    "Casa & Decoração":            ["Decoração de Interiores","Reforma e Construção","Móveis Planejados","Objetos e Artesanato","Jardinagem e Paisagismo","Limpeza e Organização","Eletrodomésticos e Utilidades","Iluminação","Pisos e Revestimentos","Portas e Janelas"],
    "Tecnologia & Digital":        ["Aplicativos / SaaS","E-commerce / Loja Virtual","Desenvolvimento Web e Apps","Segurança Digital e VPN","Hardware e Gadgets","Games e Entretenimento Digital","Inteligência Artificial","Automação e Produtividade","Hospedagem e Domínios","Marketing Digital / Ferramentas"],
    "Imóveis":                     ["Construtora / Incorporadora","Imobiliária","Imóveis para Investimento","Aluguel por Temporada","Loteamentos e Terrenos","Imóveis Comerciais","Financiamento Imobiliário","Decoração e Reforma para Revenda"],
    "Automotivo":                  ["Concessionária / Revenda","Oficina e Mecânica","Acessórios Automotivos","Seguros de Veículo","Som e Elétrica Automotiva","Estética Automotiva","Locação de Veículos","Moto e Scooter"],
    "Turismo & Viagens":           ["Agência de Viagens","Pacotes Nacionais","Pacotes Internacionais","Turismo de Aventura","Cruzeiros","Turismo de Luxo","Turismo Religioso","Ecoturismo","Aluguel de Temporada","Passagens Aéreas"],
    "Serviços Profissionais":      ["Advocacia e Direito","Contabilidade","Arquitetura e Engenharia","Consultoria de RH","Segurança Privada","Seguros em Geral","Assessoria Financeira","Psicologia Organizacional","Tradução e Idiomas","Limpeza e Conservação"],
    "Pet & Animais":               ["Pet Shop","Veterinária e Clínica","Ração e Petiscos","Adestramento","Hotel e Day Care para Pets","Banho e Tosa","Produtos Naturais para Pets","Roupinhas e Acessórios","Seguros Pet"],
    "Infantil & Família":          ["Escola e Creche","Brinquedos e Jogos","Roupas Infantis","Festas e Eventos Infantis","Pediatria e Saúde Infantil","Cursos para Pais","Produtos para Bebê","Alimentação Infantil","Recreação e Lazer"],
    "Finanças & Investimentos":    ["Investimentos (Ações, FIIs, Cripto)","Educação Financeira","Crédito e Empréstimos","Seguros de Vida e Previdência","Planejamento Financeiro","Consórcio","Câmbio e Remessas","Cartões e Benefícios"],
    "Religião & Espiritualidade":  ["Igreja e Ministério","Retiros Espirituais","Produtos Religiosos","Terapias Holísticas","Astrologia e Tarot","Meditação e Mindfulness","Livros e Literatura Espiritual"],
    "Esportes & Lazer":            ["Academias e Esportes Coletivos","Esportes de Aventura e Outdoor","Ciclismo e Corrida","Natação e Aquáticos","Artes Marciais","Equipamentos Esportivos","Clube de Campo / Social","eSports e Games","Pesca e Caça"],
    "Arte & Entretenimento":       ["Fotografia e Vídeo","Música (Aulas, Shows, Equipamentos)","Cinema e Streaming","Teatro e Performance","Arte Visual e Pintura","Design Gráfico","Podcasts e Conteúdo Digital","Jogos de Tabuleiro"],
    "Agronegócio":                 ["Insumos e Defensivos","Máquinas e Implementos","Consultoria Agrícola","Pecuária e Veterinária Rural","Tecnologia para o Campo","Crédito Rural","Orgânicos e Sustentabilidade"],
}

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gerenciar Clientes · Dash Digital",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS — identidade visual Dash Digital ──────────────────────────────────────
st.markdown("""
<style>
/* ── Sidebar ────────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] { background:#0d2137 !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color:#fff !important; }

div[data-testid="stSidebarNav"] { display:none; }

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] select,
[data-testid="stSidebar"] textarea {
    background-color:#1a3a5c !important;
    color:#fff !important;
    border:1px solid rgba(255,255,255,0.25) !important;
    border-radius:8px !important;
}

/* Botão principal da sidebar */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg,#f8b940,#d99a20) !important;
    color:#003f7c !important;
    font-weight:700 !important;
    border:none !important;
    border-radius:10px !important;
    padding:12px !important;
    font-size:1rem !important;
    width:100% !important;
    margin-top:6px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg,#ffc94d,#e8aa30) !important;
    transform:translateY(-1px) !important;
}

/* ── Main ───────────────────────────────────────────────────────────────────── */
.main .block-container {
    padding-top:1.5rem;
    padding-bottom:3rem;
    max-width:1100px;
    background:#f0f3f8;
}

/* Header */
.cl-header {
    background: linear-gradient(135deg,#003f7c 0%,#1a5a9a 60%,#0d4080 100%);
    border-radius:16px;
    padding:26px 32px;
    color:#fff;
    margin-bottom:28px;
    position:relative;
    overflow:hidden;
}
.cl-header::after {
    content:'';
    position:absolute;
    inset:0;
    background:radial-gradient(ellipse at 85% 15%,rgba(255,255,255,0.10) 0%,transparent 60%);
    pointer-events:none;
}
.cl-header-title { font-size:1.45rem; font-weight:700; margin-bottom:4px; }
.cl-header-sub   { font-size:.88rem; opacity:.65; }

/* Stat pills */
.stat-bar { display:flex; gap:10px; margin-bottom:20px; flex-wrap:wrap; }
.stat-pill {
    background:#fff;
    border:1px solid #dde3ed;
    border-radius:20px;
    padding:5px 14px;
    font-size:.82rem;
    color:#003f7c;
    font-weight:600;
}

/* Cards de cliente */
.cl-card {
    background:#fff;
    border:1px solid #dde3ed;
    border-radius:14px;
    padding:18px 22px;
    margin-bottom:12px;
    box-shadow:0 2px 6px rgba(0,0,0,0.04);
}

/* Títulos de seção do formulário */
.form-section {
    font-size:.72rem;
    font-weight:700;
    letter-spacing:.08em;
    text-transform:uppercase;
    color:#003f7c;
    margin:22px 0 8px 0;
    padding-bottom:5px;
    border-bottom:2px solid #dde3ed;
}

/* Botões de ação (editar, ativar) na área principal */
.main .stButton > button {
    border-radius:8px !important;
    font-size:.85rem !important;
    padding:6px 12px !important;
}

/* Botão primário de salvar */
[data-testid="stForm"] button[kind="primaryFormSubmit"],
[data-testid="stForm"] button[data-testid="baseButton-primaryFormSubmit"] {
    background: linear-gradient(135deg,#003f7c,#1a5a9a) !important;
    color:#fff !important;
    font-weight:700 !important;
    border:none !important;
    border-radius:10px !important;
    padding:12px !important;
    font-size:1rem !important;
}

#MainMenu { visibility:hidden; }
footer    { visibility:hidden; }
</style>
""", unsafe_allow_html=True)


# ── Supabase helpers ──────────────────────────────────────────────────────────
def _get_creds() -> tuple[str, str]:
    try:
        url = st.secrets.get("supabase_url", "") or ""
        key = st.secrets.get("supabase_service_key", "") or ""
        return url, key
    except Exception:
        return "", ""

def _is_configured() -> bool:
    u, k = _get_creds()
    return bool(u and k)

def _headers() -> dict:
    _, key = _get_creds()
    return {
        "apikey":        key,
        "Authorization": f"Bearer {key}",
        "Content-Type":  "application/json",
        "Prefer":        "return=representation",
    }

def _rest(table: str) -> str:
    url, _ = _get_creds()
    return f"{url}/rest/v1/{table}"


# ── File helper ───────────────────────────────────────────────────────────────
def _extract_file(f) -> str:
    try:
        if f.name.lower().endswith(".pdf"):
            import pypdf
            reader = pypdf.PdfReader(f)
            return "\n".join(p.extract_text() or "" for p in reader.pages).strip()
        return f.read().decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return f"[Erro ao ler arquivo: {e}]"


# ── CRUD ──────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_clients() -> list[dict]:
    if not _is_configured():
        return []
    try:
        r = requests.get(
            _rest("clients"), headers=_headers(),
            params={"order": "name.asc", "select": "*"}, timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except Exception:
        return []

def save_client(data: dict) -> tuple[bool, str]:
    if not _is_configured():
        return False, "Supabase não configurado."
    try:
        r = requests.post(
            _rest("clients"),
            headers={**_headers(), "Prefer": "resolution=merge-duplicates,return=minimal"},
            json=data, timeout=10,
        )
        if r.status_code in (200, 201):
            return True, f"✅ Cliente '{data['name']}' salvo com sucesso!"
        return False, f"Erro {r.status_code}: {r.text}"
    except Exception as e:
        return False, f"Erro de conexão: {e}"

def toggle_active(key: str, active: bool) -> bool:
    try:
        r = requests.patch(
            _rest("clients"), headers=_headers(),
            params={"key": f"eq.{key}"},
            json={"active": active}, timeout=10,
        )
        return r.status_code in (200, 204)
    except Exception:
        return False


# ── Tom de voz — histórico de versões ─────────────────────────────────────────

def save_tov_version(client_key: str, client_name: str, content: str) -> bool:
    """Salva uma versão do tom de voz na tabela tone_of_voice_history."""
    if not _is_configured() or not content.strip():
        return False
    try:
        r = requests.post(
            _rest("tone_of_voice_history"),
            headers={**_headers(), "Prefer": "return=minimal"},
            json={"client_key": client_key, "client_name": client_name, "content": content.strip()},
            timeout=10,
        )
        return r.status_code in (200, 201)
    except Exception:
        return False


@st.cache_data(ttl=120)
def load_tov_history(client_key: str) -> list[dict]:
    """Carrega o histórico de versões do tom de voz de um cliente."""
    if not _is_configured():
        return []
    try:
        r = requests.get(
            _rest("tone_of_voice_history"),
            headers=_headers(),
            params={
                "client_key": f"eq.{client_key}",
                "order":      "created_at.desc",
                "limit":      "10",
                "select":     "id,content,created_at",
            },
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except Exception:
        return []


# ── Helpers visuais ───────────────────────────────────────────────────────────
def _rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    try:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"
    except Exception:
        return f"rgba(0,63,124,{alpha})"

_DEFAULT_COLORS = {
    "p": "#003f7c", "p2": "#1a5a9a", "a": "#f8b940", "ad": "#d99a20",
    "header_end": "#2471c8", "period_color": "#ffe08a", "stat_color": "#f8b940",
}

_COLOR_DEFS = [
    ("p",            "Cor primária",              "#003f7c"),
    ("p2",           "Cor primária secundária",    "#1a5a9a"),
    ("a",            "Cor de destaque",            "#f8b940"),
    ("ad",           "Destaque escuro",            "#d99a20"),
    ("header_end",   "Cor final do cabeçalho",     "#2471c8"),
    ("period_color", "Cor do badge de período",    "#ffe08a"),
    ("stat_color",   "Cor dos números (KPIs)",     "#f8b940"),
]

def _logo_b64() -> str:
    try:
        with open("assets/logo.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""


# ══════════════════════════════════════════════════════════════════════════════
# FORMULÁRIO DE CLIENTE
# ══════════════════════════════════════════════════════════════════════════════
def client_form(existing: dict = None, form_key: str = "new") -> dict | None:
    e = existing or {}
    colors = e.get("colors") or _DEFAULT_COLORS
    if isinstance(colors, str):
        colors = json.loads(colors)
    goals = e.get("goals") or {}
    if isinstance(goals, str):
        goals = json.loads(goals)

    with st.form(key=f"form_{form_key}"):

        # ── 1. Identificação ──────────────────────────────────────────────────
        st.markdown('<div class="form-section">👤 Identificação</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            name   = st.text_input("Nome do cliente *", value=e.get("name", ""),
                                    placeholder="Ex: Prof. Wanzeller")
            handle = st.text_input("Handle do Instagram *", value=e.get("handle", ""),
                                    placeholder="Ex: @prof.wanzeller")
        with c2:
            slug = st.text_input(
                "Identificador interno (slug) *", value=e.get("key", ""),
                placeholder="Ex: wanzeller",
                help="Texto curto sem espaços, em letras minúsculas. "
                     "Usado internamente para identificar o cliente no sistema.",
            )
            avatar = st.text_input("Emoji do cliente", value=e.get("avatar", "📊"),
                                    help="Um emoji representativo. Ex: 🎓 👩‍💼 📚 🏋️")

        nicho_atual = e.get("nicho", "")
        nicho_opts  = ["(Não definido)"] + NICHES
        nicho_idx   = nicho_opts.index(nicho_atual) if nicho_atual in nicho_opts else 0
        nicho = st.selectbox(
            "Nicho principal",
            options=nicho_opts,
            index=nicho_idx,
            help="Usado pelo Gerador de Copies para pré-selecionar o nicho automaticamente.",
        )

        sub_nicho_atual = e.get("sub_nicho", "")
        if nicho != "(Não definido)":
            sub_nicho_opts = ["(Não definido)"] + SUB_NICHES.get(nicho, [])
        else:
            # Nicho não definido — preserva sub_nicho existente para não apagar dados
            sub_nicho_opts = ["(Selecione o nicho primeiro)"]
            if sub_nicho_atual and sub_nicho_atual not in sub_nicho_opts:
                sub_nicho_opts = [sub_nicho_atual] + sub_nicho_opts
        sub_nicho_idx = sub_nicho_opts.index(sub_nicho_atual) if sub_nicho_atual in sub_nicho_opts else 0
        sub_nicho = st.selectbox(
            "Sub-nicho",
            options=sub_nicho_opts,
            index=sub_nicho_idx,
            help="Especialidade dentro do nicho. Pré-selecionado automaticamente no Gerador de Copies.",
        )

        # ── 2. IDs das Contas Meta ────────────────────────────────────────────
        st.markdown('<div class="form-section">📱 IDs das Contas Meta</div>', unsafe_allow_html=True)
        st.caption(
            "**Instagram Business ID:** Meta Business Suite → Configurações → "
            "Contas do Instagram → selecione a conta → ID da conta.  \n"
            "**Meta Ads Account ID:** Gerenciador de Anúncios → a URL contém "
            "'act_NÚMERO' — use só o número, sem o 'act_'."
        )
        cm1, cm2 = st.columns(2)
        with cm1:
            ig_id = st.text_input("ID da Conta Instagram Business *",
                                   value=e.get("instagram_id", ""),
                                   placeholder="Ex: 17841479657213211")
        with cm2:
            fb_id = st.text_input("ID da Conta Meta Ads *",
                                   value=e.get("facebook_account_id", ""),
                                   placeholder="Ex: 1429787371828065")

        # ── 3. Apresentação no Relatório ──────────────────────────────────────
        st.markdown('<div class="form-section">📄 Apresentação no Relatório</div>', unsafe_allow_html=True)
        bio = st.text_area(
            "Descrição do cliente",
            value=e.get("bio", ""), height=75,
            placeholder="Aparece no cabeçalho do relatório. "
                        "Ex: 'Professor de matemática para concursos públicos'",
            help="Preenchida manualmente — pode ser diferente da bio real do Instagram.",
        )
        hashtags = st.text_input(
            "Hashtags / Áreas de atuação",
            value=", ".join(e.get("tags") or []),
            placeholder="Ex: #Educação, #ConcursoPúblico, #TráfegoPago",
            help="Etiquetas que aparecem no cabeçalho do relatório. Separe por vírgula.",
        )
        footer = st.text_input(
            "Rodapé do relatório",
            value=e.get("footer", ""),
            placeholder="Deixe vazio para gerar automaticamente com o nome do cliente.",
        )

        # ── 4. Tom de Voz ─────────────────────────────────────────────────────
        st.markdown('<div class="form-section">🗣️ Tom de Voz (Gerador de Copies)</div>', unsafe_allow_html=True)
        st.caption("O upload de arquivo tem prioridade sobre o texto digitado abaixo.")
        tv1, tv2 = st.columns(2)
        with tv1:
            tov_file = st.file_uploader(
                "Upload do guia de tom de voz (TXT ou PDF)",
                type=["txt", "pdf"], key=f"tov_{form_key}",
            )
        with tv2:
            tov_text = st.text_area(
                "Ou descreva o tom de voz",
                value=e.get("tone_of_voice", ""), height=120,
                placeholder="Como o cliente fala? Que palavras usa? "
                            "O que evita? Qual é o tom? Exemplos de frases...",
            )
        competitors = st.text_input(
            "Páginas concorrentes no Facebook",
            value=e.get("competitors", ""),
            placeholder="Ex: Página Concorrente A, Página Concorrente B",
        )

        # ── 5. Cores do Relatório ─────────────────────────────────────────────
        st.markdown('<div class="form-section">🎨 Cores do Relatório</div>', unsafe_allow_html=True)
        st.caption("Cole o código hex de cada cor (formato #RRGGBB). O quadrado mostra a cor atual salva.")
        col_vals = {}
        for i in range(0, len(_COLOR_DEFS), 2):
            row = st.columns([5, 1, 5, 1])
            for j in range(2):
                if i + j < len(_COLOR_DEFS):
                    fk, lbl, dflt = _COLOR_DEFS[i + j]
                    current = colors.get(fk, dflt)
                    with row[j * 2]:
                        val = st.text_input(lbl, value=current,
                                            key=f"c_{fk}_{form_key}", max_chars=7)
                        col_vals[fk] = val
                    with row[j * 2 + 1]:
                        st.markdown(
                            f'<div style="margin-top:28px;width:34px;height:34px;'
                            f'border-radius:6px;background:{current};'
                            f'border:1px solid #dde3ed;"></div>',
                            unsafe_allow_html=True,
                        )

        # ── 6. Metas de Tráfego Pago ──────────────────────────────────────────
        st.markdown('<div class="form-section">🎯 Metas de Tráfego Pago</div>', unsafe_allow_html=True)
        st.caption("Defina os limites para cada métrica. Use 0 para não definir uma meta.")
        mg1, mg2, mg3 = st.columns(3)
        with mg1:
            st.markdown("**Aquisição de Seguidores**")
            g_seg = st.number_input("Custo máx. por seguidor (R$)",
                                     min_value=0.0, step=0.50, format="%.2f",
                                     value=float(goals.get("custo_por_seguidor") or 0))
            g_cpm = st.number_input("CPM máximo — por mil impressões (R$)",
                                     min_value=0.0, step=1.0, format="%.2f",
                                     value=float(goals.get("cpm_maximo") or 0))
        with mg2:
            st.markdown("**Vendas / Conversões**")
            g_venda = st.number_input("Custo máx. por venda (R$)",
                                       min_value=0.0, step=1.0, format="%.2f",
                                       value=float(goals.get("custo_por_venda") or 0))
            g_cpa = st.number_input("CPA máximo — custo por resultado (R$)",
                                     min_value=0.0, step=1.0, format="%.2f",
                                     value=float(goals.get("cpa_maximo") or 0))
            g_roas = st.number_input("ROAS mínimo (×)",
                                      min_value=0.0, step=0.5, format="%.1f",
                                      value=float(goals.get("roas_minimo") or 0))
        with mg3:
            st.markdown("**Engajamento / Cliques**")
            g_ctr = st.number_input("CTR mínimo (%)",
                                     min_value=0.0, step=0.1, format="%.2f",
                                     value=float(goals.get("ctr_minimo") or 0))
            g_cpc = st.number_input("CPC máximo — custo por clique (R$)",
                                     min_value=0.0, step=0.10, format="%.2f",
                                     value=float(goals.get("cpc_maximo") or 0))
            g_conv = st.number_input("Taxa de conversão mínima (%)",
                                      min_value=0.0, step=0.1, format="%.2f",
                                      value=float(goals.get("taxa_conversao_minima") or 0))

        # ── 7. Observações ────────────────────────────────────────────────────
        st.markdown('<div class="form-section">📝 Observações</div>', unsafe_allow_html=True)
        observations = st.text_area(
            "Observações sobre o cliente",
            value=e.get("observations", ""), height=90,
            placeholder="Informações importantes, particularidades, contexto, acordos, etc.",
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button(
            "💾 Salvar Cliente", use_container_width=True, type="primary",
        )

    if not submitted:
        return None

    # ── Validação ─────────────────────────────────────────────────────────────
    errs = []
    if not name.strip():   errs.append("Nome do cliente")
    if not handle.strip(): errs.append("Handle do Instagram")
    if not slug.strip():   errs.append("Identificador interno")
    if not ig_id.strip():  errs.append("ID da Conta Instagram")
    if not fb_id.strip():  errs.append("ID da Conta Meta Ads")
    if errs:
        st.error(f"Campos obrigatórios não preenchidos: **{', '.join(errs)}**")
        return None

    tov_final = tov_text.strip()
    if tov_file is not None:
        tov_final = _extract_file(tov_file)

    p_v = col_vals.get("p",  "#003f7c")
    a_v = col_vals.get("a",  "#f8b940")
    final_colors = {
        "p":            p_v,
        "p2":           col_vals.get("p2",  "#1a5a9a"),
        "a":            a_v,
        "ad":           col_vals.get("ad",  "#d99a20"),
        "al":           _rgba(a_v, 0.13),
        "pl":           _rgba(p_v, 0.08),
        "bg":           "#f0f3f8",
        "header_end":   col_vals.get("header_end",   "#2471c8"),
        "period_color": col_vals.get("period_color", "#ffe08a"),
        "stat_color":   col_vals.get("stat_color",   "#f8b940"),
    }

    def _g(v): return v if v and v > 0 else None
    final_goals = {k: v for k, v in {
        "custo_por_seguidor":    _g(g_seg),
        "custo_por_venda":       _g(g_venda),
        "cpa_maximo":            _g(g_cpa),
        "ctr_minimo":            _g(g_ctr),
        "cpm_maximo":            _g(g_cpm),
        "cpc_maximo":            _g(g_cpc),
        "roas_minimo":           _g(g_roas),
        "taxa_conversao_minima": _g(g_conv),
    }.items() if v is not None}

    return {
        "key":                 slug.strip().lower().replace(" ", "-"),
        "name":                name.strip(),
        "handle":              handle.strip(),
        "instagram_id":        ig_id.strip(),
        "facebook_account_id": fb_id.strip(),
        "bio":                 bio.strip(),
        "tags":                [t.strip() for t in hashtags.split(",") if t.strip()],
        "avatar":              avatar.strip() or "📊",
        "footer":              footer.strip() or
                               f"Relatório gerado para <strong>{name.strip()}</strong> por Dash Digital.",
        "colors":              final_colors,
        "tone_of_voice":       tov_final,
        "competitors":         competitors.strip(),
        "goals":               final_goals,
        "observations":        observations.strip(),
        "nicho":               nicho if nicho != "(Não definido)" else "",
        "sub_nicho":           sub_nicho if sub_nicho not in ("(Não definido)", "(Selecione o nicho primeiro)") else "",
        "active":              True,
    }


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    logo = _logo_b64()
    if logo:
        st.markdown(
            f'<div style="padding:12px 4px 8px;">'
            f'<img src="data:image/png;base64,{logo}" style="height:38px;"></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="padding:12px 0 4px;font-size:1.1rem;font-weight:700;">📊 Dash Digital</div>',
            unsafe_allow_html=True,
        )

    st.markdown("**Gerenciar Clientes**")
    st.markdown("---")

    if st.button("➕ Cadastrar novo cliente", use_container_width=True):
        st.session_state.cl_new     = True
        st.session_state.cl_editing = None
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small style='opacity:.5;font-size:.72rem;'>"
        "Clientes cadastrados aqui aparecem automaticamente no "
        "Gerador de Relatórios e no Gerador de Copies.</small>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cl-header">
  <div class="cl-header-title">👥 Gerenciar Clientes</div>
  <div class="cl-header-sub">
    Cadastre e edite os clientes da agência.
    Alterações aparecem automaticamente no Gerador de Relatórios e no Gerador de Copies.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Verificação Supabase ──────────────────────────────────────────────────────
if not _is_configured():
    st.error(
        "⚠️ **Supabase não configurado.** "
        "Adicione `supabase_url` e `supabase_service_key` nos Secrets do Streamlit Cloud."
    )
    st.stop()

# ── Session state ─────────────────────────────────────────────────────────────
for _k, _v in [("cl_editing", None), ("cl_new", False)]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── Estatísticas ──────────────────────────────────────────────────────────────
clients = load_clients()
total   = len(clients)
ativos  = sum(1 for c in clients if c.get("active", True))

st.markdown(
    f'<div class="stat-bar">'
    f'<div class="stat-pill">🏢 {total} cliente{"s" if total != 1 else ""} cadastrado{"s" if total != 1 else ""}</div>'
    f'<div class="stat-pill">✅ {ativos} ativo{"s" if ativos != 1 else ""}</div>'
    f'<div class="stat-pill">🔕 {total - ativos} inativo{"s" if (total-ativos) != 1 else ""}</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── Formulário novo cliente ───────────────────────────────────────────────────
if st.session_state.cl_new:
    with st.expander("➕ Cadastrar Novo Cliente", expanded=True):
        result = client_form(form_key="new")
        if result is not None:
            ok, msg = save_client(result)
            if ok:
                # Salva versão inicial do tom de voz se preenchido
                if result.get("tone_of_voice", "").strip():
                    save_tov_version(result["key"], result["name"], result["tone_of_voice"])
                st.success(msg)
                st.session_state.cl_new = False
                load_clients.clear()
                st.rerun()
            else:
                st.error(msg)
        if st.button("✕ Cancelar", key="cancel_new"):
            st.session_state.cl_new = False
            st.rerun()

# ── Lista de clientes ─────────────────────────────────────────────────────────
if not clients:
    st.info("Nenhum cliente cadastrado. Clique em **➕ Cadastrar novo cliente** na barra lateral.")
else:
    for cl in clients:
        active  = cl.get("active", True)
        clr     = cl.get("colors") or {}
        if isinstance(clr, str):
            clr = json.loads(clr)
        accent  = clr.get("a", "#f8b940")
        opacity = "1" if active else "0.45"

        ca, ci, cb = st.columns([1, 8, 2])
        with ca:
            st.markdown(
                f'<div style="font-size:2rem;width:52px;height:52px;border-radius:50%;'
                f'background:{accent}22;display:flex;align-items:center;'
                f'justify-content:center;opacity:{opacity};margin-top:4px;">'
                f'{cl.get("avatar","📊")}</div>',
                unsafe_allow_html=True,
            )
        with ci:
            status_badge = (
                "" if active else
                ' <span style="background:#fee2e2;color:#991b1b;font-size:.68rem;'
                'padding:2px 9px;border-radius:10px;font-weight:700;margin-left:6px;">INATIVO</span>'
            )
            badges = []
            if cl.get("goals"):                          badges.append("🎯 Metas")
            if cl.get("tone_of_voice", "").strip():      badges.append("🗣️ Tom de voz")
            if cl.get("observations", "").strip():       badges.append("📝 Obs.")
            badge_str = ("  ·  " + "  ·  ".join(badges)) if badges else ""

            st.markdown(
                f'<div style="opacity:{opacity};padding:4px 0;">'
                f'<strong style="font-size:1rem;color:#003f7c;">{cl["name"]}</strong>'
                f'{status_badge}<br>'
                f'<span style="font-size:.85rem;color:#6b7280;">{cl.get("handle","")}'
                f' · IG: <code style="font-size:.78rem;">{cl.get("instagram_id","")}</code></span>'
                + (f'<br><span style="font-size:.75rem;color:#9ca3af;">{badge_str}</span>' if badges else "")
                + '</div>',
                unsafe_allow_html=True,
            )
        with cb:
            b1, b2 = st.columns(2)
            with b1:
                if st.button("✏️", key=f"ed_{cl['key']}", help="Editar"):
                    st.session_state.cl_editing = cl["key"]
                    st.session_state.cl_new = False
            with b2:
                if active:
                    if st.button("🔕", key=f"da_{cl['key']}", help="Desativar"):
                        if toggle_active(cl["key"], False):
                            load_clients.clear(); st.rerun()
                else:
                    if st.button("✅", key=f"ac_{cl['key']}", help="Reativar"):
                        if toggle_active(cl["key"], True):
                            load_clients.clear(); st.rerun()

        if st.session_state.cl_editing == cl["key"]:
            with st.expander(f"✏️ Editando: {cl['name']}", expanded=True):
                result = client_form(existing=cl, form_key=f"edit_{cl['key']}")
                if result is not None:
                    # ── Detecta mudança no tom de voz e versiona ──────────────
                    old_tov = (cl.get("tone_of_voice") or "").strip()
                    new_tov = (result.get("tone_of_voice") or "").strip()
                    tov_changed = new_tov and new_tov != old_tov

                    ok, msg = save_client(result)
                    if ok:
                        if tov_changed:
                            save_tov_version(cl["key"], cl["name"], new_tov)
                            load_tov_history.clear()
                        st.success(msg)
                        st.session_state.cl_editing = None
                        load_clients.clear(); st.rerun()
                    else:
                        st.error(msg)
                if st.button("✕ Cancelar edição", key=f"ce_{cl['key']}"):
                    st.session_state.cl_editing = None; st.rerun()

        # ── Histórico do Tom de Voz ───────────────────────────────────────────
        tov_history = load_tov_history(cl["key"])
        if tov_history:
            with st.expander(f"📜 Histórico do Tom de Voz — {cl['name']} ({len(tov_history)} versão{'ões' if len(tov_history) > 1 else ''})", expanded=False):
                for i, entry in enumerate(tov_history):
                    created = entry.get("created_at", "")
                    # Formata data: "2025-05-18T14:30:00+00:00" → "18/05/2025 às 14:30"
                    try:
                        from datetime import datetime as _dt
                        dt = _dt.fromisoformat(created.replace("Z", "+00:00"))
                        date_label = dt.strftime("%d/%m/%Y às %H:%M")
                    except Exception:
                        date_label = created[:16] if created else "—"

                    version_label = "Versão atual" if i == 0 else f"Versão {len(tov_history) - i}"
                    badge_color   = "#d1fae5" if i == 0 else "#f3f4f6"
                    badge_text    = "#065f46" if i == 0 else "#374151"

                    st.markdown(
                        f'<div style="border:1px solid #e5e7eb;border-radius:10px;'
                        f'padding:12px 16px;margin-bottom:10px;background:#fafafa;">'
                        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">'
                        f'<span style="background:{badge_color};color:{badge_text};font-size:.72rem;'
                        f'font-weight:700;padding:2px 10px;border-radius:8px;">{version_label}</span>'
                        f'<span style="font-size:.72rem;color:#9ca3af;">{date_label}</span>'
                        f'</div>'
                        f'<div style="font-size:.82rem;color:#374151;white-space:pre-wrap;line-height:1.6;">'
                        f'{entry.get("content","")[:600]}'
                        f'{"…" if len(entry.get("content","")) > 600 else ""}'
                        f'</div></div>',
                        unsafe_allow_html=True,
                    )

        st.divider()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<p style="text-align:center;font-size:.72rem;color:#9ca3af;margin-top:20px;">'
    'Gerenciar Clientes · Dash Digital · @dashdgt · Dados sincronizados via Supabase</p>',
    unsafe_allow_html=True,
)
