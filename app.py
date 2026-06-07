import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="FitFlix", page_icon="🔥", layout="wide", initial_sidebar_state="collapsed")

if "page" not in st.session_state:
    st.session_state.page = "Home"

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;700&display=swap');
  html,body,[class*="css"]{font-family:'Barlow',sans-serif;background-color:#0f1117;color:#e5e5e5;}
  .stApp{background-color:#0f1117;}
  #MainMenu,footer,header{visibility:hidden;}
  [data-testid="stSidebar"]{display:none;}
  .block-container{padding:0 2rem 4rem 2rem !important;max-width:1400px;}

  div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button{
    background:transparent !important;color:#9ba3b5 !important;
    border:1px solid #2e3240 !important;border-radius:8px !important;
    font-family:'Barlow',sans-serif !important;font-weight:500 !important;
    font-size:0.82rem !important;letter-spacing:0.04em !important;
    padding:0.42rem 1.1rem !important;transition:all 0.18s ease !important;
    white-space:nowrap !important;text-transform:none !important;width:100% !important;
  }
  div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button:hover{
    background:#1f2333 !important;border-color:#464e66 !important;color:#e5e5e5 !important;transform:none !important;
  }
  .nav-active div[data-testid="stButton"] button{
    background:#1a1f2e !important;border-color:#e50914 !important;color:#ffffff !important;
  }
  .action-btn div[data-testid="stButton"] button{
    background:#e50914 !important;color:white !important;border:none !important;
    border-radius:6px !important;font-weight:700 !important;font-size:.88rem !important;
    letter-spacing:.07em !important;text-transform:uppercase !important;padding:.6rem 2rem !important;
  }
  .action-btn div[data-testid="stButton"] button:hover{background:#f40612 !important;transform:scale(1.02) !important;}

  .hero{width:calc(100% + 4rem);margin-left:-2rem;min-height:460px;
    background:linear-gradient(105deg,#080a0e 0%,rgba(8,10,14,.9) 38%,rgba(15,17,23,.25) 100%),
    url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1400&q=80') center/cover no-repeat;
    display:flex;align-items:flex-end;padding:3rem;border-radius:0 0 10px 10px;margin-bottom:2.5rem;}
  .hero-tag{font-family:'Barlow Condensed',sans-serif;font-size:.75rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#e50914;margin-bottom:.4rem;}
  .hero-title{font-family:'Bebas Neue',sans-serif;font-size:clamp(3rem,6vw,5rem);line-height:.95;color:#fff;letter-spacing:.02em;margin-bottom:.9rem;text-shadow:0 4px 24px rgba(0,0,0,.8);}
  .hero-title span{color:#e50914;}
  .hero-desc{font-size:.95rem;font-weight:300;color:#888;line-height:1.6;}

  .metric-row{display:flex;gap:1rem;margin-bottom:2.5rem;flex-wrap:wrap;}
  .metric-card{flex:1;min-width:140px;background:linear-gradient(135deg,#1c1f2a,#151820);border:1px solid #252836;border-radius:8px;padding:1.2rem 1.5rem;position:relative;overflow:hidden;transition:border-color .2s,transform .2s;}
  .metric-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:#e50914;}
  .metric-card:hover{border-color:#e50914;transform:translateY(-2px);}
  .metric-value{font-family:'Bebas Neue',sans-serif;font-size:2.6rem;color:#fff;line-height:1;}
  .metric-label{font-size:.72rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:#555;margin-top:.3rem;}

  .section-header{display:flex;align-items:center;gap:.75rem;margin:2rem 0 1.2rem 0;}
  .section-title{font-family:'Bebas Neue',sans-serif;font-size:1.5rem;letter-spacing:.05em;color:#fff;}
  .section-accent{width:36px;height:3px;background:#e50914;border-radius:2px;}

  .exercise-card{background:linear-gradient(145deg,#1c1f2a,#161820);border:1px solid #252836;border-radius:8px;padding:1.1rem .95rem;position:relative;overflow:hidden;transition:all .22s ease;}
  .exercise-card::after{content:"";position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#e50914,#ff6b35);transform:scaleX(0);transition:transform .22s ease;}
  .exercise-card:hover{border-color:#3a3f52;transform:scale(1.04);box-shadow:0 10px 36px rgba(229,9,20,.15);}
  .exercise-card:hover::after{transform:scaleX(1);}
  .exercise-number{font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:#252836;line-height:1;margin-bottom:.4rem;}
  .exercise-name{font-weight:600;font-size:.85rem;color:#e5e5e5;line-height:1.3;}
  .exercise-badge{display:inline-block;margin-top:.55rem;padding:.12rem .45rem;border-radius:3px;font-size:.62rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;background:rgba(229,9,20,.15);color:#e50914;border:1px solid rgba(229,9,20,.3);}

  .prediction-result{background:linear-gradient(135deg,#1a0a0a,#1f1414);border:1px solid #e50914;border-radius:8px;padding:2rem;text-align:center;box-shadow:0 0 60px rgba(229,9,20,.15);margin-top:1.5rem;}
  .prediction-label{font-size:.72rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#555;margin-bottom:.5rem;}
  .prediction-value{font-family:'Bebas Neue',sans-serif;font-size:4rem;color:#e50914;letter-spacing:.05em;}

  .stSelectbox>div>div{background-color:#1c1f2a !important;border-color:#2e3240 !important;color:#e5e5e5 !important;border-radius:6px !important;}
  .stSelectbox label{color:#888 !important;font-size:.78rem !important;font-weight:600 !important;letter-spacing:.07em !important;text-transform:uppercase !important;}
  [data-testid="stSuccess"]{background:rgba(229,9,20,.1) !important;border-color:#e50914 !important;color:#e5e5e5 !important;border-radius:6px !important;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_data():
    df         = pickle.load(open("gym_data.pkl","rb"))
    similarity = pickle.load(open("similarity.pkl","rb"))
    model      = pickle.load(open("difficulty_model.pkl","rb"))
    tfidf      = pickle.load(open("tfidf.pkl","rb"))
    le         = pickle.load(open("label_encoder.pkl","rb"))
    return df,similarity,model,tfidf,le

df,similarity,model,tfidf,le = load_data()

NETFLIX_PAL=["#e50914","#ff6b35","#ff9f1c","#c7243a","#8b0000","#ff4444","#cc0000","#990000","#ff8c00","#ff5500"]
def dark_style():
    plt.rcParams.update({"figure.facecolor":"#1c1f2a","axes.facecolor":"#1c1f2a","axes.edgecolor":"#252836","axes.labelcolor":"#777","xtick.color":"#555","ytick.color":"#555","text.color":"#e5e5e5","grid.color":"#1f2233","grid.linewidth":.6,"font.family":"sans-serif","axes.spines.top":False,"axes.spines.right":False})

# ── NAVBAR ──
pages=[("🏠","Home"),("📊","Analytics"),("🎯","Recommendations"),("🤖","Difficulty Predictor")]
col_logo,c1,c2,c3,c4=st.columns([1.4,1.1,1.1,1.4,1.5])
with col_logo:
    st.markdown("<div style=\"font-family:'Bebas Neue',sans-serif;font-size:1.55rem;color:#e50914;padding-top:.35rem;letter-spacing:.04em\">FIT<span style=\"color:#fff\">FLIX</span></div>",unsafe_allow_html=True)
for col,(icon,label) in zip([c1,c2,c3,c4],pages):
    with col:
        active=st.session_state.page==label
        if active: st.markdown("<div class=\"nav-active\">",unsafe_allow_html=True)
        if st.button(f"{icon}  {label}",key=f"nav_{label}"):
            st.session_state.page=label; st.rerun()
        if active: st.markdown("</div>",unsafe_allow_html=True)
st.markdown("<hr style=\"border:none;border-top:1px solid #1e2130;margin:.4rem 0 2rem 0\"/>",unsafe_allow_html=True)
page=st.session_state.page

lvc={"Beginner":"#27ae60","Intermediate":"#f39c12","Expert":"#e50914"}

# ── HOME ──
if page=="Home":
    st.markdown("""<div class="hero"><div style="max-width:600px"><div class="hero-tag">▶ Now Streaming — Workouts</div><div class="hero-title">YOUR NEXT<br><span>GREAT</span><br>WORKOUT</div><div class="hero-desc">Discover, track, and master exercises curated just for you.<br>Powered by AI · Built for results.</div></div></div>""",unsafe_allow_html=True)
    st.markdown(f"""<div class="metric-row"><div class="metric-card"><div class="metric-value">{len(df)}</div><div class="metric-label">Total Exercises</div></div><div class="metric-card"><div class="metric-value">{df["BodyPart"].nunique()}</div><div class="metric-label">Body Parts</div></div><div class="metric-card"><div class="metric-value">{df["Equipment"].nunique()}</div><div class="metric-label">Equipment Types</div></div><div class="metric-card"><div class="metric-value">{round(df["Rating"].mean(),1)}</div><div class="metric-label">Avg Rating</div></div></div>""",unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">TOP PICKS FOR YOU</div></div>',unsafe_allow_html=True)
    top=df.nlargest(8,"Rating"); cols=st.columns(8)
    for i,(col,(_,row)) in enumerate(zip(cols,top.iterrows())):
        with col:
            c=lvc.get(row.get("Level",""),"#e50914")
            st.markdown(f"<div class=\"exercise-card\"><div class=\"exercise-number\">0{i+1}</div><div class=\"exercise-name\">{row['Title']}</div><span class=\"exercise-badge\" style=\"color:{c};border-color:{c}\">{row.get('Level','')}</span></div>",unsafe_allow_html=True)
    for bp in df["BodyPart"].value_counts().head(5).index:
        sub=df[df["BodyPart"]==bp].nlargest(5,"Rating")
        st.markdown(f"<p style='font-family:Barlow Condensed,sans-serif;font-size:.95rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#444;margin:1.5rem 0 .5rem 0'>{bp}</p>",unsafe_allow_html=True)
        cols=st.columns(5)
        for col,(_,row) in zip(cols,sub.iterrows()):
            with col: st.markdown(f"<div class=\"exercise-card\" style=\"padding:.85rem .8rem\"><div class=\"exercise-name\" style=\"font-size:.78rem\">{row['Title']}</div><span class=\"exercise-badge\">⭐ {round(row['Rating'],1)}</span></div>",unsafe_allow_html=True)

# ── ANALYTICS ──
elif page=="Analytics":
    st.markdown("<div style=\"font-family:'Bebas Neue',sans-serif;font-size:2.8rem;color:#fff;letter-spacing:.05em;margin-bottom:1rem\">ANALYTICS <span style=\"color:#e50914\">DASHBOARD</span></div>",unsafe_allow_html=True)
    bodypart=st.selectbox("Filter by Body Part",["All"]+sorted(df["BodyPart"].unique()))
    data=df if bodypart=="All" else df[df["BodyPart"]==bodypart]; dark_style()
    col1,col2=st.columns(2)
    with col1:
        st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">BY BODY PART</div></div>',unsafe_allow_html=True)
        fig,ax=plt.subplots(figsize=(6,5)); counts=data["BodyPart"].value_counts()
        bars=ax.barh(counts.index,counts.values,color=NETFLIX_PAL[:len(counts)],height=.6)
        ax.set_xlabel("Count"); ax.grid(axis="x",alpha=.3)
        for bar,val in zip(bars,counts.values): ax.text(val+.3,bar.get_y()+bar.get_height()/2,str(val),va="center",color="#e5e5e5",fontsize=9)
        fig.tight_layout(); st.pyplot(fig)
    with col2:
        st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">DIFFICULTY BREAKDOWN</div></div>',unsafe_allow_html=True)
        fig,ax=plt.subplots(figsize=(6,5)); lv=data["Level"].value_counts()
        wedges,texts,autotexts=ax.pie(lv.values,labels=lv.index,autopct="%1.0f%%",colors=["#27ae60","#f39c12","#e50914"][:len(lv)],startangle=90,wedgeprops=dict(linewidth=2,edgecolor="#0f1117"))
        for t in texts: t.set_color("#888")
        for t in autotexts: t.set_color("#fff"); t.set_fontweight("bold")
        fig.patch.set_facecolor("#1c1f2a"); fig.tight_layout(); st.pyplot(fig)
    st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">RATING DISTRIBUTION</div></div>',unsafe_allow_html=True)
    fig,ax=plt.subplots(figsize=(12,3.5)); ax.hist(data["Rating"],bins=25,color="#e50914",alpha=.85,edgecolor="#0f1117",linewidth=.5)
    ax.set_xlabel("Rating"); ax.set_ylabel("Count"); ax.grid(axis="y",alpha=.3); fig.tight_layout(); st.pyplot(fig)
    st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">TOP RATED EXERCISES</div></div>',unsafe_allow_html=True)
    top10=data.nlargest(10,"Rating"); fig,ax=plt.subplots(figsize=(12,5))
    ax.barh(top10["Title"][::-1],top10["Rating"][::-1],color=[NETFLIX_PAL[i%10] for i in range(10)],height=.65)
    ax.set_xlim(top10["Rating"].min()*.97,top10["Rating"].max()*1.01); ax.grid(axis="x",alpha=.3); fig.tight_layout(); st.pyplot(fig)
    st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">EQUIPMENT x LEVEL HEATMAP</div></div>',unsafe_allow_html=True)
    pivot=data.pivot_table(index="Equipment",columns="Level",values="Rating",aggfunc="count",fill_value=0)
    fig,ax=plt.subplots(figsize=(12,max(4,len(pivot)*.45))); sns.heatmap(pivot,ax=ax,cmap="Reds",linewidths=.5,linecolor="#0f1117",annot=True,fmt="d",cbar_kws={"shrink":.7})
    fig.tight_layout(); st.pyplot(fig)

# ── RECOMMENDATIONS ──
elif page=="Recommendations":
    st.markdown("<div style=\"font-family:'Bebas Neue',sans-serif;font-size:2.8rem;color:#fff;letter-spacing:.05em;margin-bottom:.3rem\">EXERCISE <span style=\"color:#e50914\">RECOMMENDATIONS</span></div>",unsafe_allow_html=True)
    st.markdown("<p style=\"color:#555;margin-bottom:1.5rem\">Smart picks powered by cosine similarity AI</p>",unsafe_allow_html=True)
    col_sel,col_btn=st.columns([3,1])
    with col_sel: exercise=st.selectbox("Choose an exercise you like",sorted(df["Title"].unique()))
    with col_btn:
        st.write(""); st.write("")
        st.markdown("<div class=\"action-btn\">",unsafe_allow_html=True)
        clicked=st.button("▶ Get Picks")
        st.markdown("</div>",unsafe_allow_html=True)
    sel=df[df["Title"]==exercise].iloc[0]
    st.markdown(f"""<div style="background:#1c1f2a;border:1px solid #252836;border-radius:8px;padding:1.4rem;margin:1rem 0 1.5rem 0"><div style="font-size:.68rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#e50914;margin-bottom:.35rem">SELECTED</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:#fff;margin-bottom:.7rem">{sel["Title"]}</div><div style="display:flex;gap:.6rem;flex-wrap:wrap"><span style="background:#131620;border:1px solid #252836;border-radius:4px;padding:.18rem .55rem;font-size:.72rem;color:#777">💪 {sel.get("BodyPart","—")}</span><span style="background:#131620;border:1px solid #252836;border-radius:4px;padding:.18rem .55rem;font-size:.72rem;color:#777">🏋️ {sel.get("Equipment","—")}</span><span style="background:#131620;border:1px solid #252836;border-radius:4px;padding:.18rem .55rem;font-size:.72rem;color:#777">⚡ {sel.get("Level","—")}</span><span style="background:#131620;border:1px solid #252836;border-radius:4px;padding:.18rem .55rem;font-size:.72rem;color:#777">⭐ {round(sel.get("Rating",0),1)}</span></div></div>""",unsafe_allow_html=True)
    def recommend(name,n=10):
        idx=df[df["Title"]==name].index[0]
        return [df.iloc[s[0]] for s in sorted(enumerate(similarity[idx]),key=lambda x:x[1],reverse=True)[1:n+1]]
    if clicked:
        recs=recommend(exercise,10)
        st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">BECAUSE YOU LIKE THIS</div></div>',unsafe_allow_html=True)
        cols=st.columns(5)
        for i,(col,row) in enumerate(zip(cols*2,recs)):
            with col:
                c=lvc.get(row.get("Level",""),"#e50914")
                st.markdown(f"<div class=\"exercise-card\"><div class=\"exercise-number\">0{i+1}</div><div class=\"exercise-name\">{row['Title']}</div><div style=\"margin-top:.45rem\"><span style=\"font-size:.68rem;color:#444\">{row.get('BodyPart','')}</span><br><span class=\"exercise-badge\" style=\"color:{c};border-color:{c}\">{row.get('Level','')}</span></div></div>",unsafe_allow_html=True)
        dark_style()
        st.markdown('<div class="section-header" style="margin-top:2rem"><div class="section-accent"></div><div class="section-title">SIMILARITY SCORES</div></div>',unsafe_allow_html=True)
        idx=df[df["Title"]==exercise].index[0]
        scores=sorted(enumerate(similarity[idx]),key=lambda x:x[1],reverse=True)[1:11]
        titles=[(df.iloc[s[0]]["Title"][:27]+"…" if len(df.iloc[s[0]]["Title"])>27 else df.iloc[s[0]]["Title"]) for s in scores]
        vals=[s[1] for s in scores]
        fig,ax=plt.subplots(figsize=(12,4))
        ax.bar(range(len(titles)),vals,color=["#e50914"]+["#2e3240"]*9,width=.6)
        ax.set_xticks(range(len(titles))); ax.set_xticklabels(titles,rotation=33,ha="right",fontsize=9)
        ax.set_ylabel("Cosine Similarity"); ax.set_ylim(0,max(vals)*1.15)
        for i,v in enumerate(vals): ax.text(i,v+.004,f"{v:.3f}",ha="center",color="#e5e5e5",fontsize=8)
        ax.grid(axis="y",alpha=.3); fig.tight_layout(); st.pyplot(fig)

# ── DIFFICULTY PREDICTOR ──
elif page=="Difficulty Predictor":
    st.markdown("<div style=\"font-family:'Bebas Neue',sans-serif;font-size:2.8rem;color:#fff;letter-spacing:.05em;margin-bottom:.3rem\">AI DIFFICULTY <span style=\"color:#e50914\">PREDICTOR</span></div>",unsafe_allow_html=True)
    st.markdown("<p style=\"color:#555;margin-bottom:1.5rem\">Let the model gauge how hard your workout will be</p>",unsafe_allow_html=True)
    col1,col2,col3=st.columns(3)
    with col1: type_input=st.selectbox("Exercise Type",sorted(df["Type"].unique()))
    with col2: body_input=st.selectbox("Body Part",sorted(df["BodyPart"].unique()))
    with col3: equipment_input=st.selectbox("Equipment",sorted(df["Equipment"].unique()))
    st.write("")
    st.markdown("<div class=\"action-btn\">",unsafe_allow_html=True)
    predict_btn=st.button("🔥 Predict Difficulty")
    st.markdown("</div>",unsafe_allow_html=True)
    if predict_btn:
        text=f"{type_input} {body_input} {equipment_input}"
        vector=tfidf.transform([text]); pred=model.predict(vector); level=le.inverse_transform(pred)[0]
        icon_map={"Beginner":"🟢","Intermediate":"🟡","Expert":"🔴"}
        col_map={"Beginner":"#27ae60","Intermediate":"#f39c12","Expert":"#e50914"}
        icon,color=icon_map.get(level,"🔴"),col_map.get(level,"#e50914")
        st.markdown(f"""<div class="prediction-result" style="border-color:{color};box-shadow:0 0 60px {color}22"><div class="prediction-label">Predicted Difficulty Level</div><div class="prediction-value" style="color:{color}">{icon} {level.upper()}</div><div style="color:#444;font-size:.82rem;margin-top:.75rem">{type_input} · {body_input} · {equipment_input}</div></div>""",unsafe_allow_html=True)
        similar=df[df["Level"]==level].sample(min(6,len(df[df["Level"]==level]))).reset_index()
        st.markdown(f"<div class=\"section-header\" style=\"margin-top:2rem\"><div class=\"section-accent\"></div><div class=\"section-title\">OTHER {level.upper()} EXERCISES</div></div>",unsafe_allow_html=True)
        cols=st.columns(6)
        for col,(_,row) in zip(cols,similar.iterrows()):
            with col: st.markdown(f"<div class=\"exercise-card\"><div class=\"exercise-name\" style=\"font-size:.78rem\">{row['Title']}</div><span class=\"exercise-badge\" style=\"color:{color};border-color:{color}\">{row.get('BodyPart','')}</span></div>",unsafe_allow_html=True)