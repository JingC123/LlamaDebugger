from flask import Flask, request, jsonify
import openai
import re
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
# GPT connection, add your api key below
# openai.api_key = ""

# llama3.1 connection
openai.api_key = "EMPTY"
openai.api_base = "http://localhost:11434/v1"


def generate_collaboration_prompt(user_message, current_code, chat_history=None):
    prompt = f"""
    You are a helpful coding assistant collaborating with a user to generate or refine code. Your responses should be clear,\n 
    informative, and help the user achieve their goals efficiently.
    ``` Look the example of debugging Q&A, which may help you undetstand how to debug.

    Q: I am having trouble understanding this code. Can you explain what this code is trying to do? I also noticed that the return statement is empty. 
    What should I return as the output of this function? Lastly, can you explain the purpose of the variables 'start' and 'max_length'? 
    Here is my code: ```python def longest_palindromic_substring(s: str) -> str: n = len(s) if n == 0: return "" start, max_length = 0, 1 for i in range(n): l, 
    r = i, i while r < n - 1 and s[r] == s[r + 1]: r += 1 i = r while l > 0 and r < n - 1 and s[l - 1] == s[r + 1]: l -= 1 r += 1 length = r - l + 1 
    if length > max_length: start, max_length = l, length return s[start:start + max_length] ```
    
    A: Sure, I would be happy to help. First, let me explain what the code is trying to do. The function `longest_palindromic_substring` takes a string `s` as input and 
    returns the longest palindromic substring in `s`. A palindromic string is a string that reads the same backward as forward, for example, "racecar" is a palindromic string. 
    The function works by iterating through each character in the string `s` and checking whether there is a palindromic string that starts with that character. 
    To do this, it checks whether there are any palindromes that are centered around that character. If there are, it updates the `start` and `max_length` variables to 
    keep track of the longest palindromic substring seen so far. Now, let's move on to the bugs in the code. The first bug is on line 3, where the function returns nothing 
    if the length of the input string `s` is 0. This is problematic because the function is expected to return a string value. We can fix this by changing the return statement 
    to `return ""` so that the function returns an empty string if the input string is empty. The second bug is on line 22, where the function returns nothing after performing 
    all the necessary computations. This is also problematic because the function is expected to return the longest palindromic substring as a string value. We can fix this by 
    changing the return statement to `return s[start:start + max_length]` so that the function returns the longest palindromic substring. Finally, the purpose of 
    the `start` and `max_length` variables is to keep track of the starting index and length of the longest palindromic substring seen so far. The `start` variable is 
    initially set to 0, and the `max_length` variable is initially set to 1. These values are updated whenever a longer palindromic substring is found. 
    To summarize, the bugs in the code are related to the return statements, and we can fix them by changing them to return the appropriate string values. 
    The purpose of the `start` and `max_length` variables is to keep track of the longest palindromic substring seen so far. Here is the corrected code: 
    ```python def longest_palindromic_substring(s: str) -> str: n = len(s) if n == 0: return "" start, max_length = 0, 1 for i in range(n): l, r = i, i 
    while r < n - 1 and s[r] == s[r + 1]: r += 1 i = r while l > 0 and r < n - 1 and s[l - 1] == s[r + 1]: l -= 1 r += 1 length = r - l + 1 if length > max_length: 
    start, max_length = l, length return s[start:start + max_length] ```

    ```Here is the current context:
    """
    if current_code:
        prompt += f"""
    
    Current Code:
    ```Observe the following {current_code} faulty code which is complete with no extra context. Your task is to fix the code.
    ```
    """
        prompt += f"""

        User Message:
        {user_message}
        If you have suggestions for best practices or additional improvements, include them in the Explanation.
        Before writing your final answer, carefully analyze the code step by step to identify any bugs or errors and determine how to fix them.\n 
        carefully read the code you fixed before and check if there is still any issue.  Do not include this analysis in your final response.
        Your final response should:
        - Provide the fixed code, enclosed all the code within <code></code> tags.
        - Provide some comments you modified and give reason for that.
        - Include a short explanation conclude that the issue of the code and your modification, enclosed within <exp></exp> tags.
        - Do not write anything else besides the code and the explanation within the specified tags.
        Your reply should be formatted as follows:
        <code>
        [Your fixed code here]
        </code>
        <exp>
        [Your short explanation here]
        </exp>

        """
    else:
        prompt += "No current code provided."
        prompt += f"""

        User Message:
        {user_message}
        """


    return prompt


def parse_response(response):
    # Split response into Explanation and Code Section based on structured format
    explanation = ""
    code_section = ""

    code_section = response[response.find('<code>') + len('<code>'):response.find('</code>')]
    explanation = response[response.find('<exp>') + len('<exp>'):response.find('</exp>')]
    

    return explanation, code_section

@app.route('/hello', methods=['GET'])
def hello_world():
    return "Hello, World!"

@app.route('/api/code-collaboration', methods=['POST'])
def code_collaboration():
    data = request.get_json() or {}
    current_code = data.get('current_code', '')
    user_message = data.get('user_message', '')

    prompt = generate_collaboration_prompt(user_message, current_code)

    try:
        response = openai.ChatCompletion.create(
            # model="gpt-4o",
            model='llama3.1',
            messages=[{"role": "user", "content": prompt}]
        )
        response_text = response.choices[0].message.content
        print('response text', response_text)
        explanation, code_section = parse_response(response_text)
        return jsonify({"response_text": response_text, "user_message": user_message, "explanation": explanation, "code_section": code_section})
    except Exception as e:
        print(f"error: {str(e)}")
        return jsonify({"error": str(e)}), 500



@app.route('/api/reset', methods=['POST'])
def reset_code():
    return jsonify({"result": ""})


if __name__ == '__main__':
    app.run(debug=True)
