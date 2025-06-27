<template>
  <Sidebar>
  <div class="dashboard">
    <div class="header">
      <h1>Today's Event : <span class="date">{{ day }}<sup>{{ daySuffix }}</sup> {{ month }} {{ year }}</span>, {{ eventName }}</h1>
      <div class="refresh-container">
        <p>Last Updated {{ updatedTime }}</p>
        <button class="refresh-btn" @click="refresh">
          🔄
        </button>
      </div>
    </div>

    <h2 class="section-title">Analytics Overview</h2>

    <div class="analytics-cards">
      <div class="card">
        <div class="value checked-in">{{ checkedIn }}</div>
        <div class="label">Checked In</div>
      </div>
      <div class="card">
        <div class="value not-checked-in">{{ notCheckedIn }}</div>
        <div class="label">Not Checked In</div>
      </div>
      <div class="card">
        <div class="value not-attending">{{ notAttending }}</div>
        <div class="label">Not Attending</div>
      </div>
    </div>
    <h2 class="section-title">Have Not Arrived</h2>
<table class="not-checked-in-table">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email Address</th>
      <th>Reminder</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(person, index) in notCheckedInList" :key="index">
      <td>{{ person.name }}</td>
      <td>{{ person.email }}</td>
      <td>
        <a :href="`mailto:${person.email}`">
          <button>Email</button>
        </a>
      </td>
    </tr>
  </tbody>
</table>
  </div>
  </Sidebar>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from '../components/Sidebar.vue'

// To be changed to dynamic data later
const checkedIn = ref(79)
const notCheckedIn = ref(22)
const notAttending = ref(3)
const updatedTime = ref('4:16 PM')

const refresh = () => {
  updatedTime.value = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function getDaySuffix(day) {
  if (day > 3 && day < 21) return 'th'
  switch (day % 10) {
    case 1: return 'st'
    case 2: return 'nd'
    case 3: return 'rd'
    default: return 'th'
  }
}

const today = new Date()
const day = today.getDate()
const daySuffix = getDaySuffix(day)
const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
const month = monthNames[today.getMonth()]
const year = today.getFullYear()

// To be changed to dynamic event name later
const eventName = ref('Hackathon @ SMU')

// To be changed to dynamic data later
const notCheckedInList = ref([
  { name: 'gyaltsen', email: 'gyaltsen@computing.smu' },
  { name: 'kevan', email: 'kevan@computing.smu' },
  { name: 'yan song', email: 'yansong@computing.smu' },
  { name: 'gerald', email: 'gerald@computing.smu' },
  { name: 'nicole', email: 'nicole@computing.smu' }
])
</script>

<style scoped>
.dashboard {
  font-family: serif;
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
}

.header h1 {
  font-size: 1.5rem;
  color: #5c3b00;
}

.date {
  color: #a16e00;
}

.refresh-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.refresh-container p {
  font-size: 1rem;
  margin: 0;
}

.refresh-btn {
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  transition: transform 0.2s;
}

.refresh-btn:hover {
  transform: rotate(90deg);
}

.section-title {
  color: rgb(43, 125, 226);
  font-size: 1.5rem;
  margin: 2rem 0 1rem;
}

.analytics-cards {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  justify-content: center;
}

.card {
  border: 2px solid black;
  border-radius: 4px;
  width: 200px;
  height: 150px;
  text-align: center;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.value {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.checked-in {
  color: green;
}

.not-checked-in {
  color: red;
}

.not-attending {
  color: orange;
}

.label {
  font-size: 1.2rem;
  color: black;
}

.not-checked-in-table {
  width: 100%;
  max-width: 100%;
  margin: 1rem auto 0;
  border-collapse: collapse;
  font-size: 1rem;
}

.not-checked-in-table th,
.not-checked-in-table td {
  border: 1px solid #ccc;
  padding: 0.5rem 1rem;
  text-align: left;
}

.not-checked-in-table th {
  background-color: #f0f0f0;
}

.not-checked-in-table button {
  padding: 0.3rem 0.6rem;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  background-color: #2c7be5;
  color: white;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.not-checked-in-table button:hover {
  background-color: #1a5fcc;
}

</style>

