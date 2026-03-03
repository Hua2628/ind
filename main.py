import pandas as pd
import yfinance as yf
import requests
from datetime import datetime
import io
import json
import time

# --- 1. 產業清單 (您可以自行增加或修改此清單) ---
MARKET_MAP = {
    ##重要指數
    "SPY": {"cat": "重要指數", "name": "標普500"},
    "DIA": {"cat": "重要指數", "name": "道瓊工業"},
    "QQQ": {"cat": "重要指數", "name": "那斯達克100"},
    "IWM": {"cat": "重要指數", "name": "羅素2000"},
    "MGK": {"cat": "重要指數", "name": "大型成長股"},
    "QQQE": {"cat": "重要指數", "name": "等權重QQQ"},
    "RSP": {"cat": "重要指數", "name": "等權重SPY"},
    "MDY": {"cat": "重要指數", "name": "標普中型400"},
    "TLT": {"cat": "重要指數", "name": "20年期美債"},
    "IBIT": {"cat": "重要指數", "name": "比特幣現貨"},
    "ETHA": {"cat": "重要指數", "name": "乙太幣現貨"},
    "ARKK": {"cat": "重要指數", "name": "ARK創新"},
    "FFTY": {"cat": "重要指數", "name": "IBD 50 指數"},   


    ##等權重
    "RSPT": {"cat": "等權重", "name": "等權重科技"},
    "RSPC": {"cat": "等權重", "name": "等權重通訊服務"},
    "RSPN": {"cat": "等權重", "name": "等權重工業"},
    "RSPF": {"cat": "等權重", "name": "等權重金融"},
    "RSPD": {"cat": "等權重", "name": "等權重非必選消費"},
    "RSPU": {"cat": "等權重", "name": "等權重公共事業"},
    "RSPR": {"cat": "等權重", "name": "等權重房地產"},
    "RSPH": {"cat": "等權重", "name": "等權重醫療保健"},
    "RSPM": {"cat": "等權重", "name": "等權重原物料"},
    "RSPS": {"cat": "等權重", "name": "等權重必需消費"},
    "RSPG": {"cat": "等權重", "name": "等權重能源"},

    ##11大類股
    "XLK": {"cat": "11大類股", "name": "科技類股"},
    "XLC": {"cat": "11大類股", "name": "通訊服務"},
    "XLP": {"cat": "11大類股", "name": "必需消費"},
    "XLY": {"cat": "11大類股", "name": "非必選消費"},
    "XLV": {"cat": "11大類股", "name": "醫療保健"},
    "XLF": {"cat": "11大類股", "name": "金融類股"},
    "XLB": {"cat": "11大類股", "name": "原物料"},
    "XLI": {"cat": "11大類股", "name": "工業類股"},
    "XLE": {"cat": "11大類股", "name": "能源類股"},
    "XLU": {"cat": "11大類股", "name": "公共事業"},
    "XLRE": {"cat": "11大類股", "name": "房地產"},

    ##標普大中小型股

    "IJR": {"cat": "標普大中小型股", "name": "標普小型600"},
    "IJS": {"cat": "標普大中小型股", "name": "標普小型600價值"},
    "IJT": {"cat": "標普大中小型股", "name": "標普小型600成長"},
    "IJH": {"cat": "標普大中小型股", "name": "標普中型400"},
    "IJJ": {"cat": "標普大中小型股", "name": "標普中型400價值"},
    "IJK": {"cat": "標普大中小型股", "name": "標普中型400成長"},
    "IVE": {"cat": "標普大中小型股", "name": "標普500價值"},
    "IWW": {"cat": "標普大中小型股", "name": "羅素3000"},
    "IVW": {"cat": "標普大中小型股", "name": "標普500成長"},
    "IWO": {"cat": "標普大中小型股", "name": "羅素2000成長"},

    ##細分產業

    "IGV": {"cat": "細分產業", "name": "科技軟體"},
    "WCLD": {"cat": "細分產業", "name": "雲端運算"},
    "FDN": {"cat": "細分產業", "name": "網路指數"},
    "AIQ": {"cat": "細分產業", "name": "AI與大數據"},
    "ROBO": {"cat": "細分產業", "name": "機器人與自動化"},
    "CIBR": {"cat": "細分產業", "name": "網路安全"},
    "SOCL": {"cat": "細分產業", "name": "社群媒體"},
    "SMH": {"cat": "細分產業", "name": "半導體"},
    "KBE": {"cat": "細分產業", "name": "銀行股"},
    "KRE": {"cat": "細分產業", "name": "區域銀行"},
    "KCE": {"cat": "細分產業", "name": "資本市場"},
    "ARKF": {"cat": "細分產業", "name": "ARK金融科技"},
    "IBB": {"cat": "細分產業", "name": "那斯達克生技"},
    "IHI": {"cat": "細分產業", "name": "醫療器械"},
    "TAN": {"cat": "細分產業", "name": "太陽能"},
    "UNG": {"cat": "細分產業", "name": "天然氣"},
    "JETS": {"cat": "細分產業", "name": "全球航空"},
    "BOAT": {"cat": "細分產業", "name": "航運"},
    "DRIV": {"cat": "細分產業", "name": "自動駕駛與電動車"},
    "PAVE": {"cat": "細分產業", "name": "基礎建設"},
    "ITA": {"cat": "細分產業", "name": "航太與國防"},
    "IBUY": {"cat": "細分產業", "name": "網路零售"},
    "XRT": {"cat": "細分產業", "name": "零售"},
    "PEJ": {"cat": "細分產業", "name": "休閒娛樂"},
    "IYZ": {"cat": "細分產業", "name": "電信服務"},
    "UTES": {"cat": "細分產業", "name": "公共事業"},
    "IBIT": {"cat": "細分產業", "name": "比特幣現貨"},
    "BLOK": {"cat": "細分產業", "name": "區塊鏈"},
    "MSOS": {"cat": "細分產業", "name": "大麻"},
    "KWEB": {"cat": "細分產業", "name": "中概互聯網"},
    "SOXX": {"cat": "細分產業", "name": "半導體"},
    "PSI": {"cat": "細分產業", "name": "半導體"},
    "VGT": {"cat": "細分產業", "name": "資訊科技"},
    "PS": {"cat": "細分產業", "name": "軟體"},
    "CLOU": {"cat": "細分產業", "name": "雲端運算"},
    "SKYY": {"cat": "細分產業", "name": "雲端運算"},
    "HACK": {"cat": "細分產業", "name": "網路安全"},
    "ONLN": {"cat": "細分產業", "name": "網路零售"},
    "BBH": {"cat": "細分產業", "name": "生物技術"},
    "IEO": {"cat": "細分產業", "name": "油氣探勘與生產"},
    "OIL": {"cat": "細分產業", "name": "原油"},
    "SLX": {"cat": "細分產業", "name": "鋼鐵業"},
    "COPX": {"cat": "細分產業", "name": "銅礦開採"},
    "GNR": {"cat": "細分產業", "name": "全球天然資源"},
    "GUNR": {"cat": "細分產業", "name": "天然資源"},
    "XAR": {"cat": "細分產業", "name": "航太與國防"},
    "IYT": {"cat": "細分產業", "name": "運輸指數"},
    "ITB": {"cat": "細分產業", "name": "營建股"},
    "RTH": {"cat": "細分產業", "name": "零售"},
    "FIVG": {"cat": "細分產業", "name": "5G網路"},
    "XTL": {"cat": "細分產業", "name": "電信"},
    "UFO": {"cat": "細分產業", "name": "太空產業"},
    "BOTZ": {"cat": "細分產業", "name": "機器人與人工智慧"},
    "VEGI": {"cat": "細分產業", "name": "農業"},
    "XME": {"cat": "細分產業", "name": "金屬與採礦"},
    "GLD": {"cat": "細分產業", "name": "黃金"},
    "GDX": {"cat": "細分產業", "name": "黃金礦業"},
    "SILJ": {"cat": "細分產業", "name": "銀礦小盤股"},
    "SLV": {"cat": "細分產業", "name": "白銀"},
    "CPER": {"cat": "細分產業", "name": "銅"},
    "XOP": {"cat": "細分產業", "name": "油氣探勘與生產"},
    "USO": {"cat": "細分產業", "name": "原油"},
    "FCG": {"cat": "細分產業", "name": "天然氣開採"},
    "XES": {"cat": "細分產業", "name": "能源設備與服務"},
    "OIH": {"cat": "細分產業", "name": "石油服務"},
    "ICLN": {"cat": "細分產業", "name": "乾淨能源"},
    "LIT": {"cat": "細分產業", "name": "鋰電池與電池科技"},
    "DBA": {"cat": "細分產業", "name": "農業商品"},
    "DBC": {"cat": "細分產業", "name": "綜合商品指數"},
    "VNQ": {"cat": "細分產業", "name": "房地產REITs"},
    "SCHH": {"cat": "細分產業", "name": "房地產REITs"},
    "REZ": {"cat": "細分產業", "name": "特定房地產"},
    "XBI": {"cat": "細分產業", "name": "生技 (等權重)"},
    "ARKG": {"cat": "細分產業", "name": "ARK基因革命"},
    "PPH": {"cat": "細分產業", "name": "製藥"},
    "XHE": {"cat": "細分產業", "name": "醫療設備"},
    "KIE": {"cat": "細分產業", "name": "保險"},
    "IPAY": {"cat": "細分產業", "name": "移動支付"},
    "XTN": {"cat": "細分產業", "name": "運輸"},
    "EATZ": {"cat": "細分產業", "name": "餐飲服務"},
    "XHB": {"cat": "細分產業", "name": "營建"},
    "PBJ": {"cat": "細分產業", "name": "食品與飲料"},
    "GXC": {"cat": "細分產業", "name": "標普中國"},
    "FXI": {"cat": "細分產業", "name": "中國大盤"},
    "FNGS": {"cat": "細分產業", "name": "FANG+ 指數"},
    "URA": {"cat": "細分產業", "name": "鈾礦"},
    "WGMI": {"cat": "細分產業", "name": "比特幣採礦"},
    "REMX": {"cat": "細分產業", "name": "稀土/戰略金屬"}
}

