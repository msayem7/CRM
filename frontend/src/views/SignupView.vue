<template>
  <div class="signup-page">
    <div class="signup-background">
      <div class="bg-shape bg-shape-1"></div>
      <div class="bg-shape bg-shape-2"></div>
      <div class="bg-shape bg-shape-3"></div>
    </div>
    
    <div class="signup-container">
      <div class="signup-card">
        <div class="signup-header">
          <h1>Create Account</h1>
          <p class="subtitle">Start managing your business</p>
        </div>
        
        <form @submit.prevent="handleSignup">
          <div class="form-group">
            <label for="name">Name</label>
            <input 
              v-model="form.name" 
              type="text" 
              id="name" 
              placeholder="Enter your full name"
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="email">Email *</label>
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
            <label for="business_name">Business Name</label>
            <input 
              v-model="form.business_name" 
              type="text" 
              id="business_name" 
              placeholder="Your company name"
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="password">Password *</label>
            <div class="password-field">
              <input 
                v-model="form.password" 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                placeholder="Create a password (min 8 characters)"
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

          <div class="form-group">
            <label for="password_confirm">Confirm Password *</label>
            <div class="password-field">
              <input 
                v-model="form.password_confirm" 
                :type="showPasswordConfirm ? 'text' : 'password'" 
                id="password_confirm" 
                placeholder="Confirm your password"
                required 
                :disabled="loading"
              />
              <button 
                type="button" 
                class="toggle-password"
                @click="showPasswordConfirm = !showPasswordConfirm"
              >
                {{ showPasswordConfirm ? '👁️' : '👁️‍🗨️' }}
              </button>
            </div>
          </div>

          <div v-if="error" class="error-message">
            {{ formatError(error) }}
          </div>

          <button type="submit" class="btn-primary" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Creating account...' : 'Create Account' }}
          </button>

          <p class="login-link">
            Already have an account? 
            <router-link to="/login">Sign in</router-link>
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
  name: '',
  email: '',
  business_name: '',
  password: '',
  password_confirm: '',
})

const loading = ref(false)
const error = ref(null)
const showPassword = ref(false)
const showPasswordConfirm = ref(false)

const formatError = (err) => {
  if (typeof err === 'object' && err !== null) {
    const firstKey = Object.keys(err)[0]
    if (firstKey && Array.isArray(err[firstKey])) {
      return `${firstKey}: ${err[firstKey][0]}`
    }
    return JSON.stringify(err)
  }
  return err
}

const handleSignup = async () => {
  if (form.password !== form.password_confirm) {
    error.value = 'Passwords do not match.'
    return
  }
  
  if (form.password.length < 8) {
    error.value = 'Password must be at least 8 characters.'
    return
  }
  
  if (!form.email) {
    error.value = 'Email is required.'
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    // Split name into first_name and last_name
    const nameParts = form.name.trim().split(' ')
    const first_name = nameParts[0] || ''
    const last_name = nameParts.slice(1).join(' ') || ''
    
    // Generate username from email (part before @)
    const username = form.email.split('@')[0].toLowerCase()
    
    await authStore.signup({
      username: username,
      email: form.email.toLowerCase(),
      first_name: first_name,
      last_name: last_name,
      business_name: form.business_name,
      password: form.password,
      password_confirm: form.password_confirm,
    })
    router.push('/dashboard')
  } catch (err) {
    if (err.response?.data?.errors) {
      error.value = err.response.data.errors
    } else if (err.response?.data?.message) {
      error.value = err.response.data.message
    } else {
      error.value = err.message || 'Registration failed. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.signup-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
  padding: 40px 20px;
}

.signup-background {
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

.signup-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 440px;
}

.signup-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 40px 36px;
}

.signup-header {
  text-align: center;
  margin-bottom: 32px;
}

.signup-header h1 {
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
  margin-bottom: 20px;
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

.login-link {
  text-align: center;
  margin-top: 28px;
  color: #666;
  font-size: 15px;
}

.login-link a {
  color: #667eea;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s;
}

.login-link a:hover {
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
  .signup-card {
    padding: 28px 24px;
    border-radius: 16px;
  }

  .signup-header h1 {
    font-size: 26px;
  }

  .form-group {
    margin-bottom: 18px;
  }

  .form-group input {
    padding: 12px 16px;
  }

  .btn-primary {
    padding: 14px;
  }

  .signup-page {
    padding: 20px 16px;
  }
}
</style>
