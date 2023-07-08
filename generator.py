import os
import pandas as pd
from dotenv import load_dotenv
from gpt import GPT
import smtplib, ssl
from email.message import EmailMessage




load_dotenv()

class Generator:
    def __init__(self) -> None:
        self.participant_id = None

    def send_email(self, content, to):

        msg = EmailMessage()
        msg['Subject'] = f"Agents of BOB for participant: {self.participant_id}"
        msg['From'] = "agents@bob.ai"
        msg['To'] = to
        msg.set_content(f"""
        Welcome participant to the Masquerade ball, here is your BOB AI character summary from what you provided us with:

        {content}

        Thank you very much for your participation in the Masquerade Ball

        Agents of BOB
        """)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(os.environ.get("SMTP_HOST"), os.environ.get("SMTP_PORT"), context=context) as server:
            server.login(os.environ.get("SMTP_LOGIN"), os.environ.get("SMTP_PASSWORD"))
            server.send_message(msg)
        
    def get_participant_ID(self):
        participantID = input("Participant ID: ")
        self.participant_id = participantID
        self.gpt = GPT(self.participant_id)

    def generate_summary(self):
        anwser = ""
        while anwser.lower() not in ["y", "n"]:
            anwser = input("Generate Summary? [Y/n]")
            if not anwser:
                anwser = "y"
        if anwser.lower() == "y":
            return True
        else:
            return False

    def generate_character_summary(self):
        result = self.gpt.generate_character_summary()
        f = open(f"{self.participant_id}-character_summary.txt", 'w')
        f.write(result)
        f.close()
        return result

    def generate_sygil_data(self, summary):
        result = self.gpt.generate_sygil_data(summary)
        f = open(f"{self.participant_id}-sygil_data.txt", 'w')
        f.write(result)
        f.close()
        return result

    def run(self):
        self.generate_summary()
        os.system('cls' if os.name == 'nt' else 'clear')

        self.get_participant_ID()

        summary = self.generate_character_summary()
        print("=========================================================")
        print("The character's summary is: \n", summary)

        sygil = self.generate_sygil_data(summary)
        self.send_email(sygil, os.environ.get("SYGIL_ADDRESS"))

        print("=========================================================")
        print("The character's sygil is: \n", sygil)
        
        self.send_email(summary, os.environ.get("MASTER_ADDRESS"))
        if self.gpt.participant_email:
            self.send_email(summary, self.gpt.participant_email)


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        G = Generator()
        G.run()