# --- 2. 工具函式 ---
def fix_ticker_suffix(symbol):
    s = str(symbol).strip().upper()
    if ":" not in s: return s
    market, ticker = s.split(":")
    market_suffix_map = {"TSX": ".TO", "HKG": ".HK", "TYO": ".T", "ASX": ".AX"}
    suffix = market_suffix_map.get(market, "")
    return f"{ticker}{suffix}"

def get_realtime_holdings(etf_symbol):
    url = f"https://stockanalysis.com/etf/{etf_symbol.lower()}/holdings/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        df_h = pd.read_html(io.StringIO(response.text))[0]
        sym_col = [c for c in df_h.columns if 'Symbol' in str(c)][0]
        df_h['Yahoo_Symbol'] = df_h[sym_col].astype(str).apply(fix_ticker_suffix)
        df_h = df_h[~df_h['Yahoo_Symbol'].str.contains("CASH|USD|GBP|JPY")].head(15)
        weight_col = [c for c in df_h.columns if '%' in str(c) or 'Weight' in str(c)][0]
        if df_h[weight_col].dtype == 'O':
            df_h['Weight'] = df_h[weight_col].str.replace('%', '').str.replace(',', '').astype(float) / 100
        else:
            df_h['Weight'] = df_h[weight_col] / (100 if df_h[weight_col].max() > 1 else 1)
        return df_h[['Yahoo_Symbol', 'Weight']]
    except: return pd.DataFrame()

