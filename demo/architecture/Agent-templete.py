from pandasai.core.prompts.base import BasePrompt
import pandasai as pai
import pandas as pd
from pathlib import Path
import os
import re
import logging
from pandasai.dataframe.base import DataFrame as PaiDataFrame
from Readfile import read_file
from pandasai.llm.bamboo_llm import BambooLLM
from pandasai.core.prompts.base import BasePrompt
from agent_functions import *

# 设置环境变量启用调试模式
os.environ["PANDASAI_VERBOSE"] = "1"

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pandasai')
logger.setLevel(logging.DEBUG)

def print_query_info(response):
    """打印查询信息，包括生成的代码"""

    print("\n查询结果:")
    print(response)

# 创建配置
config = {
    "verbose": True,
    "save_logs": True,
    "enable_cache": False
}


pai.api_key.set("PAI-a4927d55-bcb4-4e97-8cef-4250564d1f69")
# Load your data
# df = pai.DataFrame(pd.read_csv("../../data/TBC Lille.csv"))
# 用 pandas 讀 CSV，並加上 encoding 參數



# ------------------------------------------------------------------------------------
# 多表讀取
# all_sheets = pd.read_excel("D:\mine\corsur\EDI\NEW_2005-main\data\SpesLog_wWX1385281_Fri0523_164218\pre-load\提取.xlsx", sheet_name=None)

# pai_dfs = []

# for sheet_name, dfs in all_sheets.items():
#     df = pai.DataFrame(dfs)
#     pai_dfs.append(df)
#     print(f"已轉換：{sheet_name} -> pai.DataFrame")

# df = pd.read_excel("data/renn.xlsx")
# df = pai.DataFrame(df)

# mytickets = pai.create(
#     "data\pre-load\总工单表-wy.xlsx",
#     df,
#     description="This is a dedicated inventory file for Rennes, used to record all items and their serial numbers."
# )

# orders_dataset = pai.create(
#     "data/huawei-export-inventaire-genateq-1",
#     pai_dfs[1],
#     description="This is mainly used to search for items and their serial numbers in the location inventory."
# )

# orders_dataset1 = pai.create(
#     "data/huawei-export-inventaire-genateq-2",
#     pai_dfs[0],
#     description="Show the total count of each inventory item."
# )

# orders_dataset2 = pai.create(
#     "data/huawei-export-inventaire-genateq-3",
#     pai_dfs[2],
#     description="do not use this dataset"
# )

# orders_dataset3 = pai.create(
#     "data/huawei-export-inventaire-genateq-4",
#     pai_dfs[3],
#     description="do not use this dataset"
# )

# orders_dataset4 = pai.create(
#     "data/huawei-export-inventaire-genateq-5",
#     pai_dfs[4],
#     description="do not use this dataset"
# )
# #多表詢問(多表)
# response = pai.chat( "show me all item with serial number which localisation is STOCK_RENNES in the dataset, bom col as item ", *pai_dfs)
# response = pai.DataFrame(response.value)
# result = pai.chat( "Compare serial numbers for each item between table1 and table2. List serial numbers from table1 that do not appear in table2, and serial numbers from table2 that do not appear in table1. Do not create pairwise combinations. Only show missing serials with their item code.", response, df)
# print("Second query result:")
# print(result)

# bllm = BambooLLM(api_key="PAI-a4927d55-bcb4-4e97-8cef-4250564d1f69")
# context = r"""show me all item with serial number which localisation is STOCK_RENNES in the dataset, bom col as item """
# prompt = """I have a complex data processing task. Please help me break it down into clear, logical steps.
# First, ummarize your understanding of what I want to do (in your own words).
# Then, list each step that should be performed in order.
# After that, we will go through each step one by one.
# Break it down into clear, sequential, and actionable steps.
# output only the steps you break down, no other text
# Task: {context}""".format(context=context)
# result = bllm.call(prompt)
# print(result)


#------------------------------------------------------------------------------------

#多表詢問(單一表)
# all_sheets = pd.read_excel("data/HUAWEI - Export inventaire GenateQ(1).xlsx", sheet_name=None)

# # 转换为 PandasAI DataFrame 并设置配置
# pai_dfs = pai.DataFrame(all_sheets['STOCK_TIBCO_HUAWEI'])
# pai_dfs._config = config

# # 第一次查询
# print("\n执行第一次查询...")
# response = pai_dfs.chat("show me all records which localisation is STOCK_CARVIN in the dataset")
# print_query_info(response)

