# 🚀 INÍCIO RÁPIDO — Super-Dashboard CE

## ⚡ 30 segundos para funcionar

### 1. Abra o terminal no diretório do projeto

```powershell
cd "d:\PERIODO 7\DASHBOARD CE"
```

### 2. Ative o ambiente virtual

```powershell
venv\Scripts\activate
```

**Esperado**: Você verá `(venv)` no prompt

### 3. Execute o Super-Dashboard

```powershell
streamlit run app/Super_Dashboard_Streamlit.py
```

**Esperado**: Seu navegador abre automaticamente em `http://localhost:8501/`

---

## 📊 Primeira Execução

Quando abrir, você verá:

1. **Título**: "📊 Super-Dashboard CE — Visão 360° de Produtos"
2. **Sidebar esquerda**: Filtros e carregamento de dados
3. **KPIs**: 6 cartões com indicadores principais (Receita, Estoque, Gasto, etc.)
4. **Seletor de Produto**: Escolha um produto para análise 360°
5. **Painel 360°**: Estoque vs Vendas vs Compras do produto
6. **Abas de Análise**: 4 abas com visualizações consolidadas
7. **Recomendações**: 3 sugestões estratégicas automáticas

---

## 🧪 Teste Rápido (Dados de Exemplo)

### Pré-preenchido:

- ✅ "Usar dados de exemplo" marcado
- ✅ Produtos: Produto_001 a Produto_005 pré-selecionados
- ✅ Categorias: Todas
- ✅ Lojas: Todas
- ✅ Período: 365 dias anteriores

### Clique em:

1. **🔍 Filtros → Mostrar tabela completa** → Veja consolidação
2. **Abas → Produtos Críticos** → Veja riscos de ruptura
3. **Abas → Série Temporal** → Veja receita vs gasto mensal
4. **Abas → Comparativo Fornecedores** → Veja eficiência
5. **Abas → Heatmap** → Veja padrões

---

## 🎯 Teste de Funcionalidade

### ✅ Filtro de Produto
- Desselecione "Produto_001"
- Observe: KPIs atualizam, alertas mudam, gráficos se ajustam

### ✅ Filtro de Período
- Mude a data final para há 30 dias
- Observe: Vendas e Compras reduzem, série temporal muda

### ✅ Download de Dados
- Abra aba "🔴 Produtos Críticos"
- Clique "📥 Baixar Lista de Críticos (CSV)"
- Arquivo `produtos_criticos.csv` é salvo

### ✅ Seletor de Produto (360°)
- Escolha "Produto_001"
- Veja: Estoque atual vs Mínimo, Vendas acumuladas, Compras recebidas

---

## 🛠️ Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'streamlit'"
**Solução**: Certifique-se de ativar o ambiente virtual
```powershell
venv\Scripts\activate
```

### Erro: "Port 8501 already in use"
**Solução**: Outra instância do Streamlit já está rodando. Feche-a ou use porta diferente:
```powershell
streamlit run app/Super_Dashboard_Streamlit.py --server.port 8502
```

### Dashboard carrega branco
**Solução**: Atualize o navegador com `Ctrl+Shift+R` (cache do Streamlit)

### Dados não atualizam com filtros
**Solução**: Verifique se "Usar dados de exemplo" está marcado no sidebar

---

## 📁 Arquivos do Projeto

```
app/
├── Super_Dashboard_Streamlit.py     ⭐ MAIN — Super-Dashboard consolidado
├── Dashboard_Vendas_Streamlit.py    📊 Análise individual de vendas
├── Dashboard_Estoque_Streamlit.py   📦 Análise individual de estoque
└── Dashboard_Compras_Streamlit.py   💳 Análise individual de compras

docs/
└── manual_execucao.md               📖 Manual com 7 seções

README.md                             📄 Documentação completa
requirements.txt                      📋 Dependências
PROJETO_FINALIZADO.md                 ✅ Status e funcionalidades
INICIO_RAPIDO.md                      🚀 Este arquivo
```

---

## 💡 Dicas

- **Sempre use dados de exemplo primeiro** para entender a interface
- **Explore cada aba** para ver diferentes perspectivas dos dados
- **Experimente os filtros** para ver atualização em tempo real
- **Leia os alertas** — eles indicam riscos reais nos dados
- **Revise o manual_execucao.md** para aprender casos de uso

---

## 🎓 Para Professores/Avaliadores

O Super-Dashboard demonstra:

✅ **Consolidação de Dados**: Merge de 3 fontes (Estoque, Vendas, Compras)  
✅ **Cálculos Complexos**: Margens, riscos, flags booleanas  
✅ **Filtros Dinâmicos**: Multiselect, date picker com propagação  
✅ **Visualizações Interativas**: Plotly scatter, line, heatmap  
✅ **UX/UI**: Alertas visuais, KPIs, recomendações automáticas  
✅ **Exportação**: Download CSV em tempo real  
✅ **Boas Práticas**: Cache, validação, tratamento de erros  

---

**Pronto para começar? Execute agora!** 🚀

```powershell
venv\Scripts\activate && streamlit run app/Super_Dashboard_Streamlit.py
```
