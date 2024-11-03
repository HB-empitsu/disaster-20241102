import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import streamlit as st

@st.cache_data()
def load_data():
    df_dam = pd.read_csv("20241102_dam.csv")
    df_dam["日時"] = pd.to_datetime(df_dam["日時"], errors="coerce")
    df_dam.drop("貯水率治水容量", axis=1, inplace=True)

    df_river = pd.read_csv("20241102_river.csv")
    df_river["日時"] = pd.to_datetime(df_river["日時"], errors="coerce")
    df_river.drop("国分橋", axis=1, inplace=True)

    return df_dam, df_river

st.set_page_config(page_title="2024年11月2日　大雨災害", page_icon=None, initial_sidebar_state="auto", menu_items=None)
st.title("2024年11月2日　大雨災害")

df_dam, df_river = load_data()

tab1, tab2, tab3 = st.tabs(["グラフ", "玉川ダム", "蒼社川"])

tab1.subheader("グラフ")

# グラフの作成
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(
        x=df_river["日時"],
        y=df_river["中通"],
        name="中通",
        line=dict(color="blue"),
    ),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(
        x=df_river["日時"],
        y=df_river["高野"],
        name="高野",
        line=dict(color="red"),
    ),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(
        x=df_river["日時"],
        y=df_river["片山"],
        name="片山",
        line=dict(color="green"),
    ),
    secondary_y=False,
)

# 流入量
fig.add_trace(
    go.Scatter(
        x=df_dam["日時"],
        y=df_dam["全流入量"],
        name="全流入量",
        line=dict(color="orange"),
    ),
    secondary_y=True,
)

# 放流量
fig.add_trace(
    go.Scatter(
        x=df_dam["日時"],
        y=df_dam["全放流量"],
        name="全放流量",
        line=dict(color="purple"),
    ),
    secondary_y=True,
)

# レイアウトの設定
fig.update_layout(
    hovermode="x unified",
    height=800,
    hoverlabel=dict(namelength=-1),
    xaxis=dict(tickformat="%H:%M\n%Y-%m-%d", hoverformat="%Y-%m-%d %H:%M"),
)

# グラフの表示
tab1.plotly_chart(fig, use_container_width=True)


tab2.subheader("玉川ダム")


fig_dam = make_subplots(rows=2, cols=1)

# 貯水量
fig_dam.add_trace(
    go.Scatter(
        x=df_dam["日時"],
        y=df_dam["貯水量"],
        name="貯水量",
        line=dict(color="blue"),
    ),
    row=1,
    col=1,
)

# 流入量と放流量
fig_dam.add_trace(
    go.Scatter(
        x=df_dam["日時"],
        y=df_dam["全流入量"],
        name="全流入量",
        line=dict(color="red"),
    ),
    row=2,
    col=1,
)
fig_dam.add_trace(
    go.Scatter(
        x=df_dam["日時"],
        y=df_dam["全放流量"],
        name="全放流量",
        line=dict(color="green"),
    ),
    row=2,
    col=1,
)

# 防災操作（洪水調節）
fig_dam.add_hline(y=90, line_width=1, line_dash="dot", line_color="red", row=2, col=1)

# レイアウトと軸の設定
fig_dam.update_layout(
    hovermode="x unified",
    height=800,
    hoverlabel=dict(namelength=-1),
    xaxis=dict(tickformat="%H:%M\n%Y-%m-%d", hoverformat="%Y-%m-%d %H:%M"),
    xaxis2=dict(tickformat="%H:%M\n%Y-%m-%d", hoverformat="%Y-%m-%d %H:%M"),
)

# グラフの表示
tab2.plotly_chart(fig_dam, use_container_width=True)

df_dam.set_index("日時", inplace=True)

tab2.dataframe(df_dam.style.highlight_max(axis=0), use_container_width=True)

tab3.subheader("蒼社川")

fig_river = make_subplots(rows=3, cols=1)

fig_river.add_trace(
    go.Scatter(
        x=df_river["日時"],
        y=df_river["中通"],
        name="中通",
        line=dict(color="blue"),
    ),
    row=1,
    col=1,
)

fig_river.add_trace(
    go.Scatter(
        x=df_river["日時"],
        y=df_river["高野"],
        name="高野",
        line=dict(color="red"),
    ),
    row=2,
    col=1,
)
fig_river.add_trace(
    go.Scatter(
        x=df_river["日時"],
        y=df_river["片山"],
        name="片山",
        line=dict(color="green"),
    ),
    row=3,
    col=1,
)


# 水防団待機水位（高野）
fig_river.add_hline(y=3.5, line_width=1, line_dash="dot", line_color="green", row=2, col=1)
# 氾濫注意水位（高野）
fig_river.add_hline(y=4, line_width=1, line_dash="dot", line_color="orange", row=2, col=1)

# 水防団待機水位（片山）
fig_river.add_hline(y=2.1, line_width=1, line_dash="dot", line_color="green", row=3, col=1)
# 氾濫注意水位（片山）
fig_river.add_hline(y=2.4, line_width=1, line_dash="dot", line_color="orange", row=3, col=1)
# 避難判断水位（片山）
fig_river.add_hline(y=2.6, line_width=1, line_dash="dot", line_color="red", row=3, col=1)
# 氾濫危険水位（片山）
fig_river.add_hline(y=2.85, line_width=1, line_dash="dot", line_color="purple", row=3, col=1)

# レイアウトと軸の設定
fig_river.update_layout(
    # title="蒼社川水位",
    hovermode="x unified",
    height=800,
    hoverlabel=dict(namelength=-1),
    xaxis=dict(tickformat="%H:%M\n%Y-%m-%d", hoverformat="%Y-%m-%d %H:%M"),
    xaxis2=dict(tickformat="%H:%M\n%Y-%m-%d", hoverformat="%Y-%m-%d %H:%M"),
    xaxis3=dict(tickformat="%H:%M\n%Y-%m-%d", hoverformat="%Y-%m-%d %H:%M"),
)

# グラフの表示
tab3.plotly_chart(fig_river, use_container_width=True)

df_river.set_index("日時", inplace=True)

tab3.dataframe(df_river.style.highlight_max(axis=0), use_container_width=True)
