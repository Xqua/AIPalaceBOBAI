import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

import openai
openai.api_key = os.environ.get("OPENAI_API_KEY")

class GPT:
    def __init__(self, participant_id) -> None:
        self.participant_id = participant_id
        self.participant_email = None
        self.sheet_id = os.environ.get("SHEET_ID", None)

        # Prompts
        self.system_prompt = open("./prompts/system_prompt.txt").read()
        self.form_data_questions = open("./prompts/form_data_prompt.txt").read()
        self.form_data_prompt = open("./prompts/form_data_prompt.txt").read()
        self.interogration_data_prompt = open("./prompts/interogration_data_prompt.txt").read()
        self.intermediate_prompt = open("./prompts/intermediate_prompt.txt").read()
        self.character_summary_prompt = open("./prompts/character_summary_prompt.txt").read()
        self.sygil_prompt = open("./prompts/sygil_prompt.txt").read()
        
        # Data
        self.form_data = self.read_form_data()
        try:
            self.interogation_data = self.read_interogation_data()
        except:
            self.interogation_data = pd.DataFrame(columns=["question", "anwser"])

    def read_form_data(self):
        url = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=csv"
        form_data = pd.read_csv(url)
        form_data = form_data[form_data["Identification Card Number"] == int(self.participant_id)]
        return form_data

    def read_interogation_data(self):
        interogation_data = pd.read_csv(f"./{self.participant_id}.csv")
        return interogation_data

    def format_form_data_prompt(self):
        prompt = self.form_data_prompt
        for column in self.form_data.columns:
            if column not in ["Timestamp", "Email Address"]:
                anwser = self.form_data[column].values[0]
                prompt += f"""
                question: {column}
                anwser: {anwser}
                """
            if column == "Email Address":
                self.participant_email = self.form_data[column].values[0]
        return prompt

    def format_interogation_prompt(self):
        prompt = self.interogration_data_prompt
        for question, answer in self.interogation_data.values:
            prompt += f"""
            question: {question}
            anwser: {answer}
            """
        return prompt
    
    def format_intermediate_prompt(self):
        form_data_prompt = self.format_form_data_prompt()
        prompt = f"""
        {self.system_prompt}
        {form_data_prompt}
        """
        return prompt

    def format_final_prompt(self):
        form_data_prompt = self.format_form_data_prompt()
        interogation_data_promp = self.format_interogation_prompt()
        prompt = f"""
        {self.system_prompt}
        {form_data_prompt}
        {interogation_data_promp}
        """
        return prompt

    def generate_intermediate_summary(self):
        system_prompt = self.format_intermediate_prompt()
        user_prompt = self.intermediate_prompt
        result = self.generate_from_GPT(system_prompt, user_prompt)
        return result 

    def generate_character_summary(self):
        system_prompt = self.format_intermediate_prompt()
        user_prompt = self.character_summary_prompt
        result = self.generate_from_GPT(system_prompt, user_prompt)
        return result

    def generate_sygil_data(self, summary):
        system_prompt = self.format_intermediate_prompt()
        user_prompt = f"""
            This is the character summary: 
            {summary}

            {self.sygil_prompt}
        """
        result = self.generate_from_GPT(system_prompt, user_prompt)
        return result

    def generate_from_GPT(self, system_prompt, user_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
            ]
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=0)
        result = chat_completion['choices'][0]['message']['content']
        return result
        
