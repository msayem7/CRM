<template>
  <div class="d-flex min-vh-100 bg-light">
    <!-- Sidebar (Desktop) -->
    <div 
      class="d-none d-md-flex flex-column flex-shrink-0 p-3 text-white bg-dark transition-all"
      :style="{ width: isSidebarCollapsed ? '80px' : '280px', transition: 'width 0.3s ease' }"
    >
      <div class="d-flex align-items-center justify-content-between mb-3 mb-md-0">
        <span class="fs-4 fw-bold" v-show="!isSidebarCollapsed">CRM</span>
        <button class="btn btn-outline-light btn-sm" @click="toggleSidebar">
          <i :class="isSidebarCollapsed ? 'bi bi-chevron-right' : 'bi bi-chevron-left'"></i>
        </button>
      </div>
      <hr>
      <ul class="nav nav-pills flex-column mb-auto">
        <li class="nav-item">
          <a href="#" class="nav-link active d-flex align-items-center" aria-current="page">
            <i class="bi bi-speedometer2 fs-5"></i>
            <span class="ms-3" v-show="!isSidebarCollapsed">Dashboard</span>
          </a>
        </li>
        <li>
          <a href="#" class="nav-link text-white d-flex align-items-center">
            <i class="bi bi-people fs-5"></i>
            <span class="ms-3" v-show="!isSidebarCollapsed">Customers</span>
          </a>
        </li>
        <li>
          <a href="#" class="nav-link text-white d-flex align-items-center">
            <i class="bi bi-graph-up-arrow fs-5"></i>
            <span class="ms-3" v-show="!isSidebarCollapsed">Analytics</span>
          </a>
        </li>
        <li>
          <a href="#" class="nav-link text-white d-flex align-items-center">
            <i class="bi bi-list-task fs-5"></i>
            <span class="ms-3" v-show="!isSidebarCollapsed">Leads</span>
          </a>
        </li>
        <li>
          <a href="#" class="nav-link text-white d-flex align-items-center">
            <i class="bi bi-briefcase fs-5"></i>
            <span class="ms-3" v-show="!isSidebarCollapsed">Deals</span>
          </a>
        </li>
        <li>
          <a href="#" class="nav-link text-white d-flex align-items-center">
            <i class="bi bi-gear fs-5"></i>
            <span class="ms-3" v-show="!isSidebarCollapsed">Settings</span>
          </a>
        </li>
      </ul>
      <hr>
      <div class="dropdown">
        <a href="#" class="d-flex align-items-center text-white text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown" aria-expanded="false">
          <i class="bi bi-person-circle fs-5"></i>
          <strong class="ms-3" v-show="!isSidebarCollapsed">{{ authStore.userFullName || 'User' }}</strong>
        </a>
        <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser1">
          <li><a class="dropdown-item" href="#">Profile</a></li>
          <li><hr class="dropdown-divider"></li>
          <li><a class="dropdown-item" href="#" @click.prevent="handleLogout">Sign out</a></li>
        </ul>
      </div>
    </div>

    <!-- Offcanvas Sidebar (Mobile) -->
    <div class="offcanvas offcanvas-start text-white bg-dark" tabindex="-1" id="sidebarMenu" aria-labelledby="sidebarMenuLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title fw-bold" id="sidebarMenuLabel">CRM Dashboard</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body d-flex flex-column">
        <ul class="nav nav-pills flex-column mb-auto">
          <li class="nav-item">
            <a href="#" class="nav-link active" aria-current="page">
              <span class="me-2">📊</span> Dashboard
            </a>
          </li>
          <li>
            <a href="#" class="nav-link text-white">
              <span class="me-2">👥</span> Customers
            </a>
          </li>
          <li>
            <a href="#" class="nav-link text-white">
              <span class="me-2">📈</span> Analytics
            </a>
          </li>
          <li>
            <a href="#" class="nav-link text-white">
              <span class="me-2">📋</span> Leads
            </a>
          </li>
          <li>
            <a href="#" class="nav-link text-white">
              <span class="me-2">💼</span> Deals
            </a>
          </li>
          <li>
            <a href="#" class="nav-link text-white">
              <span class="me-2">⚙️</span> Settings
            </a>
          </li>
        </ul>
        <hr>
        <div class="dropdown mt-auto">
          <a href="#" class="d-flex align-items-center text-white text-decoration-none dropdown-toggle" id="dropdownUser2" data-bs-toggle="dropdown" aria-expanded="false">
            <strong>{{ authStore.userFullName || 'User' }}</strong>
          </a>
          <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser2">
            <li><a class="dropdown-item" href="#">Profile</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#" @click.prevent="handleLogout">Sign out</a></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-grow-1 d-flex flex-column overflow-hidden">
      <!-- Top Navbar for Mobile -->
      <nav class="navbar navbar-expand-md navbar-light bg-white shadow-sm d-md-none">
        <div class="container-fluid px-4">
          <button class="navbar-toggler border-0 px-0" type="button" data-bs-toggle="offcanvas" data-bs-target="#sidebarMenu" aria-controls="sidebarMenu">
            <span class="navbar-toggler-icon"></span>
          </button>
          <a class="navbar-brand fw-bold ms-2" href="#">CRM</a>
          <div class="d-flex align-items-center">
            <button @click="handleLogout" class="btn btn-outline-danger btn-sm rounded-pill px-3">Logout</button>
          </div>
        </div>
      </nav>

      <!-- Top Header for Desktop -->
      <header class="d-none d-md-flex align-items-center justify-content-between px-4 py-3 bg-white shadow-sm">
        <h4 class="mb-0 fw-bold text-dark">Dashboard</h4>
        <div class="d-flex align-items-center">
          <span class="me-3 text-muted fw-medium" v-if="authStore.business">{{ authStore.business.name }}</span>
          <button @click="handleLogout" class="btn btn-outline-danger btn-sm rounded-pill px-3">Logout</button>
        </div>
      </header>

      <main class="container-fluid px-4 py-4 overflow-auto">
        <div class="row mb-4">
          <div class="col-12">
            <div class="card border-0 shadow-sm rounded-3 bg-white">
              <div class="card-body p-4">
                <h2 class="card-title fw-bold text-dark mb-2">Welcome back, {{ authStore.user?.username || 'User' }}!</h2>
                <p class="card-text text-muted fs-5 mb-0" v-if="authStore.business">
                  Managing: <strong class="text-primary">{{ authStore.business.name }}</strong>
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="row g-4">
          <div class="col-md-6 col-lg-4">
            <div class="card h-100 border-0 shadow-sm rounded-3 hover-shadow transition-all">
              <div class="card-body p-4 d-flex align-items-start">
                <div class="bg-primary bg-opacity-10 p-3 rounded-circle me-3">
                  <span class="fs-3">📊</span>
                </div>
                <div>
                  <h4 class="card-title fw-bold mb-1">Overview</h4>
                  <p class="card-text text-muted">Your CRM dashboard is ready</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-6 col-lg-4">
            <div class="card h-100 border-0 shadow-sm rounded-3 hover-shadow transition-all">
              <div class="card-body p-4 d-flex align-items-start">
                <div class="bg-success bg-opacity-10 p-3 rounded-circle me-3">
                  <span class="fs-3">👥</span>
                </div>
                <div>
                  <h4 class="card-title fw-bold mb-1">Customers</h4>
                  <p class="card-text text-muted">Manage your customers</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-6 col-lg-4">
            <div class="card h-100 border-0 shadow-sm rounded-3 hover-shadow transition-all">
              <div class="card-body p-4 d-flex align-items-start">
                <div class="bg-info bg-opacity-10 p-3 rounded-circle me-3">
                  <span class="fs-3">📈</span>
                </div>
                <div>
                  <h4 class="card-title fw-bold mb-1">Analytics</h4>
                  <p class="card-text text-muted">View reports and insights</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-6 col-lg-4">
            <div class="card h-100 border-0 shadow-sm rounded-3 hover-shadow transition-all">
              <div class="card-body p-4 d-flex align-items-start">
                <div class="bg-warning bg-opacity-10 p-3 rounded-circle me-3">
                  <span class="fs-3">📋</span>
                </div>
                <div>
                  <h4 class="card-title fw-bold mb-1">Leads</h4>
                  <p class="card-text text-muted">Track your leads</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-6 col-lg-4">
            <div class="card h-100 border-0 shadow-sm rounded-3 hover-shadow transition-all">
              <div class="card-body p-4 d-flex align-items-start">
                <div class="bg-danger bg-opacity-10 p-3 rounded-circle me-3">
                  <span class="fs-3">💼</span>
                </div>
                <div>
                  <h4 class="card-title fw-bold mb-1">Deals</h4>
                  <p class="card-text text-muted">Manage your deals</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-6 col-lg-4">
            <div class="card h-100 border-0 shadow-sm rounded-3 hover-shadow transition-all">
              <div class="card-body p-4 d-flex align-items-start">
                <div class="bg-secondary bg-opacity-10 p-3 rounded-circle me-3">
                  <span class="fs-3">⚙️</span>
                </div>
                <div>
                  <h4 class="card-title fw-bold mb-1">Settings</h4>
                  <p class="card-text text-muted">Configure your account</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref  } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const isSidebarCollapsed = ref(false);
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

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};
</script>

<style scoped>
.hover-shadow:hover {
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15)!important;
  transform: translateY(-2px);
}
.transition-all {
  transition: all .3s ease;
}
</style>
