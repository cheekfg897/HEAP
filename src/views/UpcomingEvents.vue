<template>
  <Sidebar>
  <div class="upcoming-events-page">
    <h1>📅 Upcoming Events</h1>

    <!-- Search input -->
    <input 
      type="text" 
      v-model="searchTerm" 
      placeholder="Search events..." 
      class="search-input"
    />

    <table class="events-table">
      <thead>
        <tr>
          <th>Event Name</th>
          <th>Date</th>
          <th>Location</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="event in filteredEvents" 
          :key="event.id"
          @click="selectEvent(event)"
          :class="{ selected: selectedEvent && selectedEvent.id === event.id }"
          style="cursor: pointer;"
        >
          <td>{{ event.name }}</td>
          <td>{{ formatDate(event.date) }}</td>
          <td>{{ event.location }}</td>
        </tr>
        <tr v-if="filteredEvents.length === 0">
          <td colspan="3" style="text-align:center; color: #999;">No events found.</td>
        </tr>
      </tbody>
    </table>

    <div v-if="selectedEvent" class="participant-section">
      <h2>Participants for "{{ selectedEvent.name }}"</h2>
      <table class="participants-table" v-if="participants.length">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="participant in participants" :key="participant.email">
            <td>{{ participant.name }}</td>
            <td>{{ participant.email }}</td>
            <td>{{ participant.status }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No participants found for this event.</p>
    </div>
  </div>
</Sidebar>
</template>

<script setup>
import { ref, computed } from 'vue'
import Sidebar from '../components/Sidebar.vue'

// To be changed to dynamic data later
// Sample data for events and participants
const events = ref([
  { id: 1, name: 'Hackathon @ SMU', date: '2025-06-14', location: 'SMU School of Computing 1' },
  { id: 2, name: 'BrainHack', date: '2025-07-07', location: 'MBS Convention Centre' },
  { id: 3, name: 'HEAP', date: '2025-07-25', location: 'SMU School Of Economics' },
])

const eventParticipants = {
  1: [
    { name: 'gyaltsen', email: 'gyaltsen@computing.smu', status: 'Registered' },
    { name: 'kevan', email: 'kevan@computing.smu', status: 'Checked In' },
  ],
  2: [
    { name: 'yan song', email: 'yansong@computing.smu', status: 'Registered' },
    { name: 'gerald', email: 'gerald@computing.smu', status: 'Registered' },
    { name: 'nicole', email: 'nicole@computing.smu', status: 'Registered' },
  ],
  3: [
    { name: 'james', email: 'james@computing.smu', status: 'Registered' },
  ]
}

const selectedEvent = ref(null)
const participants = ref([])

const searchTerm = ref('')

const filteredEvents = computed(() => {
  if (!searchTerm.value) return events.value
  const lower = searchTerm.value.toLowerCase()
  return events.value.filter(ev =>
    ev.name.toLowerCase().includes(lower) ||
    ev.location.toLowerCase().includes(lower)
  )
})

function selectEvent(event) {
  if (selectedEvent.value && selectedEvent.value.id === event.id) {
    selectedEvent.value = null
    participants.value = []
  } else {
    selectedEvent.value = event
    participants.value = eventParticipants[event.id] || []
  }
}

function formatDate(dateStr) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString(undefined, options)
}
</script>

<style scoped>
.upcoming-events-page {
  max-width: 800px;
  margin: 2rem auto;
  font-family: serif;
}

.search-input {
  width: 100%;
  padding: 0.5rem 1rem;
  margin-bottom: 1rem;
  font-size: 1rem;
  box-sizing: border-box;
}

.events-table,
.participants-table {
  width: 100%;
  border-collapse: collapse;
}

.events-table th,
.events-table td,
.participants-table th,
.participants-table td {
  border: 1px solid #ccc;
  padding: 0.5rem 1rem;
  text-align: left;
}

.events-table tr.selected {
  background-color: #d6eaff;
}

.events-table tr:hover {
  background-color: #f0f8ff;
}

.participant-section {
  margin-top: 2rem;
}

.participants-table th {
  background-color: #f0f0f0;
}
</style>
