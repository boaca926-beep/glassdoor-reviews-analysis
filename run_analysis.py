from langchain_ollama.llms import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

"""
    Pull LLM
"""
model_nm=["deepseek-r1:7b"]
model_indx = 0 # 0: deepseek-r1, 1: llama3.2
#model = OllamaLLM(model=model_nm[model_indx])
model = OllamaLLM(model="llama3.2")

print(f"LLM {model_nm[model_indx]} pulled succuessful!")

template = """
We are asking questions about company reviews

Here are some relevant reviews: {reviews}

Heare is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model # Pass prompt {reviews} and {questions} to LLM

while True:
    print("\n\n----------------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n----------------------------------------")

    if question == "q":
        print("Welcome back whenever you have a question ...")
        break

    reviews = retriever.invoke(question)
    result = chain.invoke({"reviews": reviews, "question": question})
    print(result)

