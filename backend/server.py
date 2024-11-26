from flask import Flask, request, jsonify
import openai
import re
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
# openai.api_key = API_KEY
# llama3.1 connection
openai.api_key = "sk-"
openai.api_base = "http://localhost:11434/v1"


def generate_collaboration_prompt(user_message, current_code, chat_history=None):
    prompt = f"""
    You are a helpful coding assistant collaborating with a user to create or refine code. Your responses should be clear, informative, and help the user achieve their goals efficiently.

    Here is the current context:

 
    """
    if current_code:
        prompt += f""" Current Code:
    ```Observe the following {current_code} faulty code which is complete with no extra context. Your task is to fix the code.
    ```
    """
        prompt += f"""

        User Message:
        {user_message}
        If you have suggestions for best practices or additional improvements, include them in the Explanation.
        Before writing your final answer, carefully analyze the code step by step to identify any bugs or errors and determine how to fix them. carefully read the code you fixed before and check if there is still any issue.  Do not include this analysis in your final response.
        Your final response should:
        - Provide the fixed code enclosed within <code></code> tags.
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
