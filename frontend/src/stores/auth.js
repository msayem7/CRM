import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../api/auth'
import { getErrorMessage } from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const business = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  // Getters
  const isAuthenticated = computed(() => !!user.value && !!localStorage.getItem('access_token'))
  const userFullName = computed(() => {
    if (!user.value) return ''
    return [user.value.first_name, user.value.last_name].filter(Boolean).join(' ') || user.value.username
  })
  
  // Actions
  /**
   * Register a new user
   */
  const signup = async (signupData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authApi.signup(signupData)
      const { data } = response.data
      
      // Store tokens
      localStorage.setItem('access_token', data.tokens.access)
      localStorage.setItem('refresh_token', data.tokens.refresh)
      
      // Update state
      user.value = data.user
      business.value = data.business
      
      return response.data
    } catch (err) {
      error.value = getErrorMessage(err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  /**
   * Login user
   */
  const login = async (username, password) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authApi.login(username, password)
      const { data } = response.data
      
      // Store tokens
      localStorage.setItem('access_token', data.tokens.access)
      localStorage.setItem('refresh_token', data.tokens.refresh)
      
      // Update state
      user.value = data.user
      business.value = data.business
      
      return response.data
    } catch (err) {
      error.value = getErrorMessage(err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  /**
   * Logout user
   */
  const logout = async () => {
    const refreshToken = localStorage.getItem('refresh_token')
    
    try {
      if (refreshToken) {
        await authApi.logout(refreshToken)
      }
    } catch (err) {
      // Ignore logout errors
      console.warn('Logout API error:', err)
    } finally {
      // Clear state regardless of API result
      user.value = null
      business.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }
  
  /**
   * Restore session from stored token
   */
  const restoreSession = async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      return false
    }
    
    loading.value = true
    error.value = null
    
    try {
      const response = await authApi.getMe()
      const { data } = response.data
      
      user.value = data.user
      business.value = data.business
      
      return true
    } catch (err) {
      // Token invalid or expired - clear storage
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      user.value = null
      business.value = null
      return false
    } finally {
      loading.value = false
    }
  }
  
  /**
   * Update business details
   */
  const updateBusiness = async (businessData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authApi.updateBusiness(businessData)
      business.value = response.data.data
      return response.data
    } catch (err) {
      error.value = getErrorMessage(err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  /**
   * Change password
   */
  const changePassword = async (passwordData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authApi.changePassword(passwordData)
      return response.data
    } catch (err) {
      error.value = getErrorMessage(err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  return {
    // State
    user,
    business,
    loading,
    error,
    // Getters
    isAuthenticated,
    userFullName,
    // Actions
    signup,
    login,
    logout,
    restoreSession,
    updateBusiness,
    changePassword,
  }
})
