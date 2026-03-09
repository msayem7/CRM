<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <h1>Dashboard</h1>
        <div class="user-menu">
          <span class="user-name">{{ authStore.userFullName }}</span>
          <button @click="handleLogout" class="btn-logout">Logout</button>
        </div>
      </div>
    </header>

    <main class="dashboard-content">
      <div class="welcome-section">
        <div class="welcome-card">
          <h2>Welcome back, {{ authStore.user?.username || 'User' }}!</h2>
          <p v-if="authStore.business">
            Managing: <strong>{{ authStore.business.name }}</strong>
          </p>
        </div>
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

        <div class="stat-card">
          <div class="stat-icon">📋</div>
          <div class="stat-info">
            <h3>Leads</h3>
            <p>Track your leads</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">💼</div>
          <div class="stat-info">
            <h3>Deals</h3>
            <p>Manage your deals</p>
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
  background-color: #f0f2f5;
}

.dashboard-header {
  background: white;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-header h1 {
  margin: 0;
  color: #1a1a1a;
  font-size: 24px;
  font-weight: 600;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-name {
  color: #666;
  font-weight: 500;
  font-size: 14px;
}

.btn-logout {
  padding: 8px 20px;
  background-color: #f0f0f0;
  color: #333;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  background-color: #e0e0e0;
  color: #000;
}

.dashboard-content {
  padding: 32px;
  max-width: 1400px;
  margin: 0 auto;
}

.welcome-section {
  margin-bottom: 32px;
}

.welcome-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px 48px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

.welcome-card h2 {
  margin: 0 0 12px 0;
  font-size: 32px;
  font-weight: 600;
}

.welcome-card p {
  margin: 0;
  opacity: 0.9;
  font-size: 16px;
}

.welcome-card strong {
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.stat-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 40px;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 12px;
}

.stat-info h3 {
  margin: 0 0 8px 0;
  color: #1a1a1a;
  font-size: 18px;
  font-weight: 600;
}

.stat-info p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    padding: 12px 16px;
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .dashboard-header h1 {
    font-size: 20px;
  }

  .user-menu {
    width: 100%;
    justify-content: space-between;
  }

  .dashboard-content {
    padding: 16px;
  }

  .welcome-card {
    padding: 24px;
  }

  .welcome-card h2 {
    font-size: 24px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .stat-card {
    padding: 20px;
  }

  .stat-icon {
    font-size: 32px;
    width: 52px;
    height: 52px;
  }

  .stat-info h3 {
    font-size: 16px;
  }
}

@media (min-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .welcome-card {
    padding: 48px 56px;
  }

  .welcome-card h2 {
    font-size: 36px;
  }
}
</style>
