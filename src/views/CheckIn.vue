<template>
  <Sidebar>
    <div class="dashboard">
      <h1>📸 Check In</h1>
        <div id="video-container" v-if="videoVisible">
        <img id="video-feed" src="http://127.0.0.1:5000/video" width="640" height="480">
      </div>

      <h3 id="status-text">{{ statusText }}</h3>

    </div>
  </Sidebar>
</template>

<script setup>
import { reactive, computed, ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'

// ✅ Declare reactive variables
const videoVisible = ref(true)
const statusText = ref("Waiting for QR code...")

// ✅ Use onMounted to start polling after DOM is ready
onMounted(() => {
  const poll = setInterval(() => {
    fetch('http://127.0.0.1:5000/attendance_status')
      .then(res => res.json())
      .then(data => {
        if (data.data) {
          videoVisible.value = false
          statusText.value = "Attendance marked ✅: " + data.data
          clearInterval(poll)
        }
      })
  }, 1000)
})
</script>

<style scoped>
/* Keep your attendance dashboard styles */
</style>

