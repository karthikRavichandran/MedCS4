import json
'''
TODO 
from evaluation.llm_judge import LLMJudge
from evaluation.metrics import compute_metrics
from utils.io import load_data, save_results
from runner.single_turn import run_single_turn
from runner.multi_turn import run_multi_turn
from utils.flowchart import generate_multi_turn_flow
 '''

from utils.utils import client
from utils.prompts import get_CQAD_prompt, CQAD_system_prompt
from data.example_context import example_inf_cn,example_inf_conv, context1
from prompts.level1_prompts import get_cs4_level_pt,read_fs_base_pt
from runner.llm_runner import llm_runner
from runner.llm_as_a_judge import generate_llm_judge_prompt, judge_llm_runner
import json


def llm(clinical_note, conversation):
    prompt = get_cs4_level_pt(prompt_comp=read_fs_base_pt(),
                              inf_cn=clinical_note, inf_conv=conversation)
    llm_out = llm_runner(model='gpt-4.1-mini',
                         system_pt="You're any Medical assistant to generate data",
                         user_pt=prompt)
    dict_llm_out = json.loads(llm_out)
    return dict_llm_out


def judge(clinical_note, conversation, dict_llm_out):
    system_judge_prompt, user_judge_prompt = generate_llm_judge_prompt(
        clinical_note=clinical_note,
        conversation=conversation,
        utterance=dict_llm_out['utterances'],
        mapped_sentence=dict_llm_out['mapped_sentences'])

    # gpt-4.1-mini
    judge_llm_out = judge_llm_runner(model='gpt-4.1-mini',
                                     system_pt=system_judge_prompt,
                                     user_pt=user_judge_prompt)
    return judge_llm_out


if __name__=="__main__":
    # api_key_and_run_tester()

    clinical_note, conversation = (example_inf_cn,example_inf_conv)
    dict_llm_out = llm(clinical_note, conversation)
    judge_llm_out = judge(clinical_note, conversation, dict_llm_out)




    # print(llm_out)
    print(judge_llm_out)
