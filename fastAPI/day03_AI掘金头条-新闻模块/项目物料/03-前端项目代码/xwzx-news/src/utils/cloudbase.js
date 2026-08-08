import cloudbase from '@cloudbase/js-sdk'

// CloudBase 环境配置
const app = cloudbase.init({
  env: import.meta.env.VITE_TCB_ENV_ID || 'cloud1-5gh0r8j0272e1c10',
  region: import.meta.env.VITE_TCB_REGION || 'ap-shanghai',
})

// 匿名登录（免注册使用 CloudBase 能力）
export async function ensureLogin() {
  const auth = app.auth()
  const loginState = await auth.getLoginState()
  if (!loginState) {
    await auth.signInAnonymously()
  }
  return loginState
}

export const db = app.database()
export const storage = app.uploadFile.bind(app)

export default app
