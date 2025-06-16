<template>
  <div class="app-container">
    <!-- Sidebar -->
    <aside :class="{ 'sidebar-open': isOpen }" class="sidebar">
      <button class="close-btn" @click="toggleSidebar">✖</button>
      <nav>
        <div class="nav-item"><a href="/dashboard">🏠 Dashboard</a></div>
        <div class="nav-item"><a href="/checkin">📄 Check In</a></div>
        <div class="nav-section-title">Features:</div>
        <div class="nav-item"><a href="#">📅 Upcoming Events</a></div>
        <div class="nav-item"><a href="#">📊 Post Event Analytics</a></div>
        <div class="nav-item logout"><a href="#">🚪 Log Out</a></div>
      </nav>
    </aside>

    <!-- Overlay for mobile -->
    <div class="overlay" v-if="isOpen" @click="toggleSidebar"></div>

    <!-- Main content -->
    <main class="main-content">
      <button class="toggle-btn" @click="toggleSidebar">☰ Menu</button>
      <slot />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isOpen = ref(false)
const toggleSidebar = () => {
  isOpen.value = !isOpen.value
}
</script>

<style scoped>
.app-container {
  display: flex;
  min-height: 100vh;
}

/* Sidebar styling */
.sidebar {
  width: 250px;
  background-color: #2c3e50;
  color: white;
  padding: 2rem 1rem;
  position: fixed;
  left: -250px;
  top: 0;
  bottom: 0;
  transition: left 0.3s ease;
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

.sidebar-open {
  left: 0;
}

.sidebar .close-btn {
  background: none;
  color: white;
  border: none;
  font-size: 1.5rem;
  margin-bottom: 2rem;
  align-self: flex-end;
  cursor: pointer;
}

.nav-item {
  margin: 1rem 0;
  background-color: #34495e;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  transition: background 0.2s;
}

.nav-item a {
  text-decoration: none;
  color: white;
  font-size: 1rem;
  display: block;
  text-align: center;
}

.nav-item:hover {
  background-color: #3d566e;
}

.nav-section-title {
  margin-top: 2rem;
  margin-bottom: 0.5rem;
  font-weight: bold;
  font-size: 0.9rem;
  color: #bdc3c7;
  text-align: center;
}

.logout {
  margin-top: auto;
  background-color: #c0392b;
}

.logout:hover {
  background-color: #e74c3c;
}

/* Overlay for mobile */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 500;
}

/* Main content */
.main-content {
  margin-left: 0;
  padding: 1rem;
  flex-grow: 1;
  transition: margin-left 0.3s ease;
}

/* Toggle button (mobile) */
.toggle-btn {
  background: #2c3e50;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  cursor: pointer;
}

/* Desktop layout */
@media (min-width: 768px) {
  .main-content {
    margin-left: 250px;
  }

  .sidebar {
    left: 0;
    position: static;
  }

  .toggle-btn, .close-btn, .overlay {
    display: none;
  }
}
</style>


