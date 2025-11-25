import { createApp } from 'vue';
import App from './App.vue';

const app = createApp(App);

// 全局错误处理
app.config.errorHandler = (err, vm, info) => {
  // 这里的错误捕获主要是用来捕获 Vue 组件中的运行时错误
  console.error('Global Error Handler:', err); // 打印错误信息
  console.error('Component Info:', info); // 错误发生的组件信息
  // 你可以在这里发送错误日志到后端进行监控
  alert('系统发生错误，请稍后重试');
};

app.mount('#app'); // 挂载 Vue 实例
