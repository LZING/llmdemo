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

    **评分标准：**

    1.  **可读性 (0-10):** 代码是否易于理解，变量和函数命名是否恰当，代码风格是否一致。请务必给出具体的理由，例如：
        - "命名清晰易懂，符合规范"
        - "代码风格一致，缩进合理"
        - "逻辑结构清晰，易于追踪"
    2.  **效率 (0-10):** 代码的时间复杂度和空间复杂度如何，是否存在性能瓶颈。请务必给出具体的理由，例如：
        - "使用了高效的算法和数据结构"
        - "避免了不必要的计算和内存占用"
        - "存在可以优化的部分，例如..."
    3.  **正确性 (0-10):** 代码是否能正确地完成预期的功能，是否经过充分测试。请务必给出具体的理由，例如：
        - "通过了所有测试用例"
        - "逻辑严谨，没有发现明显的错误"
        - "可能存在边界情况未处理"
    4.  **结构 (0-10):** 代码的组织结构是否清晰，模块划分是否合理，是否存在重复代码。请务必给出具体的理由，例如：
        - "模块划分清晰，职责明确"
        - "函数功能单一，易于复用"
        - "存在一些重复代码，可以进行重构"
    5.  **注释 (0-10):** 代码注释是否清晰、全面，能够解释代码的意图和功能。请务必给出具体的理由，例如：
        - "注释详细，解释了代码的意图"
        - "注释覆盖了关键部分，易于理解"
        - "注释不够全面，有些地方需要补充"
    6.  **可维护性 (0-10):** 代码是否易于理解和修改，是否遵循良好的编程实践。请务必给出具体的理由，例如：
        - "遵循了良好的编程规范，易于维护"
        - "代码结构清晰，修改方便"
        - "依赖关系复杂，修改困难"
    7.  **安全性 (0-10):** 代码是否存在安全漏洞或潜在风险，是否遵循了安全编程规范。请务必给出具体的理由，例如：
        - "没有发现明显的安全漏洞"
        - "遵循了安全编程规范，输入验证严格"
        - "存在潜在的SQL注入风险"
    8.  **规范性 (0-10):** 代码是否遵循编码规范和最佳实践，包括代码格式、命名约定等。请务必给出具体的理由，例如：
        - "遵循了PEP 8编码规范"
        - "命名规范一致，易于阅读"
        - "存在一些不规范的地方，例如..."

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
