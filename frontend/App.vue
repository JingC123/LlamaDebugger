<script setup lang="jsx">
import { ref, nextTick, onMounted } from 'vue';
import { Codemirror } from "vue-codemirror";
import { javascript } from "@codemirror/lang-javascript";
import { python } from "@codemirror/lang-python";
import { oneDark } from "@codemirror/theme-one-dark";
import { EditorView } from "@codemirror/view";
import { SystemCodeIcon } from 'tdesign-icons-vue-next';
import { codeCollaboration, quickAction } from './apiservice'; // 导入API请求函数

const content = ref('');
const BTN_TEXT = 'Submit 🚀';
const res = ref('🔍 Ask me any code you want to check or polish! \n');
const customTheme = EditorView.theme({
  '&': {
    backgroundColor: 'white',
    borderRadius: '8px',
    border: '1px solid #ddd',
  },
  '.cm-content': {
    fontFamily: 'monospace',
    fontSize: '14px',
    color: 'black',
  },
});

const lastPrompt = ref('');

const btnText = ref(BTN_TEXT);
const code = ref(`# please input your code here!`);
const extensions = [customTheme, python()];

function sleep(milliseconds) {
  return new Promise(resolve => setTimeout(resolve, milliseconds));
}

const searchKeyword = async () => {
  btnText.value = 'Generating Code... 🔍';

  const userMessages = [
    {
      role: 'system',
      content: `Observe the following faulty code which is complete with no extra context. Your task is to fix up the code and polish the coding style and explain on the modification.
You have to write the fixed code again. Do not write anything else in your response. Your reply should be like this:
Fixed Code:
here is your fixed code

Feedback:
short explanation about the bug and the coding style`
    },
    { role: 'user', content: content.value }
  ];

  

  const requestData = {
    model: 'gpt-4o', // Corrected model name
    messages: userMessages,
  };

  const fetchOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${import.meta.env.VITE_OPEN_API_KEY}`,
    },
    body: JSON.stringify(requestData),
  };

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', fetchOptions);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Error:', errorText);
      btnText.value = BTN_TEXT;
      return;
    }

    const jsonResponse = await response.json();
    const payload = jsonResponse.choices[0].message.content.trim();
    console.log('Assistant:', payload);
    
    res.value = payload;
  } catch (error) {
    console.error('Error:', error);
  } finally {
    btnText.value = BTN_TEXT;
  }
};

// 新增用于调用 codeCollaboration API 的方法
const handleCodeCollaboration = async () => {
  const userMessage = content.value;
  const currentCode = code.value;
  btnText.value = 'Fixing Code... 🔍';

  try {
    const result = await codeCollaboration(userMessage, currentCode);
    console.log('Code Collaboration Result:', result);
    lastPrompt.value = result.user_message
    code.value = result.code_section
    res.value = result.explanation
    content.value = ""
  } catch (error) {
    console.error('Error in handleCodeCollaboration:', error);
  } finally {
    btnText.value = BTN_TEXT;
  }
};

</script>

<template>
  <h2>🤖️ LlamaDebugger</h2>
  <div class="container">
    <div class="chat">
      <div class="dialogue">
        <div class="card-last-prompt" v-if="lastPrompt.value !== '' ">
          <pre>{{ lastPrompt }}</pre>
        </div>
        <div class="response-box">
          <t-avatar class="avatar"><SystemCodeIcon></SystemCodeIcon></t-avatar>
          <div class="card-result">
            <pre>{{ res }}</pre>
          </div>
        </div>
        
      </div>
      
      <div class="input-box">
        <textarea
          class="input"
          placeholder="Fix code for me...🌽"
          v-model="content">
        </textarea>
        <div class="button-block">
          <button type="button" @click="handleCodeCollaboration" class="btn">
            <strong>{{ btnText }}</strong>
            <div id="container-stars">
              <div id="stars"></div>
            </div>
            <div id="glow">
              <div class="circle"></div>
              <div class="circle"></div>
            </div>
          </button>
        </div>
      </div>
    </div>
    <div class="right">
      <codemirror v-model="code" placeholder="Code gose here..." :style="{ height: '100%'}" :autofocus="true"
          :tabSize="3" :extensions="extensions" />
    </div>
  </div>
</template>




<style scoped>

.custom-codemirror .cm-editor {
  border-radius: 8px; /* 设置圆角 */
  background-color: white; /* 背景色为白色 */
  border: 1px solid #ddd; /* 添加边框颜色（可选） */
  padding: 10px; /* 内边距，让内容不贴边（可选） */
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* 可选的阴影效果 */
}

/* 设置代码区域的背景色和文字颜色 */
.custom-codemirror .cm-content {
  background-color: white;
  color: black; /* 设置文字颜色 */
  border-radius: inherit; /* 继承容器的圆角 */
}

.avatar{
  margin: 1rem 0px;
}
.input-box{
  display: flex;
  align-items: center;
  width: calc(100% - 20px);
  /* min-height: 150px; Set a reasonable height for code snippets */
  max-height: 200px; /* Set a reasonable height for code snippets */
  padding: 12px;
  border: none;
  border-radius: 16px;
  box-shadow: 2px 2px 7px 0 rgba(0, 0, 0, 0.2);
  outline: none;
  font-size: 16px;
  resize: none; /* Allow users to resize the textarea vertically */
  font-family: 'Courier New', Courier, monospace; /* Use monospace font for code */
  line-height: 1.5; /* Improve readability */
  overflow: auto; /* Add scrollbars if content overflows */
  bottom: 10px;
}

h1 {
  margin-bottom: 64px;
}

.dialogue{
  display: flex;
  flex-direction: column;
  height: 500px;
  overflow: scroll;
  scrollbar-width: none;

}

.response-box{
  display: flex;
}

.container{
  display: flex;
  width: 100%;
  height: 80%;
  box-sizing: border-box;
}
.chat{
  width: 40%;
  /* height: 100%; */
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.output-container{
  background-color: #d9dadb;
  padding: 5px 5px 5px 5px;
}

.right{
  width: 55%;
  height: 100%;
  margin-left: 5%;
}

.input { 
  width: calc(100% - 128px);
  /* min-height: 150px; Set a reasonable height for code snippets */
  max-height: 200px; /* Set a reasonable height for code snippets */
  padding: 12px;
  border: none;
  outline: none;
  font-size: 16px;
  resize:none;
  font-family: 'Courier New', Courier, monospace; /* Use monospace font for code */
  line-height: 1.5; /* Improve readability */
  overflow: auto; /* Add scrollbars if content overflows */
  bottom: 10px;

}


.input:invalid {
  animation: justshake 0.3s forwards;
  color: red;
}

@keyframes justshake {
  25% {
    transform: translateX(5px);
  }
  50% {
    transform: translateX(-5px);
  }

  75% {
    transform: translateX(5px);
  }

  100% {
    transform: translateX-(5px);
  }
}

button {
  cursor: pointer;
  height: 32px;
  font-size: 16px;
  /* margin-top: 24px; */
  background: royalblue;
  color: white;
  padding: 0.7em 1em;
  padding-left: 0.9em;
  display: flex;
  align-items: center;
  border: none;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.2s;
}

button span {
  display: block;
  margin-left: 0.3em;
  transition: all 0.3s ease-in-out;
}

button svg {
  display: block;
  transform-origin: center center;
  transition: transform 0.3s ease-in-out;
}


.card-last-prompt{
  margin-right: 10px;
  /* line-height: 10px; */
  max-width: 75%;
  align-self: flex-end;
  width: auto;
  background: #e6e7e8;
  position: relative;
  display: flex;
  place-content: center;
  place-items: center;
  overflow: hidden;
  border-radius: 16px;
  padding: 0rem 1.2rem 0rem 1.2rem;
  margin-bottom: 25px;
}

.card-result {
  /* width: auto; */
  align-self: flex-start;
  max-width: 75%;
  overflow: scroll;
  scrollbar-width: none !important; /* 隐藏滚动条 (仅适用于 Firefox) */
  border-radius: 16px;
  padding: 0rem 2rem 0rem 2rem;
  color: black;
}

.card-last-prompt::-webkit-scrollbar {
  display: none; /* 隐藏滚动条 (仅适用于 Chrome、Safari 和 Edge Chromium) */
}

.button-block {
  display: flex;
  align-items: center;
  justify-content: end;
}
.btn {
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 8rem;
  max-width: 13rem;
  height: 3rem;
  background-size: 300% 300%;
  backdrop-filter: blur(1rem);
  border-radius: 5rem;
  transition: 0.5s;
  animation: gradient_301 5s ease infinite;
  border: double 4px transparent;
  background-image: linear-gradient(#212121, #212121),
    linear-gradient(137.48deg, #ffdb3b 10%, #fe53bb 45%, #8f51ea 67%, #0044ff 87%);
  background-origin: border-box;
  background-clip: content-box, border-box;
}

#container-stars {
  position: fixed;
  z-index: -1;
  width: 100%;
  height: 100%;
  overflow: hidden;
  transition: 0.5s;
  backdrop-filter: blur(1rem);
  border-radius: 5rem;
}

strong {
  z-index: 2;
  font-size: 16px;
  color: #ffffff;
  text-shadow: 0 0 4px white;
}

#glow {
  position: absolute;
  display: flex;
  width: 12rem;
}

.circle {
  width: 100%;
  height: 30px;
  filter: blur(2rem);
  animation: pulse_3011 4s infinite;
  z-index: -1;
}

.circle:nth-of-type(1) {
  background: rgba(254, 83, 186, 0.636);
}

.circle:nth-of-type(2) {
  background: rgba(142, 81, 234, 0.704);
}

.btn:hover #container-stars {
  z-index: 1;
  background-color: #212121;
}

.btn:hover {
  transform: scale(1.1);
}

.btn:active {
  border: double 4px #fe53bb;
  background-origin: border-box;
  background-clip: content-box, border-box;
  animation: none;
}

.btn:active .circle {
  background: #fe53bb;
}

#stars {
  position: relative;
  background: transparent;
  width: 200rem;
  height: 200rem;
}

#stars::after {
  content: '';
  position: absolute;
  top: -10rem;
  left: -100rem;
  width: 100%;
  height: 100%;
  animation: animStarRotate 90s linear infinite;
}

#stars::after {
  background-image: radial-gradient(#ffffff 1px, transparent 1%);
  background-size: 50px 50px;
}

#stars::before {
  content: '';
  position: absolute;
  top: 0;
  left: -50%;
  width: 170%;
  height: 500%;
  animation: animStar 60s linear infinite;
}

#stars::before {
  background-image: radial-gradient(#ffffff 1px, transparent 1%);
  background-size: 50px 50px;
  opacity: 0.5;
}

@keyframes animStar {
  from {
    transform: translateY(0);
  }

  to {
    transform: translateY(-135rem);
  }
}

@keyframes animStarRotate {
  from {
    transform: rotate(360deg);
  }

  to {
    transform: rotate(0);
  }
}

@keyframes gradient_301 {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

@keyframes pulse_3011 {
  0% {
    transform: scale(0.75);
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.7);
  }

  70% {
    transform: scale(1);
    box-shadow: 0 0 0 10px rgba(0, 0, 0, 0);
  }

  100% {
    transform: scale(0.75);
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
  }
}

.input-container {
  margin-bottom: 20px;
}

</style>
