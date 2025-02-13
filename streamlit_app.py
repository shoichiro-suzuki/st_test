# pip install streamlit
import streamlit as st
from azure_.cosmosdb import upsert_to_container
from azure_.blob_strage import upload_blob_to_azure
from tools.gps import get_gps_coordinates, get_full_address
from st_init import init

st.set_page_config(page_title="作業報告", layout="wide", page_icon="🐗")


def main():
    st.title("作業報告🐗")
    with st.form(key="task_form"):
        users = st.multiselect("従事者", ["宮田", "加藤", "伊藤"])
        uploaded_files = st.file_uploader(
            "写真をアップロード", accept_multiple_files=True, type=["jpg", "png"]
        )
        task_type = st.selectbox("作業種類", ["見回り", "捕獲"])
        task_date = st.date_input("日付")
        task_description = st.text_area("作業内容を入力")
        # ボタンが押せるかどうかの条件を設定
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        # uploaded_files が1つ以上で、users が1つ以上選択されている場合のみ処理を実行
        if uploaded_files and users:
            data = {
                "users": users,
                "task_type": task_type,
                "task_date": task_date.strftime("%Y-%m-%d"),
                "task_description": task_description,
            }
            # st.write(data)

            if uploaded_files:
                first_file = uploaded_files[0]
                gps_coordinates = get_gps_coordinates(first_file.read())
                if gps_coordinates:
                    lat, lon = gps_coordinates
                    st.write(f"位置情報: 緯度 {lat}, 経度 {lon}")
                else:
                    st.write("位置情報が見つかりませんでした。")

            try:
                # アップロードされたファイルを Azure Blob Storage にアップロード
                for uploaded_file in uploaded_files:
                    blob_name = uploaded_file.name
                    print("blob_name==>", blob_name)
                    upload_blob_to_azure(
                        "study",
                        blob_name,
                        uploaded_file,
                    )

            except Exception as e:
                st.error(f"Blob登録エラー: {e}")
                return

            try:
                # Cosmos DB にデータを登録
                upsert_to_container(
                    database_name="02_Documents", container_name="study", data=data
                )
            except Exception as e:
                st.error(f"CosmosDB登録エラー: {e}")
                return
            st.success("送信完了")
        else:
            # 入力されていない項目に応じてエラーメッセージを変更する
            if not users:
                st.error("従事者を選択してください。")
            if not uploaded_files:
                st.error("写真をアップロードしてください。")


data = [
    {
        "latitude": 34.600521,
        "longitude": 137.121363,
        "place": "花の村ソーラーの道",
        "address": "愛知県田原市和地町",
        "muniCd": "23203",
        "id": "wazi-1",
    },
    {
        "latitude": 34.606175,
        "longitude": 137.109573,
        "place": "ハラサワ",
        "address": "愛知県田原市和地町",
        "muniCd": "23203",
        "id": "wazi-2",
    },
    {
        "latitude": 34.610929,
        "longitude": 137.113483,
        "place": "アキモトさんの檻",
        "address": "愛知県田原市長沢町",
        "muniCd": "23231",
        "id": "wazi-3",
    },
    {
        "latitude": 34.596175,
        "longitude": 137.123857,
        "place": "花の村駐車場横",
        "address": "愛知県田原市和地町",
        "muniCd": "23203",
        "id": "wazi-4",
    },
    {
        "latitude": 34.597054,
        "longitude": 137.126528,
        "place": "花の村の奥",
        "address": "愛知県田原市和地町",
        "muniCd": "23203",
        "id": "wazi-5",
    },
]


if __name__ == "__main__":
    init()
    main()
    # trap_map(data)
