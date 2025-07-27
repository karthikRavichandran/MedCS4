from utils.utils import client, retry_on_exception, logging
def generate_llm_judge_prompt(clinical_note, conversation, utterance, mapped_sentence):
    system_prompt = """You are a clinical evaluation expert. Your role is to judge the quality of 
    utterance-to-clinical-note sentence mappings using defined clinical reasoning 
    metrics.
For each mapping, evaluate based on:
1. Clinical Relevance (0–2): How meaningful is the utterance clinically?
2. Semantic Accuracy (0–3): How closely does the meaning of the utterance match the mapped sentence(s)?
3. Completeness (0–2): Does the utterance capture all relevant information from the sentence(s)?
4. Mapping Precision (0–1): Are the mapped sentence(s) appropriate and specific?

Provide a total score out of 8 and a brief justification. Output your answer in the structured format shown in the instructions.
"""

    user_prompt = f"""
You are given the following data:

Clinical Note:
\"\"\"{clinical_note}\"\"\"

Conversation:
\"\"\"{conversation}\"\"\"

Utterance:
\"\"\"{utterance}\"\"\"

Mapped Sentence(s):
\"\"\"{mapped_sentence}\"\"\"

Evaluate this utterance-to-sentence mapping based on the metrics below. Use this format in your response:

Utterance: "<...>"
Mapped Sentence(s): "<...>"

Clinical Relevance: X/2
Semantic Accuracy: X/3
Completeness: X/2
Mapping Precision: X/1

Total Score: X/8

Justification:
- <Explain reasoning for each score>

Output all the metrics and justification in json format. Only return json without json keyword
"""

    return system_prompt, user_prompt
@retry_on_exception(max_retries=5, delay=2, logger=logging)
def judge_llm_runner(model="gpt-4o-mini", system_pt=None, user_pt=None):
    print(f"Running Model API call {model} for LLM-as-a-judge...")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # claude-3-haiku-20240307
        messages=[
            {"role": "system", "content": system_pt},
            {"role": "user", "content": user_pt}
        ]
    )
    return completion.choices[0].message.content