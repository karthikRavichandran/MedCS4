import os
from utils.utils import project_root_dir, load_fs_example
from utils.prompts import base_pt_level_1
from data.example_context import example_inf_cn,example_inf_conv

def read_fs_base_pt():
    few_shot_yaml_path_1 = os.path.abspath(os.path.join(project_root_dir,
                                                      'data',
                                                      'fs_example_1.yaml'))
    few_shot_yaml_path_2 = os.path.abspath(os.path.join(project_root_dir,
                                                      'data',
                                                      'fs_example_2.yaml'))
    FS1 = load_fs_example(yaml_path=few_shot_yaml_path_1)
    FS2 = load_fs_example(yaml_path=few_shot_yaml_path_2)

    fs_examples = [FS1, FS2]
    prompt_comp = {"base_pt": base_pt_level_1, "fs_examples": fs_examples}
    return prompt_comp

def get_few_shot_example_1():
    few_shot_cn_1 = '''This 77-year-old male patient was transferred to our 
    ICU 1 week after his COVID-19 diagnosis due to continuing respiratory decompensation 
    requiring intubation. Following the acute phase, with intermittent proning, 
    the patient continued to be hemodynamically unstable and was difficult to wean. 
    Rehabilitation proved challenging under these conditions, and physical therapists had 
    to reevaluate and adapt their interventions daily according to his condition. After 2 
    weeks, he was tracheotomized and started to improve very slowly. One week after 
    tracheostomy, the patient was able to speak for the first time after a cuff-down 
    trial and with the help of a speaking valve. But the patient spoke only a few words 
    with us and it was often difficult to involve him in exercises. Two days later, 
    he was able to communicate with his relatives via video telephony. This was a very 
    emotional moment for everyone involved, but it improved his communication and he was 
    able to express to his wife that he had no strength left to continue. However, 
    through the family’s active participation in his early rehabilitation process, 
    they were able to reinforce his confidence and motivation. He was discharged to a 
    rehabilitation clinic severely weak (MRC-SS 40/60) and functionally impaired (CPAx 
    22/50), but continued to progress in slow steps.'''

    fs_conv_1 = '''Doctor: Good morning, sir. How are you feeling today?
    
    Patient: Hmm, I'm feeling a bit weak.
    
    Doctor: I see. Can you tell me a bit about your medical history?
    
    Patient: Yes, I was diagnosed with COVID-19 about a week ago.
    
    Doctor: I see. And you were transferred to our ICU due to continuing respiratory 
    decompensation, correct?
    
    Patient: Yes, that's right.
    
    Doctor: And you required intubation?
    
    Patient: Yes, I did.
    
    Doctor: I see. And after the acute phase, you continued to be hemodynamically 
    unstable and it was difficult to wean you off the ventilator, correct?
    
    Patient: Yes, that's correct.
    
    Doctor: And rehabilitation was challenging under these conditions, correct?
    
    Patient: Yes, it was.
    
    Doctor: I see. And after 2 weeks, you underwent tracheostomy and started to improve 
    very slowly, correct?
    
    Patient: Yes, that's correct.
    
    Doctor: And one week after tracheostomy, you were able to speak for the first time 
    with the help of a speaking valve, correct?
    
    Patient: Yes, I was.
    
    Doctor: I see. And you spoke only a few words, correct?
    
    Patient: Yes, that's right.
    
    Doctor: And two days later, you were able to communicate with your relatives via 
    video telephony, correct?
    
    Patient: Yes, I was.
    
    Doctor: I see. And through the family's active participation in your early 
    rehabilitation process, they were able to reinforce your confidence and motivation, 
    correct?
    
    Patient: Yes, they did.
    
    Doctor: And you were discharged to a rehabilitation clinic severely weak, correct?
    
    Patient: Yes, I was.
    
    Doctor: I see. And your MRC-SS was 40/60 and your CPAx was 22/50, correct?
    
    Patient: Yes, that's correct.
    
    Doctor: I see. Well, you've made slow but steady progress. Keep up the good work!
    
    Patient: Thank you, doctor.'''

    fs_utterance_1 = '''1.Medical history -77 year old male diagnosed with COVID-19
    a week ago
    2. ICU transfer due to respiratory decomepnsation with
    intubation
    3. Patient suffered from rehabilitation challenges with unstableness
    and breath issues without ventilator support.
    4. 2 weeks later underwent tracheostomy and able to speak few words 1
    week later
    5. Communicated with relatives 2 days later via video telepathy
    6.Reinforced confidence with family participation in early rehabilitation process
    7. Discharged to rehabilitation clinic with weak (MRC-SS 40/60) and (CPAx 22/50)
    report
    8. Recovering slowly with baby steps'''

    fs_sentence_mapping_1 = '''1.transferred to ICU 1 week after COVID-19 diagnosis
    2.Due to continuing respiratory decompensation requiring
    intubation
    3.hemodynamically unstable and difficult to wean with rehabilitation
    4.Tracheotomized after 2 weeks with slow improvement
    5. Able to speak 1 week later with help of speaking valve
    6. improved his communication 2 days later via video telepathy
    with emotional moments
    7. Family active participation in early rehab process, reinforced confidence
    and motivation
    8. Discharged to rehabilitation clinic severly weak MRC-SS 40/60
    and CPAx(22/50) to progress in slow steps'''

    FS1 = {"few_shot_cn": few_shot_cn_1, "fs_conv_1":fs_conv_1,
           "fs_utterance":fs_utterance_1, "fs_sentence_mapping":fs_sentence_mapping_1}
    return FS1



def get_cs4_level_pt(prompt_comp, inf_cn, inf_conv):

    def gen_example():
        num_of_examples = len(prompt_comp['fs_examples'])
        prompt_construction = ''
        for itr, i in enumerate(prompt_comp['fs_examples']):
            prompt_construction = prompt_construction + f"Example {itr+1} \n"
            prompt_construction = prompt_construction + f"\t Full Clinical Note: \n{i['few_shot_cn']} \n"
            prompt_construction = prompt_construction + f"\t Conversation: \n{i['fs_conv']} \n"
            prompt_construction = prompt_construction + f"\t Utterances: \n{i['fs_utterance']} \n"
            prompt_construction = prompt_construction + f"\t Sentences Mapping: \n{i['fs_sentence_mapping']} \n\n"

        return prompt_construction



    final_exce_prompt = f'''{prompt_comp['base_pt']}
    
    {gen_example()}
    
    Full Clinical Note: {inf_cn}
    
    Conversation: {inf_conv}
    
    Utterances: YOUR ANSWER
    
    Sentences Mapping: YOUR ANSWER
    '''
    return final_exce_prompt

print(get_cs4_level_pt(prompt_comp=read_fs_base_pt(),
                       inf_cn=example_inf_cn,inf_conv=example_inf_conv))
