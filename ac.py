import io

import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv
import time

def main():
    st.title("Activity Test List")

    # Load credentials from YAML
    with open('credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

  
    try:
        data = pd.read_excel("活性送測整理-webview.xlsx")
    
        # print(f"data type: {type(data.to_excel())}")
    
        # Display data
        # st.write("### Data from Excel")
        # st.dataframe(data)
    
        # Create a download button
        df = pd.read_excel('活性送測整理-webview.xlsx')
    
        column_to_split = '分類'
        unique_values = df[column_to_split].unique()
    
        buffer = io.BytesIO()
    
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            for value in unique_values:
                filtered_df = df[df[column_to_split] == value]
    
                filtered_df.to_excel(writer, sheet_name=str(value), index=False)
    
        excel_data = buffer.getvalue()
    
        st.download_button(label='Download Excel File',
                           data=excel_data,
                           file_name='exported.xlsx',
                           mime="application/vnd.ms-excel")
    
    
        # Interactive filtering
        st.write("### Filter Data")
        column = st.selectbox("Select column to filter", data.columns[1])
        unique_values = data[column].unique()
        selected_value = st.selectbox("Select value", unique_values)
        filtered_data = data[data[column] == selected_value]
    
    
        st.dataframe(filtered_data[['樣品','送測編號','樣品重量(mg)','日期','取樣者','備註']], hide_index=True)
        st.write('Total count: ', len(filtered_data))
    
        # Filtered by latest date
        # data['日期_formatted'] = data['日期'].dt.strftime('%d-%m-%y')
    
        data['日期'] = pd.to_datetime(data['日期'], errors='coerce', utc=True)
    
        latest_date = data['日期'].max()
        st.write("### Latest Data")
    
        st.dataframe(data[data['日期'] == latest_date], hide_index=True)
        st.write('Total count: ', len(data[data['日期'] == latest_date]))
        # st.write('Total price: ', filtered_data['Total'].sum())
    
    except FileNotFoundError:
        st.error("Excel file not found. Please ensure data is in the same directory")
    except Exception as e:
        st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
