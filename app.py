import streamlit as st
import pandas as pd

st.title("Фильтр Trustpilot и Google Play по брендам")
st.subheader("ВНИМАНИЕ! Перед тем как грузить таблицу, убедитесь что в таблице только 3 колонки: Поисковая фраза, Позиция и Выдача. Формат таблицы CSV!")

uploaded_file = st.file_uploader("Вставьте CSV файл с таблицей", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    all_phrases = df[["Поисковая фраза"]].drop_duplicates()

    mask_trust = df["Выдача"].str.contains("trustpilot", case=False, na=False)
    mask_play = df["Выдача"].str.contains("play.google.com", case=False, na=False)
    mask_both = mask_trust | mask_play
    both_trust_play = df[mask_both]
    #othercases = df[~mask_trust & ~mask_play]

    grouped_both = both_trust_play.groupby("Поисковая фраза", as_index=False).agg({
        "Позиция": lambda x: "\n".join(x.dropna().astype(str)),
        "Выдача": lambda x: "\n".join(x.dropna().astype(str))
    })

    #noduplicate_othercases = othercases.drop_duplicates(subset="Поисковая фраза")
    #noduplicate_othercases["Выдача"] = ""
    #noduplicate_othercases["Позиция"] = ""

    #result = pd.concat([grouped_both, noduplicate_othercases], ignore_index=True)
    result = all_phrases.merge(grouped_both,on="Поисковая фраза",how="left")
    result["Позиция"] = result["Позиция"].fillna("")
    result["Выдача"] = result["Выдача"].fillna("")

    st.write("Результат фильтрации")
    st.dataframe(result)

    csv = result.to_csv(index=False).encode("utf-8")

    st.download_button(
        label = "Скачать результат в CSV",
        data = csv,
        file_name = "Result.csv",
        mime = "text/csv",
    )
