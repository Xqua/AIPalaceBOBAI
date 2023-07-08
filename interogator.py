import pandas as pd
import os
from gpt import GPT

class Interogator:
    def __init__(self) -> None:
        self.participantID = None
        self.QA = []

    def get_emptyQA(self):
        return ()

    def begin_interogation(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        anwser = ""
        while anwser.lower() not in ["y", "n"]:
            anwser = input("Being interogation ? [Y/n]")
            if not anwser:
                anwser = "Y"
        if anwser.lower() == "y":
            return True
        else:
            return False
        
    def get_participant_ID(self):
        self.participantID = input("Participant ID: ")
        self.gpt = GPT(self.participantID)

    def get_question_anwser(self):
        question = input("Question: ")
        anwser = input("Anwser: ")
        qa = {
            "question": question,
            "anwser": anwser
        }
        self.QA.append(qa)
    
    def get_survey_summary(self):
        result = self.gpt.generate_intermediate_summary()
        return result

    def end_interogation(self):
        anwser = ""
        while anwser.lower() not in ["y", "n"]:
            anwser = input("End interogation? [y/N]")
            if not anwser:
                anwser = "n"
        if anwser.lower() == "y":
            return True
        else:
            return False
    
    def save_data(self):
        df = pd.DataFrame().from_dict(self.QA)
        df.to_csv(f"{self.participantID}.csv", index=False)
    
    def run(self):
        self.begin_interogation()
        self.get_participant_ID()
        summary = self.get_survey_summary()
        print(f"BOB says: \n", summary)
        self.get_question_anwser()
        while not self.end_interogation():
            self.get_question_anwser()
        self.save_data()

if __name__ == '__main__':
    while True:
        I = Interogator()
        I.run()