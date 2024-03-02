from langchain.prompts import PromptTemplate

def get_rag_prompt():
    template="""
    [INST]
    You are an ai assistant chatbot and your job is to answer the given question. you can look into the conext provided for additional infomation.
    If you don't have enough context just say "Insufficient  information". You are also required to keep the chat history between you and the user in mind.
    Don't let the user know that you are being provided with some context

    Context: {context}

    Question: {question}

    History: {history}

    [/INST]
    """
    prompt=PromptTemplate(
        input_variables=["context","question","history"],
        template=template
    )
    return prompt

def get_normal_prompt():
    prompt=PromptTemplate(
        input_variables=["question"],
        template="[INST] {question} [/INST]"
    )
    return prompt

def process_model_output(model,prompt):
    result=model.invoke(prompt)
    return result.split("[/INST]")[-1].strip()

def update_history(history,question:str,answer:str):
    return history+f"  \n**USER**: {question}  \n"+f"  \n**AI**: {answer}  \n"
