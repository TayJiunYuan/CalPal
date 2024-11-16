# import os
# from langchain.schema.messages import HumanMessage, SystemMessage
# from langchain_openai import ChatOpenAI
# from langchain.output_parsers.json import SimpleJsonOutputParser
# from dotenv import load_dotenv
# from datetime import date

# class OpenAIService:
#     def __init__(self, OPEN_API_KEY):
#         load_dotenv()
#         self.OPEN_API_KEY = OPEN_API_KEY
#         self.chat = ChatOpenAI(api_key=self.OPEN_API_KEY)
#         self.output_parser = SimpleJsonOutputParser()
#         self.current_date = date.today()
#         self.system_message = (
#             "You are a calendar chatbot called CalPal. Parse the user input into a suitable JSON object. "
#             "If the user does not give you the information you need, you should ask for more info. "
#             "You can only do the functions listed below. Anything else, please tell the user it's not possible. "
#             f"Today's date is {self.current_date}. "
#             "If the user wants to add an event, return an object with 'action': 'add', 'event_name', and 'event_date' in format yyyy-mm-dd. "
#             "If the user wants to view a day of events, return an object with 'action':'view_day', 'event_date' in format yyyy-mm-dd. "
#             "If the user wants to view a month of events, return an object with 'action':'view_month', 'event_month' in format yyyy-mm. "
#             "If more info is needed, return an object with 'action': 'prompt', 'message': the message to ask the user for more info. "
#         )

#     def get_response(self, user_input):
#         messages = [
#             SystemMessage(content=self.system_message),
#             HumanMessage(content=user_input),
#         ]
#         response = self.chat.invoke(messages)
#         parsed_response = self.output_parser.parse(response.content)
#         return parsed_response

import os
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.output_parsers.json import SimpleJsonOutputParser
from dotenv import load_dotenv
from datetime import date
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_openai import ChatOpenAI

class OpenAIService:
    def __init__(self, OPEN_API_KEY):
        load_dotenv()
        self.OPEN_API_KEY = OPEN_API_KEY
        self.llm = ChatOpenAI(api_key=self.OPEN_API_KEY)
        self.output_parser = SimpleJsonOutputParser()
        self.current_date = date.today()
        self.system_message = (
            "You are a calendar chatbot called CalPal. Parse the user input into a suitable JSON object. "
            "If the user does not give you the information you need, you should ask for more info. "
            "You can only do the functions listed below. Anything else, please tell the user it's not possible. "
            f"Today's date is {self.current_date}. "
            "If the user wants to ask for the possible commands or needs help, return an object with 'action': 'help' "
            "If the user wants to add an event, return an object with 'action': 'add', 'event_name', and 'event_date' in format yyyy-mm-dd. "
            "If the user wants to view a day of events, return an object with 'action':'view_day', 'event_date' in format yyyy-mm-dd. "
            "If the user wants to view a month of events, return an object with 'action':'view_month', 'event_month' in format yyyy-mm. "
            "If more info is needed, return an object with 'action': 'prompt', 'message': the message to ask the user for more info. "
        )

    def get_response(self, user_input):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=self.system_message
                ),  # The persistent system prompt
                MessagesPlaceholder(
                    variable_name="chat_history"
                ),  # Where the memory will be stored.
                HumanMessagePromptTemplate.from_template(
                    "{human_input}"
                ),  # Where the human input will injected
            ]
        )
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        chat_llm_chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            verbose=True,
            memory=memory,
        )
        response = chat_llm_chain.predict(human_input=user_input)
        print(response)
        parsed_response = self.output_parser.parse(response)
        return parsed_response
