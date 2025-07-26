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




if __name__=="__main__":
    # api_key_and_run_tester()

    prompt = get_cs4_level_pt(prompt_comp=read_fs_base_pt(),
                     inf_cn=example_inf_cn, inf_conv=example_inf_conv)
    llm_out = llm_runner(system_pt="You're any Medical assistant to generate data",
               user_pt=prompt)
    print(llm_out)