def fetch_multi_period_perf(symbols):
    valid_symbols = list(set([str(s) for s in symbols if s and "CASH" not in str(s)]))
    if not valid_symbols: return pd.DataFrame()
    data = yf.download(valid_symbols, period="2y", interval="1d", group_by='ticker', progress=False)
    results = []
    # 確保抓取所有週期
    periods = {"昨日": 1, "5日": 5, "20日": 20, "60日": 60, "120日": 120, "250日": 250}
    for s in valid_symbols:
        try:
            df = data[s] if len(valid_symbols) > 1 else data
            df = df.dropna(subset=['Close'])
            if len(df) < 251: continue
            curr = df['Close'].iloc[-1]
            row = {"代號": s} 
            for label, days in periods.items():
                past_price = df['Close'].iloc[-(days + 1)]
                row[label] = float((curr - past_price) / past_price)
            results.append(row)
        except: continue
    return pd.DataFrame(results)

# --- 3. 執行分析與輸出 ---
def main():
    print("🚀 啟動分析中，請稍候...")
    df_market_perf = fetch_multi_period_perf(list(MARKET_MAP.keys()))
    
    all_h_list = []
    for etf in MARKET_MAP.keys():
        print(f"📦 正在獲取 {etf} 的成分股數據...")
        h = get_realtime_holdings(etf)
        if not h.empty:
            h['ETF來源'] = etf
            all_h_list.append(h)
        time.sleep(0.5)

    df_final_h = pd.DataFrame()
    if all_h_list:
        df_all_h = pd.concat(all_h_list).reset_index(drop=True)
        unique_holdings = df_all_h['Yahoo_Symbol'].unique().tolist()
        print(f"📈 正在計算 {len(unique_holdings)} 檔成分股的動能指標...")
        df_h_perf = fetch_multi_period_perf(unique_holdings)
        df_final_h = pd.merge(df_all_h, df_h_perf, left_on='Yahoo_Symbol', right_on='代號', how='left').drop(columns=['代號'])

    # 依照分類整合 JSON (維持您的原始分類邏輯)
    final_output_data = []
    category_order = ["重要指數", "等權重", "11大類股", "標普大中小型股", "細分產業"]
    
    for cat in category_order:
        cat_tickers = [k for k, v in MARKET_MAP.items() if v['cat'] == cat]
        if not cat_tickers: continue
        
        cat_market_df = df_market_perf[df_market_perf['代號'].isin(cat_tickers)].copy()
        cat_market_df['名稱'] = cat_market_df['代號'].apply(lambda x: MARKET_MAP[x]['name'])
        
        cat_holdings = {}
        for ticker in cat_tickers:
            h_data = df_final_h[df_final_h['ETF來源'] == ticker].to_dict(orient='records')
            cat_holdings[ticker] = h_data

        final_output_data.append({
            "category": cat,
            "market": cat_market_df.to_dict(orient='records'),
            "holdings": cat_holdings
        })

    # --- 4. 生成 index.html (包含您的原始樣式與修正後的 TV 參數) ---
    print("📄 正在產生 index.html...")
    json_data = json.dumps(final_output_data, ensure_ascii=False)
    
    full_html = f"""<!doctype html>
<html lang="zh-TW">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ETF 強勢產業監控面板 (內建資料版)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <style>
      body {{ background-color: #ffffff; font-family: "PingFang TC", "Microsoft JhengHei", sans-serif; overflow: hidden; color: #333; font-size: 16px; }}
      .main-wrapper {{ display: flex; height: 100vh; width: 100vw; }}
      .sidebar {{ width: 35%; min-width: 420px; max-width: 50%; height: 100%; overflow-y: auto; border-right: 1px solid #e0e3eb; background: #fff; resize: horizontal; }}
      .content-area {{ flex-grow: 1; display: flex; flex-direction: column; height: 100%; background-color: #f8f9fa; overflow: hidden; }}
      .fixed-chart-section {{ flex-shrink: 0; padding: 12px; background: #f8f9fa; z-index: 100; }}
      .scrollable-list-section {{ flex-grow: 1; overflow-y: auto; padding: 0 15px 30px 15px; }}
      th.sortable {{ cursor: pointer; user-select: none; white-space: nowrap; font-size: 0.9rem; color: #444; padding: 10px 5px !important; }}
      th.sortable:hover {{ background-color: #f0f3fa; }}
      .stats-overlay {{ background: #ffffff; color: #131722; padding: 15px 20px; border-radius: 8px 8px 0 0; display: flex; flex-wrap: wrap; gap: 20px; border: 1px solid #e0e3eb; border-bottom: none; }}
      .stat-item {{ text-align: center; min-width: 65px; }}
      .stat-label {{ font-size: 12px; color: #707a8a; display: block; margin-bottom: 2px; }}
      .stat-value {{ font-size: 16px; font-weight: 800; }}
      .chart-container {{ min-height: 400px; height: 500px; background: #fff; border: 1px solid #e0e3eb; border-radius: 0 0 8px 8px; overflow: hidden; resize: vertical; }}
      .positive {{ color: #089981 !important; }}
      .negative {{ color: #f23645 !important; }}
      .active-row {{ background-color: #f0f7ff !important; border-left: 5px solid #2962ff; }}
      .category-header {{ background-color: #f1f3f9; padding: 8px 15px; font-weight: 800; font-size: 0.9rem; color: #495057; border-top: 1px solid #e0e3eb; }}
      .badge {{ font-size: 0.9rem; padding: 6px 12px; }}
      a {{ text-decoration: none; color: #2962ff; font-weight: bold; }}
    </style>
  </head>
  <body>
    <div id="app" class="main-wrapper">
      <div class="sidebar">
        <div class="p-3 bg-white sticky-top border-bottom">
          <h5 class="m-0" style="font-weight: 800;">🔥 產業排行</h5>
        </div>
        <div v-for="catData in allCategories" :key="catData.category">
          <div class="category-header">{{{{ catData.category }}}}</div>
          <table class="table table-hover table-sm text-center mb-0">
            <thead class="table-light">
              <tr>
                <th @click="sortMarket('代號')" class="sortable text-start ps-3">代號</th>
                <th @click="sortMarket('昨日')" class="sortable">昨日</th>
                <th @click="sortMarket('5日')" class="sortable">5D</th> <th @click="sortMarket('20日')" class="sortable">20D</th>
                <th @click="sortMarket('60日')" class="sortable">60D</th>
                <th @click="sortMarket('120日')" class="sortable">120D</th> <th @click="sortMarket('250日')" class="sortable">250D</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in getSortedMarketByCat(catData.market)" @click="selectETF(item)" :class="{{'active-row': selectedETF.代號 === item.代號}}" style="cursor: pointer">
                <td class="text-start ps-3">
                  <strong style="font-size: 1.05rem">{{{{item.代號}}}}</strong><br />
                  <small class="text-muted">{{{{item.名稱}}}}</small>
                </td>
                <td :class="perfClass(item['昨日'])">{{{{formatPct(item['昨日'])}}}}</td>
                <td :class="perfClass(item['5日'])">{{{{formatPct(item['5日'])}}}}</td>
                <td :class="perfClass(item['20日'])">{{{{formatPct(item['20日'])}}}}</td>
                <td :class="perfClass(item['60日'])">{{{{formatPct(item['60日'])}}}}</td>
                <td :class="perfClass(item['120日'])">{{{{formatPct(item['120日'])}}}}</td>
                <td :class="perfClass(item['250日'])">{{{{formatPct(item['250日'])}}}}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="content-area">
        <div class="fixed-chart-section">
          <div class="stats-overlay shadow-sm">
            <div class="stat-item" v-for="p in periods" :key="p.key">
              <span class="stat-label">{{{{p.label}}}}</span>
              <span class="stat-value" :class="perfClass(currentDisplay[p.key])">{{{{formatPct(currentDisplay[p.key])}}}}</span>
            </div>
            <div style="margin-left: auto; align-self: center;">
              <span class="badge bg-light text-dark border" style="font-weight: 700">
                {{{{currentDisplay.Name || currentDisplay.名稱 || currentDisplay.Yahoo_Symbol}}}}
              </span>
              <span class="badge bg-primary text-white ms-2">SPY 疊加</span>
            </div>
          </div>
          <div id="tv_chart" class="chart-container shadow-sm"></div>
        </div>

        <div class="scrollable-list-section">
          <div class="card shadow-sm border-0">
            <div class="card-header bg-white py-3">
              <strong style="font-size: 1.1rem">🔍 {{{{selectedETF.代號}}}} 成分股內容</strong>
            </div>
            <div class="card-body p-0">
              <table class="table table-sm table-hover mb-0 text-center">
                <thead class="table-light sticky-top">
                  <tr>
                    <th @click="sortHoldings('Yahoo_Symbol')" class="sortable ps-3 text-start">代號</th>
                    <th @click="sortHoldings('Weight')" class="sortable">權重</th>
                    <th v-for="p in periods" :key="p.key" @click="sortHoldings(p.key)" class="sortable">{{{{p.label}}}}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="h in sortedHoldings">
                    <td class="ps-3 text-start"><a href="javascript:void(0)" @click="selectStock(h)">{{{{h.Yahoo_Symbol}}}}</a></td>
                    <td class="text-secondary fw-bold">{{{{(h.Weight * 100).toFixed(1)}}}}%</td>
                    <td v-for="p in periods" :class="perfClass(h[p.key])">{{{{formatPct(h[p.key])}}}}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
      const DATA_ALL = {json_data};
      const {{ createApp, ref, onMounted, computed }} = Vue;
      createApp({{
        setup() {{
          const allCategories = ref(DATA_ALL);
          const allHoldings = ref({{}});
          const selectedETF = ref({{ 代號: "" }});
          const currentDisplay = ref({{}});
          const marketSortKey = ref("20日");
          const marketSortOrder = ref(-1);
          const holdingsSortKey = ref("Weight");
          const holdingsSortOrder = ref(-1);
          const periods = [
            {{ label: "昨日", key: "昨日" }}, {{ label: "5日", key: "5日" }},
            {{ label: "20日", key: "20日" }}, {{ label: "60日", key: "60日" }},
            {{ label: "120日", key: "120日" }}, {{ label: "250日", key: "250日" }}
          ];

          const loadData = () => {{
            const combinedHoldings = {{}};
            allCategories.value.forEach(src => {{ Object.assign(combinedHoldings, src.holdings); }});
            allHoldings.value = combinedHoldings;
            if (allCategories.value.length > 0) selectETF(allCategories.value[0].market[0]);
          }};

          const selectETF = (item) => {{ selectedETF.value = item; currentDisplay.value = item; updateChart(item.代號); }};
          const selectStock = (stock) => {{ currentDisplay.value = stock; updateChart(stock.Yahoo_Symbol); }};

          const updateChart = (symbol) => {{
            const container = document.getElementById("tv_chart");
            if (container) container.innerHTML = "";
            let tvSymbol = symbol.includes(".HK") ? "HKG:" + symbol.replace(".HK", "") : symbol.split(".")[0];
            
            new TradingView.widget({{
              "autosize": true,
              "symbol": tvSymbol,
              "interval": "D",
              "timezone": "Asia/Taipei",
              "theme": "light",
              "style": "9", // 設定為空心 K 線
              "locale": "zh_TW",
              "container_id": "tv_chart",
              "hide_side_toolbar": false,     // 顯示左側繪圖工具列
              "allow_symbol_change": true,    // 允許手動變更代號
              "save_image": true,             // 允許儲存圖表截圖
              "withdateranges": true,         // 顯示底部時間範圍選擇器
              "studies": [ {{ "id": "Overlay@tv-basicstudies", "inputs": {{ "symbol": "SPY", "title": "S&P 500" }}, "forceOverlay": true }} ],
              "studies_overrides": {{ "overlay.style": 9 }}, // 副圖/疊加也設定為空心
              "overrides": {{
                "mainSeriesProperties.style": 9,
                "mainSeriesProperties.hollowCandleStyle.upColor": "#089981",
                "mainSeriesProperties.hollowCandleStyle.downColor": "#f23645",
                "mainSeriesProperties.hollowCandleStyle.drawWick": true
              }}
            }});
          }};

          const sortMarket = (key) => {{ if (marketSortKey.value === key) marketSortOrder.value *= -1; else {{ marketSortKey.value = key; marketSortOrder.value = -1; }} }};
          const sortHoldings = (key) => {{ if (holdingsSortKey.value === key) holdingsSortOrder.value *= -1; else {{ holdingsSortKey.value = key; holdingsSortOrder.value = -1; }} }};
          const getSortedMarketByCat = (mList) => {{ return [...mList].sort((a, b) => (a[marketSortKey.value] > b[marketSortKey.value] ? 1 : -1) * marketSortOrder.value); }};
          const sortedHoldings = computed(() => {{ 
            let list = allHoldings.value[selectedETF.value.代號] || [];
            return [...list].sort((a, b) => (a[holdingsSortKey.value] > b[holdingsSortKey.value] ? 1 : -1) * holdingsSortOrder.value);
          }});

          const formatPct = (val) => (val === null || val === undefined || val === "-") ? "-" : (val * 100).toFixed(1) + "%";
          const perfClass = (val) => val > 0 ? "positive" : (val < 0 ? "negative" : "");

          onMounted(loadData);
          return {{ allCategories, getSortedMarketByCat, sortedHoldings, selectedETF, selectStock, selectETF, currentDisplay, perfClass, formatPct, periods, sortMarket, sortHoldings }};
        }}
      }}).mount("#app");
    </script>
  </body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"✨ 完成！請開啟 index.html 查看結果。5D 與 120D 欄位已補齊，且圖表已設定為空心 K 線。")

if __name__ == "__main__":

    main()
