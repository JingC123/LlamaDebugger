import './style.css'


import App from './App.vue'

import { createApp } from 'vue';
import TDesign from 'tdesign-vue-next';

// 引入组件库的少量全局样式变量
import 'tdesign-vue-next/es/style/index.css';

const app = createApp(App);
app.mount('#app')

app.use(TDesign);