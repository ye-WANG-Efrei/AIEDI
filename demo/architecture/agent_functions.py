# agent_functions.py
from pandasai.core.prompts.base import BasePrompt
import pandasai as pai
import pandas as pd
from pathlib import Path
import os
import re
import logging
from pandasai.dataframe.base import DataFrame as PaiDataFrame
import streamlit as st

# 你可以在这里设置API KEY和全局配置
pai.api_key.set("PAI-a4927d55-bcb4-4e97-8cef-4250564d1f69")

def ai_chat(user_query, pai_dfs):
    """
    核心AI对话函数
    :param user_query: 英文问题
    :param pai_dfs: DataFrame列表
    :return: AI返回结果（DataFrame或字符串）
    """
    response = pai.chat(user_query, *pai_dfs)
    return response.value if hasattr(response, "value") else response

def read_excel(excel_path,sheet_name=None):
    """
    读取 Excel 文件的所有 sheet，返回 pandasai DataFrame 列表
    :param excel_path: Excel 文件路径
    :return: DataFrame 列表
    """
    all_sheets = pd.read_excel(excel_path, sheet_name=sheet_name)
    pai_dfs = []
    for sheet_name, df in all_sheets.items():
        pai_df = PaiDataFrame(df)
        pai_dfs.append(pai_df)
    return pai_dfs

# =====================
# 单表自动类型读取
# =====================
def read_single_table(file_path):
    """
    根据文件类型读取单表，支持 csv、parquet、excel，返回 pandasai DataFrame
    :param file_path: 文件路径
    :return: pandasai DataFrame
    """
    ext = Path(file_path).suffix.lower()
    if ext == '.csv':
        return pai.read_csv(file_path)
    elif ext == '.parquet':
        return pai.read_parquet(file_path)
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
        return PaiDataFrame(df)
    else:
        raise ValueError(f"不支持的文件类型: {ext}")

# =====================
# 自动创建数据集装饰器
# =====================
def auto_create_dataset(read_func):
    def wrapper(file_path, path, **kwargs):
        df = read_func(file_path)
        return pai.create(path=path, df=df, **kwargs)
    return wrapper

# 用装饰器封装后的单表读取+创建
@auto_create_dataset
def read_single_table_for_create(file_path):
    return read_single_table(file_path)

