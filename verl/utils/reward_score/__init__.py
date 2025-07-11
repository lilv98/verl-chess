# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# from . import gsm8k, math, prime_math, prime_code
# from . import chess_piece, chess_legal


import re
import random

def extract_solution(solution_str):

    answer_pattern = r'<answer>(.*?)</answer>'
    match = re.finditer(answer_pattern, solution_str)
    matches = list(match)
    if matches:
        final_answer = matches[-1].group(1).strip()
    else:
        final_answer = None
    return final_answer


def compute_score_1_in_n(solution_str, ground_truth, method="strict", format_score=0.0, score=1.0):
    
    answer = extract_solution(solution_str=solution_str)
    
    if answer is None:
        return 0
    else:
        if answer in ground_truth['ground_truth'].split(' '):
            return score
        else:
            return format_score


def compute_score_set_match(solution_str, ground_truth, method="strict", format_score=0.0, score=1.0):
    
    answer = extract_solution(solution_str=solution_str)
    
    if answer is None:
        return 0
    else:
        if set(answer.split(', ')) == set(ground_truth['ground_truth'].split(' ')):
            return score
        else:
            return format_score


def compute_score_exact_match(solution_str, ground_truth, method="strict", format_score=0.0, score=1.0):
    
    answer = extract_solution(solution_str=solution_str)
    
    if answer is None:
        return 0
    else:
        if answer == ground_truth['ground_truth']:
            return score
        else:
            return format_score


def _default_compute_score(data_source, solution_str, ground_truth, extra_info=None):
    
    do_print = random.randint(1, 256) == 1
    if do_print:
        print("-------------------------")
        print(f"Predicted: {solution_str} | GT: {ground_truth['ground_truth']}")
        print(f"Solution: {solution_str}")
    
    if data_source in ["chess_legal_any_train", 
                       "chess_legal_any_test"]:
        res = compute_score_1_in_n(solution_str, ground_truth)
    elif data_source in ["chess_legal_all_train", 
                         "chess_legal_all_test"]:
        res = compute_score_set_match(solution_str, ground_truth)
    elif data_source in [
                        "chess_legal_left_train",
                        "chess_legal_left_test",
                        "chess_best_wo_train",
                        "chess_best_wo_test",
                        "chess_best_w_train",
                        "chess_best_w_test",
                        "chess_piece_train",
                        "chess_piece_test",
                        "chess_matein1_wo_train",
                        "chess_matein1_wo_test",
                        "chess_matein1_w_train",
                        "chess_matein1_w_test",
                        ]:
        res = compute_score_exact_match(solution_str, ground_truth)
    else:
        raise NotImplementedError(f"Reward function is not implemented for {data_source=}")
    
    # if data_source == "openai/gsm8k":
    #     from . import gsm8k

    #     res = gsm8k.compute_score(solution_str, ground_truth)
    # elif data_source in ["lighteval/MATH", "DigitalLearningGmbH/MATH-lighteval"]:
    #     from . import math

    #     res = math.compute_score(solution_str, ground_truth)
    #     # [Optional] Math-Verify Integration
    #     # For enhanced accuracy, consider utilizing Math-Verify (https://github.com/huggingface/Math-Verify).
    #     # Note: Math-Verify needs to be manually installed via pip: `pip install math-verify`.
    #     # To use it, override the `compute_score` function with the following implementation:

    #     # from . import math_verify
    #     # res = math_verify.compute_score(solution_str, ground_truth)
    # elif data_source == "math_dapo" or data_source.startswith("aime"):
    #     from . import math_dapo

    #     res = math_dapo.compute_score(solution_str, ground_truth)
    # elif data_source in [
    #     "numina_aops_forum",
    #     "numina_synthetic_math",
    #     "numina_amc_aime",
    #     "numina_synthetic_amc",
    #     "numina_cn_k12",
    #     "numina_olympiads",
    # ]:
    #     from . import prime_math

    #     res = prime_math.compute_score(solution_str, ground_truth)
    # elif data_source in ["codecontests", "apps", "codeforces", "taco"]:
    #     from . import prime_code

    #     res = prime_code.compute_score(solution_str, ground_truth, continuous=True)
    # elif data_source in ["hiyouga/geometry3k"]:
    #     from . import geo3k

    #     res = geo3k.compute_score(solution_str, ground_truth)
        
    # elif data_source == "chess_piece_train":
        
    #     res = chess_piece.compute_score_train(solution_str, ground_truth)
    
    # elif data_source == "chess_piece_test":
        
    #     res = chess_piece.compute_score_test(solution_str, ground_truth)
        
    # elif data_source == "chess_legal_train":
        
    #     res = chess_legal.compute_score_train(solution_str, ground_truth)
    
    # elif data_source == "chess_legal_test":
        
    #     res = chess_legal.compute_score_test(solution_str, ground_truth)
    
    # else:
    #     raise NotImplementedError(f"Reward function is not implemented for {data_source=}")

    if isinstance(res, dict):
        return res
    elif isinstance(res, (int, float, bool)):
        return float(res)
    else:
        return float(res[0])
