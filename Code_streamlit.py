import os, sys, subprocess

if __name__ == "__main__" and os.environ.get("RUNNING_IN_STREAMLIT") != "true":
    os.environ["RUNNING_IN_STREAMLIT"] = "true"
    subprocess.run(["streamlit", "run", sys.argv[0]], check=False)
    sys.exit(0)
    
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Recruit Dashboard")

st.title("Title")

if st.button("Recruit Searching"):
    jk_path = "data_tmp/data_jobkorea.csv"
    sm_path = "data_tmp/data_saramin.csv"

    if not os.path.exists(jk_path) or not os.path.exists(sm_path):
        st.error("data_tmp 폴더에 data_jobkorea.csv, data_saramin.csv 파일이 있어야 합니다.")
        st.stop()

    df_jk = pd.read_csv(jk_path)
    df_sm = pd.read_csv(sm_path)

    keep_cols = ["Site", "Col_Company", "Col_Recruit"]
    df_all = (
        pd.concat([df_jk, df_sm], ignore_index=True, sort=False)
        .loc[:, keep_cols]
        .dropna(how="any", subset=["Site", "Col_Company", "Col_Recruit"])
    )

    st.dataframe(df_all)

    grp = (
        df_all.groupby("Site", dropna=False)
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
        .reset_index(drop=True)
    )
    total = grp["Count"].sum()
    grp["Ratio"] = (grp["Count"] / total * 100).round(2)

    st.dataframe(grp)
    st.subheader("Recruitment Ratio")
    
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        grp["Count"],
        autopct=lambda p: f"{p:.1f}%",
        startangle=90
    )

    ax.legend(
        wedges,
        grp["Site"],
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )

    ax.axis("equal")
    st.pyplot(fig)