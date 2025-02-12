# pip install streamlit
import streamlit as st
from azure_.cosmosdb import upsert_to_container
from azure_.blob_strage import upload_blob_to_azure


st.set_page_config(page_title="作業報告", layout="wide", page_icon="🐗")


def main():
    st.title("作業報告🐗")
    with st.form(key="task_form"):
        users = st.multiselect("ユーザーを選択", ["宮田", "加藤", "伊藤"])
        uploaded_files = st.file_uploader(
            "写真をアップロード", accept_multiple_files=True
        )
        task_type = st.selectbox("作業種類を選択", ["見回り", "捕獲"])
        task_date = st.date_input("作業日を選択")
        task_description = st.text_area("作業内容を入力")
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        data = {
            "users": users,
            "task_type": task_type,
            "task_date": task_date.strftime("%Y-%m-%d"),  # 日付を文字列に変換
            "task_description": task_description,
        }
        st.write(data)
        try:
            # アップロードされたファイルを Azure Blob Storage にアップロード
            for uploaded_file in uploaded_files:
                blob_name = uploaded_file.name
                print("blob_name==>", blob_name)
                message = upload_blob_to_azure(
                    "study",
                    blob_name,
                    uploaded_file,
                )
                st.success(message)
        except Exception as e:
            st.error(f"Blob登録エラー: {e}")
            return
        try:
            # Cosmos DB にデータを登録
            upsert_to_container(
                database_name="02_Documents", container_name="study", data=data
            )
            st.success("CosmosDB に登録しました")
        except Exception as e:
            st.error(f"CosmosDB登録エラー: {e}")
            return


if __name__ == "__main__":
    main()
