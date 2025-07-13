<template>
  <Sidebar>
    <div class="add-event-container">
      <h1>Add New Event for {{ orgName }}</h1>

      <div v-if="message" :class="['message', messageType]">{{ message }}</div>

      <form @submit.prevent="submitEvent">
        <div class="form-group">
          <label for="eventName">Event Name</label>
          <input id="eventName" v-model="eventName" placeholder="Enter event name" />
        </div>

        <div class="form-group">
          <label for="date">Date</label>
          <input type="date" id="date" v-model="date" />
        </div>

        <div class="form-group">
          <label for="startTime">Start Time</label>
          <input type="time" id="startTime" v-model="startTime" />
        </div>

        <div class="form-group">
          <label for="endTime">End Time</label>
          <input type="time" id="endTime" v-model="endTime" />
        </div>

        <div class="form-group">
          <label for="location">Location</label>
          <input id="location" v-model="location" placeholder="Enter location" />
        </div>

        <button type="submit" :disabled="submitting">
          {{ submitting ? 'Submitting...' : 'Create Event' }}
        </button>
      </form>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { supabase } from '../supabase.js'
import Sidebar from '../components/Sidebar.vue'

// Route + org context
const route = useRoute()
const router = useRouter()
const orgId = route.query.org_id
const orgName = route.query.org_name

// Form state
const eventName = ref('')
const date = ref(new Date().toISOString().split('T')[0]) // default today
const startTime = ref('')
const endTime = ref('')
const location = ref('')
const submitting = ref(false)
const message = ref('')
const messageType = ref('')

// Submit handler
const submitEvent = async () => {
  submitting.value = true
  message.value = ''

  if (!orgId || !orgName) {
    message.value = '❌ Missing organisation info. Please go through the dashboard.'
    messageType.value = 'error'
    submitting.value = false
    return
  }

  if (!eventName.value || !startTime.value || !endTime.value || !location.value || !date.value) {
    message.value = '❌ Please fill in all fields.'
    messageType.value = 'error'
    submitting.value = false
    return
  }

  const start = new Date(`${date.value}T${startTime.value}:00Z`)
  const end = new Date(`${date.value}T${endTime.value}:00Z`)

  if (end <= start) {
    message.value = '❌ End time must be after start time.'
    messageType.value = 'error'
    submitting.value = false
    return
  }

  const { error } = await supabase.from('Events').insert({
    name: eventName.value,
    date: date.value,
    start_time: start.toISOString(),
    end_time: end.toISOString(),
    location: location.value,
    organisation_id: orgId, // Make sure this is defined
    organisation_name: orgName
  })

  if (error) {
    message.value = `❌ Failed to create event: ${error.message}`
    messageType.value = 'error'
  } else {
    message.value = '✅ Event created successfully!'
    messageType.value = 'success'
    setTimeout(() => router.push('/admin-dashboard'), 2000)
  }

  submitting.value = false
}

</script>

<style scoped>
.add-event-container {
  padding: 2rem;
  max-width: 600px;
  margin: auto;
  font-family: sans-serif;
}

h1 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  margin-top: 1rem;
  padding: 0.7rem 1.5rem;
  background: #2c7be5;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #1a5fcc;
}

button:disabled {
  background-color: #8ab6f0;
  cursor: not-allowed;
}

.message {
  padding: 0.75rem;
  margin-bottom: 1rem;
  border-radius: 6px;
  font-weight: 500;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
}
</style>
