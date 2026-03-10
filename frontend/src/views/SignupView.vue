<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light py-5 w-100">
    <div class="container-fluid px-4">
      <div class="row justify-content-center w-100 m-0">
        <div class="col-12 col-sm-10 col-md-8 col-lg-6 col-xl-5 col-xxl-4">
          <div class="card shadow-lg border-0 rounded-lg">
            <div class="card-header bg-primary text-white text-center py-4">
              <h3 class="font-weight-light my-2">Create Account</h3>
              <p class="mb-0">Start managing your business</p>
            </div>
            <div class="card-body p-5">
              <form @submit.prevent="handleSignup">
                <div class="row mb-3">
                  <div class="col-md-6">
                    <div class="form-floating mb-3 mb-md-0">
                      <input 
                        v-model="form.name" 
                        type="text" 
                        class="form-control" 
                        id="name" 
                        placeholder="Enter your full name"
                        :disabled="loading"
                      />
                      <label for="name">Full Name</label>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-floating">
                      <input 
                        v-model="form.business_name" 
                        type="text" 
                        class="form-control" 
                        id="business_name" 
                        placeholder="Your company name"
                        :disabled="loading"
                      />
                      <label for="business_name">Business Name</label>
                    </div>
                  </div>
                </div>

                <div class="form-floating mb-3">
                  <input 
                    v-model="form.email" 
                    type="email" 
                    class="form-control" 
                    id="email" 
                    placeholder="name@example.com"
                    required 
                    :disabled="loading"
                  />
                  <label for="email">Email address *</label>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <div class="form-floating mb-3 mb-md-0 position-relative">
                      <input 
                        v-model="form.password" 
                        :type="showPassword ? 'text' : 'password'" 
                        class="form-control" 
                        id="password" 
                        placeholder="Create a password"
                        required 
                        :disabled="loading"
                      />
                      <label for="password">Password *</label>
                      <button 
                        type="button" 
                        class="btn btn-link position-absolute top-50 end-0 translate-middle-y text-decoration-none text-secondary"
                        @click="showPassword = !showPassword"
                        style="z-index: 5;"
                      >
                        <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                      </button>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-floating mb-3 mb-md-0 position-relative">
                      <input 
                        v-model="form.password_confirm" 
                        :type="showPasswordConfirm ? 'text' : 'password'" 
                        class="form-control" 
                        id="password_confirm" 
                        placeholder="Confirm password"
                        required 
                        :disabled="loading"
                      />
                      <label for="password_confirm">Confirm Password *</label>
                      <button 
                        type="button" 
                        class="btn btn-link position-absolute top-50 end-0 translate-middle-y text-decoration-none text-secondary"
                        @click="showPasswordConfirm = !showPasswordConfirm"
                        style="z-index: 5;"
                      >
                        <i :class="showPasswordConfirm ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                      </button>
                    </div>
                  </div>
                </div>

                <div v-if="error" class="alert alert-danger py-2" role="alert">
                  {{ formatError(error) }}
                </div>

                <div class="mt-4 mb-0">
                  <div class="d-grid">
                    <button type="submit" class="btn btn-primary btn-lg" :disabled="loading">
                      <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      {{ loading ? 'Creating account...' : 'Create Account' }}
                    </button>
                  </div>
                </div>
              </form>
            </div>
            <div class="card-footer text-center py-3 bg-light">
              <div class="small">
                Already have an account? 
                <router-link to="/login" class="text-primary text-decoration-none">Sign in</router-link>
              </div>
            </div>
          </div>
        </div>
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
/* Custom styles can be added here if needed, but mostly relying on Bootstrap */
</style>
