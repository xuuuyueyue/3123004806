//axois封装
import axios from 'axios';
import { useUserStore } from '@/stores/user'; // 引入 Pinia 的用户 Store，用于获取用户信息（Token）

// 创建 Axios 实例
const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL, // 基础 URL，通过环境变量配置，通常会指向后端 API
  timeout: 10000, // 请求超时设置
});

// 请求拦截器：每次请求前会执行
axiosInstance.interceptors.request.use(
  (config) => {
    const userStore = useUserStore(); // 获取用户的 Store 数据
    const token = userStore.token; // 获取用户的 Token
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`; // 将 Token 添加到请求头中
      // 这里是与后端接口的对接部分，Token 必须按照后端要求的方式传递给后端
    }
    return config;
  },
  (error) => {
    // 请求发生错误时的处理
    return Promise.reject(error);
  }
);

// 响应拦截器：每次收到响应时会执行
axiosInstance.interceptors.response.use(
  (response) => {
    // 这里可以处理一些后端返回的数据格式化
    return response; // 返回响应数据
  },
  (error) => {
    // 处理响应错误
    if (error.response) {
      const status = error.response.status; // 获取 HTTP 错误状态码
      if (status === 401) {
        // 401 错误：表示 Token 过期或无效，需要重新登录
        // 可以在这里处理 Token 过期的逻辑（例如跳转到登录页）
        // 这里是你与后端认证机制对接的地方
        alert('Token 已过期，请重新登录');
        // 触发全局的登录状态更新，或跳转到登录页面
      } else {
        // 处理其他类型的错误，例如 500 系统错误
        alert('系统发生错误，请稍后重试');
      }
    }
    return Promise.reject(error); // 返回错误信息
  }
);

export default axiosInstance; // 导出封装好的 Axios 实例，供其他模块使用
