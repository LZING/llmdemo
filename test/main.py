# main.py
from agents import RecorderAgent, QuestionerAgent, AnalyzerAgent

from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_openai import ChatOpenAI
from config import openai_api_key, openai_base_url, model_name
import tempfile
from utils import clone_repository

# 定义 LLM
llm = ChatOpenAI(model_name=model_name, temperature=0.3, openai_api_key=openai_api_key, base_url=openai_base_url)
prompt_template = PromptTemplate(
    input_variables=["code"],
    template="""请根据以下标准对给定的代码进行评分，每项评分为 0 到 10 分，并给出评分的理由：

    **代码：**

    {code}

    ** testw **
    ** test **

    **请务必按照以下格式给出评分和理由：**

    1. 可读性：分数/理由
    2. 效率：分数/理由
    3. 正确性：分数/理由
    4. 结构：分数/理由
    5. 注释：分数/理由
    6. 可维护性：分数/理由
    7. 安全性：分数/理由
    8. 规范性：分数/理由
    """
)

llm_chain = LLMChain(llm=llm, prompt=prompt_template)

# 协作流程
def main():
    # root_dir = "D:\\code\\ai-analyse-repo"

    repo_url = input("请输入 Git 仓库 URL: ")
    with tempfile.TemporaryDirectory() as temp_dir:  # 创建临时目录
        if clone_repository(repo_url, temp_dir):
            # recorder = RecorderAgent()
            recorder = RecorderAgent(repo_url)  # 将 repo_url 传递给 RecorderAgent
            recorder.temp_dir = temp_dir  # 保存 temp_dir
            questioner = QuestionerAgent(temp_dir)
            analyzer = AnalyzerAgent(llm_chain)

            while True:
                file = questioner.get_next_file()
                if not file:
                    break
                print(f"正在分析文件: {file}")
                scores = analyzer.analyze_file(file)
                if scores is not None:
                    recorder.store_result(file, scores)

            report = recorder.generate_report()
            print("最终报告:\n", report)
        else:
            print("克隆仓库失败，请检查 URL 是否正确。")

    # recorder = RecorderAgent()
    # questioner = QuestionerAgent(root_dir)
    # analyzer = AnalyzerAgent(llm_chain)

    # while True:
    #     file = questioner.get_next_file()
    #     if not file:
    #         break
    #     print(f"正在分析文件: {file}")
    #     scores = analyzer.analyze_file(file)
    #     if scores is not None:
    #         print(f"文件 {file} 的评分: {scores}")
    #         # print(f"评分理由:\n{response}")
    #         recorder.store_result(file, scores)

    # 最终报告
    # recorder.generate_report()
    # print("最终报告:\n", report)

if __name__ == "__main__":
    main()
