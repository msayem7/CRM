<template>
  <div class="signup-container">
    <div class="signup-card">
      <h1>Create Account</h1>
      <p class="subtitle">Start managing your business</p>
      
      <form @submit.prevent="handleSignup">
        <div class="form-row">
          <div class="form-group">
            <label for="first_name">First Name</label>
            <input 
              v-model="form.first_name" 
              type="text" 
              id="first_name" 
              placeholder="First name"
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="last_name">Last Name</label>
            <input 
              v-model="form.last_name" 
              type="text" 
              id="last_name" 
              placeholder="Last name"
              :disabled="loading"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="username">Username *</label>
          <input 
            v-model="form.username" 
            type="text" 
            id="username" 
            placeholder="Choose a username"
            required 
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
          <input 
            v-model="form.password" 
            type="password" 
            id="password" 
            placeholder="Create a password (min 8 characters)"
            required 
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="password_confirm">Confirm Password *</label>
          <input 
            v-model="form.password_confirm" 
            type="password" 
            id="password_confirm" 
            placeholder="Confirm your password"
            required 
            :disabled="loading"
          />
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
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  business_name: '',
  password: '',
  password_confirm: '',
})

const loading = ref(false)
const error = ref(null)

const formatError = (err) => {
  if (typeof err === 'object' && err !== null) {
    // Handle validation errors object
    const firstKey = Object.keys(err)[0]
    if (firstKey && Array.isArray(err[firstKey])) {
      return `${firstKey}: ${err[firstKey][0]}`
    }
    return JSON.stringify(err)
  }
  return err
}

const handleSignup = async () => {
  // Validate passwords match
  if (form.password !== form.password_confirm) {
    error.value = 'Passwords do not match.'
    return
  }
  
  // Validate password length
  if (form.password.length < 8) {
    error.value = 'Password must be at least 8 characters.'
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    await authStore.signup({
      username: form.username,
      email: form.email,
      first_name: form.first_name,
      last_name: form.last_name,
      business_name: form.business_name,
      password: form.password,
      password_confirm: form.password_confirm,
    })
    router.push('/dashboard')
  } catch (err) {
    // Handle different error formats
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
.signup-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.signup-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  padding: 40px;
  width: 100%;
  max-width: 500px;
}

h1 {
  text-align: center;
  margin: 0 0 8px 0;
  color: #333;
  font-size: 28px;
}

.subtitle {
  text-align: center;
  color: #666;
  margin: 0 0 32px 0;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-row .form-group {
  flex: 1;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #444;
  font-size: 14px;
}

input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #667eea;
}

input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.btn-primary {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  background-color: #fee2e2;
  color: #dc2626;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
  text-align: center;
}

.login-link {
  text-align: center;
  margin-top: 24px;
  color: #666;
}

.login-link a {
  color: #667eea;
  font-weight: 600;
  text-decoration: none;
}

.login-link a:hover {
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
</style>
