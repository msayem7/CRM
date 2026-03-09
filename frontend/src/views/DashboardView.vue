<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Dashboard</h1>
      <div class="user-menu">
        <span class="user-name">{{ authStore.userFullName }}</span>
        <button @click="handleLogout" class="btn-logout">Logout</button>
      </div>
    </header>

    <main class="dashboard-content">
      <div class="welcome-card">
        <h2>Welcome, {{ authStore.user?.username || 'User' }}!</h2>
        <p v-if="authStore.business">
          Managing: <strong>{{ authStore.business.name }}</strong>
        </p>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📊</div>
          <div class="stat-info">
            <h3>Overview</h3>
            <p>Your CRM dashboard is ready</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">👥</div>
          <div class="stat-info">
            <h3>Customers</h3>
            <p>Manage your customers</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">📈</div>
          <div class="stat-info">
            <h3>Analytics</h3>
            <p>View reports and insights</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">⚙️</div>
          <div class="stat-info">
            <h3>Settings</h3>
            <p>Configure your account</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(async () => {
  // Restore session if needed
  if (!authStore.isAuthenticated) {
    const restored = await authStore.restoreSession()
    if (!restored) {
      router.push('/login')
    }
  }
})

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.dashboard-header {
  background: white;
  padding: 20px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.dashboard-header h1 {
  margin: 0;
  color: #333;
  font-size: 24px;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-name {
  color: #666;
  font-weight: 500;
}

.btn-logout {
  padding: 8px 16px;
  background-color: #fee2e2;
  color: #dc2626;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-logout:hover {
  background-color: #fecaca;
}

.dashboard-content {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 32px;
  border-radius: 12px;
  margin-bottom: 32px;
}

.welcome-card h2 {
  margin: 0 0 8px 0;
}

.welcome-card p {
  margin: 0;
  opacity: 0.9;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 32px;
}

.stat-info h3 {
  margin: 0 0 4px 0;
  color: #333;
  font-size: 18px;
}

.stat-info p {
  margin: 0;
  color: #666;
  font-size: 14px;
}
</style>