# # 第二次查询
# print("\n执行第二次查询...")
# result = pai_dfs.chat('find the rest records Modèle is "02120110-SSEE1FAN" in the dataset')
# print_query_info(result)



#------------------------------------------------------------------------------------
#單一表持續詢問
# df_raw = pd.read_csv("data/TBC Lille.csv", encoding="latin1")
# # 然後轉成 pandasai 的 DataFrame
# df = pai.DataFrame(df_raw)


# response = df.chat('show me all item which "storage days" is more than 200 in the dataset')
# print("First query result:")
# print_query_info(response)
# print(response.value)

# df = pai.DataFrame(response.value)
# response2 = df.chat('find all records where hazardcategory equals "Normal Cargo"')
# # 使用第一次查询的结果进行第二次查询
# print("Second query result:")
# print_query_info(response2)


#------------------------------------------------------------------------------------























# Example usage
# if __name__ == "__main__":
#     agent = Agent()
#     file_path = "../../data/"
#     file_name = "TBC Lille.xlsx"
    
#     # Read the file
#     agent.readFile(file_path, file_name)
    
#     # Make a request
#     request = '''show me all the columns in the dataset'''
#     result = agent.llm.chat(request,*agent.df_list)
    
#     print(result)

# if __name__ == "__main__":
#     agent = Agent()

#     # 取得絕對路徑：從當前檔案往上兩層，再到 data 資料夾下的檔案
#     file_path = Path(__file__).resolve().parents[2] / "data" / "TBC Lille.xlsx"

#     # Debug：檢查檔案是否存在
#     if not file_path.exists():
#         print(f"❌ File not found: {file_path}")
#     else:
#         print(f"✅ Found file: {file_path}")

#         # Read the file
#         df = agent.readFile(str(file_path), "tbc")

#         # Make a request
      
#         # request = '''show me all the columns in the dataset'''
#         # result = agent.llm.chat(request, *agent.df_list)\
        
#         # llm.chat()

# #多文檔讀取操作

#         # Load existing datasets
#         # stocks = pai.load("organization/coca_cola_stock")

#         # # Query using multiple datasets 
#         # result = pai.chat("Compare the revenue between Coca Cola and Apple", stocks, companies)

# #与多个 DataFrame 聊天

#         # df_customers = pai.load("company/customers")
#         # df_orders = pai.load("company/orders")
#         # df_products = pai.load("company/products")

#         # response = pai.chat('Who are our top 5 customers and what products do they buy most frequently?', df_customers, df_orders, df_products)


#         myquery = '''show me all item which storage day is more than 200 days in the dataset'''
#         result = agent.llm.chat(myquery, *agent.df_list)
#         print(result)
#         myquery_2 = '''find all records where hazardcategory is "Non DG"'''
#         result = agent.llm.chat(myquery_2, *agent.df_list)

        
        

#         print(result)

# =====================
# 测试函数
# =====================
def test_read_single_table_for_create():
    """
    测试 read_single_table_for_create 函数，演示自动读取并创建数据集
    """
    test_file = "data\pre-load\总工单表-wy.xlsx"  # 请确保该文件存在
    test_path = "testorg/wy-ticket"
    test_description =   '''
    这是一个 工单记录表（Ticket Record Table），用于记录 OA 系统相关问题的处理信息。每一行代表一个用户提交的请求或问题的处理过程，包含分类、描述、解决方案、时间节点和用户反馈等信息。
'''
    test_columns = [
  { "name": "country", "type": "string" },
  { "name": "city", "type": "string" },
  { "name": "status", "type": "string" },
  { "name": "level_1_category", "type": "string" },
  { "name": "level_2_category", "type": "string" },
  { "name": "level_3_category", "type": "string" },
  { "name": "issue_description", "type": "string" },
  { "name": "solution", "type": "string" },
  { "name": "user_id_common", "type": "string" },
  { "name": "user_id_vip", "type": "string" },
  { "name": "creator", "type": "string" },
  { "name": "open_time", "type": "datetime" },
  { "name": "response_time", "type": "datetime" },
  { "name": "resolution_time", "type": "datetime" },
  { "name": "satisfaction", "type": "string" },
  { "name": "user_feedback", "type": "string" }
]   
    df = df.apply(lambda x: x.astype(str) if x.dtype == "object" else x)
    df = read_single_table_for_create(
        test_file,
        path=test_path,
        description=test_description,
        columns=test_columns
    )
    print("创建的数据集：", df)

test_read_single_table_for_create()