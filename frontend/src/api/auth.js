import api from './client'

export const authApi = {
  /**
   * Register a new user
   * @param {Object} data - { email, password, password_confirm, first_name, last_name, business_name }
   */
  signup(data) {
    return api.post('/auth/signup/', data)
  },

  /**
   * Login user
   * @param {string} email 
   * @param {string} password 
   */
  login(email, password) {
    return api.post('/auth/login/', { email, password })
  },

  /**
   * Get current user profile
   */
  getMe() {
    return api.get('/auth/me/')
  },

  /**
   * Get current user's business
   */
  getBusiness() {
    return api.get('/auth/business/')
  },

  /**
   * Update business details
   * @param {Object} data - Business data to update
   */
  updateBusiness(data) {
    return api.put('/auth/business/', data)
  },

  /**
   * Change password
   * @param {Object} data - { current_password, new_password, new_password_confirm }
   */
  changePassword(data) {
    return api.post('/auth/password-change/', data)
  },

  /**
   * Logout user
   * @param {string} refreshToken - Refresh token to blacklist
   */
  logout(refreshToken) {
    return api.post('/auth/logout/', { refresh: refreshToken })
  },

  /**
   * Verify token validity
   * @param {string} token - Access token
   */
  verifyToken(token) {
    return api.post('/auth/token/verify/', { token })
  },

  /**
   * Refresh access token
   * @param {string} refreshToken - Refresh token
   */
  refreshToken(refreshToken) {
    return api.post('/auth/token/refresh/', { refresh: refreshToken })
  },
}

export default authApi
