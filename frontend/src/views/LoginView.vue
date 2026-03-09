<template>
  <div class="login-page">
    <div class="login-background">
      <div class="bg-shape bg-shape-1"></div>
      <div class="bg-shape bg-shape-2"></div>
      <div class="bg-shape bg-shape-3"></div>
    </div>
    
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>Welcome Back</h1>
          <p class="subtitle">Sign in to your account</p>
        </div>
        
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="email">Email</label>
            <input 
              v-model="form.email" 
              type="email" 
              id="email" 
              placeholder="Enter your email"
              required 
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <div class="password-field">
              <input 
                v-model="form.password" 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                placeholder="Enter your password"
                required 
                :disabled="loading"
              />
              <button 
                type="button" 
                class="toggle-password"
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? '👁️' : '👁️‍🗨️' }}
              </button>
            </div>
          </div>

          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <button type="submit" class="btn-primary" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>

          <p class="register-link">
            Don't have an account? 
            <router-link to="/signup">Create one</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
})

const loading = ref(false)
const error = ref(null)
const showPassword = ref(false)

const handleLogin = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Use email as username for authentication
    await authStore.login(form.email, form.password)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.message || err.message || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.bg-shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
  background: white;
}

.bg-shape-1 {
  width: 600px;
  height: 600px;
  top: -200px;
  right: -200px;
  animation: float 20s ease-in-out infinite;
}

.bg-shape-2 {
  width: 400px;
  height: 400px;
  bottom: -100px;
  left: -100px;
  animation: float 15s ease-in-out infinite reverse;
}

.bg-shape-3 {
  width: 300px;
  height: 300px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 10s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) rotate(10deg);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.1;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 0.05;
  }
}

.login-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 440px;
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 48px 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 36px;
}

.login-header h1 {
  margin: 0 0 8px 0;
  color: #1a1a1a;
  font-size: 32px;
  font-weight: 700;
}

.subtitle {
  color: #666;
  margin: 0;
  font-size: 16px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 14px 18px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s ease;
  box-sizing: border-box;
  background: #fafafa;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.form-group input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.form-group input::placeholder {
  color: #9ca3af;
}

.password-field {
  position: relative;
}

.password-field input {
  padding-right: 50px;
}

.toggle-password {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  padding: 4px;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.toggle-password:hover {
  opacity: 1;
}

.btn-primary {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 8px;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  background-color: #fef2f2;
  color: #dc2626;
  padding: 14px 18px;
  border-radius: 10px;
  margin-bottom: 20px;
  font-size: 14px;
  text-align: center;
  border: 1px solid #fecaca;
}

.register-link {
  text-align: center;
  margin-top: 28px;
  color: #666;
  font-size: 15px;
}

.register-link a {
  color: #667eea;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s;
}

.register-link a:hover {
  color: #764ba2;
  text-decoration: underline;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive Design */
@media (max-width: 480px) {
  .login-card {
    padding: 32px 24px;
    border-radius: 16px;
  }

  .login-header h1 {
    font-size: 26px;
  }

  .form-group {
    margin-bottom: 20px;
  }

  .form-group input {
    padding: 12px 16px;
  }

  .btn-primary {
    padding: 14px;
  }
}
</style>
