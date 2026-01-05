import re

class CleanJsonOutput:
    def __init__(self,text):
        self.text=text
        
    def clean_json_output(self):
            self.text = re.sub(r"^```json|```$|^```|```$", "", self.text.strip(), flags=re.MULTILINE)
            self.text = re.sub(r"^'''json|'''$|^'''|'''$", "", self.text.strip(), flags=re.MULTILINE)

            # Remove markdown labels
            self.text = re.sub(r"^json\n", "", self.text.strip(), flags=re.IGNORECASE)

            # Extract the JSON object from large text
            match = re.search(r"\{.*\}", self.text, flags=re.DOTALL)
            if match:
                return match.group(0)
            return self.text