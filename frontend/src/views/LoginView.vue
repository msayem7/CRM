<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light w-100">
    <div class="container-fluid px-4">
      <div class="row justify-content-center w-100 m-0">
        <div class="col-12 col-sm-10 col-md-8 col-lg-6 col-xl-5 col-xxl-4">
          <div class="card shadow-lg border-0 rounded-lg mt-5">
            <div class="card-header bg-primary text-white text-center py-4">
              <h3 class="font-weight-light my-2">Welcome Back</h3>
              <p class="mb-0">Sign in to your account</p>
            </div>
            <div class="card-body p-5">
              <form @submit.prevent="handleLogin">
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
                  <label for="email">Email address</label>
                </div>

                <div class="form-floating mb-3 position-relative">
                  <input 
                    v-model="form.password" 
                    :type="showPassword ? 'text' : 'password'" 
                    class="form-control" 
                    id="password" 
                    placeholder="Password"
                    required 
                    :disabled="loading"
                  />
                  <label for="password">Password</label>
                  <button 
                    type="button" 
                    class="btn btn-link position-absolute top-50 end-0 translate-middle-y text-decoration-none text-secondary"
                    @click="showPassword = !showPassword"
                    style="z-index: 5;"
                  >
                    <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    <!-- {{ showPassword ? 'Hide' : 'Show' }} -->
                  </button>
                </div>

                <div v-if="error" class="alert alert-danger py-2" role="alert">
                  {{ error }}
                </div>

                <div class="d-grid gap-2 mt-4 mb-0">
                  <button type="submit" class="btn btn-primary btn-lg" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    {{ loading ? 'Signing in...' : 'Sign In' }}
                  </button>
                </div>
              </form>
            </div>
            <div class="card-footer text-center py-3 bg-light">
              <div class="small">
                Don't have an account? 
                <router-link to="/signup" class="text-primary text-decoration-none">Create one</router-link>
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
/* Custom styles can be added here if needed, but mostly relying on Bootstrap */
</style>
