/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置（优先使用环境变量，兼容多环境部署）
export const apiConfig = {
  // 后端API基础URL
  // 开发环境：空字符串 → 相对路径 → Vite proxy 代理到本地后端
  // 生产环境：空字符串 → 相对路径 → Nginx /api/ 代理到后端
  // 也可通过 VITE_API_BASE_URL 环境变量覆盖
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
}

export const aiChatConfig = {
  // 后端 AI 聊天接口（Vite proxy: /api → localhost:8000）
  apiEndpoint: '/api/ai/chat',
}
