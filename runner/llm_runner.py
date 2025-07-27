from utils.utils import client, retry_on_exception, logging
from utils.prompts import get_CQAD_prompt, CQAD_system_prompt
from data.example_context import example_inf_cn, example_inf_conv, context1


def api_key_and_run_tester():
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # claude-3-haiku-20240307
        messages=[
            {"role": "system", "content": CQAD_system_prompt},
            {"role": "user", "content": get_CQAD_prompt(context1)}
        ]
    )
    print(completion.choices[0].message.content)

@retry_on_exception(max_retries=5, delay=2, logger=logging)
def llm_runner(model="gpt-4o-mini", system_pt=None, user_pt=None):
    print(f"Running Model API call {model} Generation...")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # claude-3-haiku-20240307
        messages=[
            {"role": "system", "content": system_pt},
            {"role": "user", "content": user_pt}
        ]
    )
    return completion.choices[0].message.content
