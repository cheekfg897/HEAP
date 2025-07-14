<template>
  <Sidebar>
    <div class="dashboard">
      <div class="header">
        <h1>
          Today's Event :
          <span class="date"
            >{{ day }}<sup>{{ daySuffix }}</sup> {{ month }} {{ year }}</span
          >,
          {{ eventName || 'No Event Scheduled Today' }}
        </h1>
        <div class="refresh-container">
          <p>Last Updated {{ updatedTime }}</p>
          <button class="refresh-btn" @click="refresh">🔄</button>
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
          <tr v-if="notCheckedInList.length === 0">
            <td colspan="3" style="text-align: center; color: #999;">No participants not checked in.</td>
          </tr>
          <tr v-for="person in notCheckedInList" :key="person.id">
            <td>{{ person.name }}</td>
            <td>{{ person.user_email }}</td>
            <td>
            <button @click="sendEmail(person.user_email, eventName)">
              Email
            </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </Sidebar>
</template>
<script>
async function sendEmail(email, eventTitle) {
  try {
    const response = await fetch('http://localhost:5000/send_email_reminder', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        recipient: email,
        eventName: eventTitle
      })
    });

    const data = await response.json();

    if (response.ok) {
      alert('✅ Email sent: ' + data.message);
    } else {
      alert('❌ Failed to send email: ' + data.message);
    }
  } catch (error) {
    alert('❌ Request error occurred');
    console.error(error);
  }
}
</script>

<script setup>
// CHANGED: Import onMounted
import { ref, onMounted } from 'vue';
import Sidebar from '../components/Sidebar.vue';
// ADDED: Supabase client import
// !!! IMPORTANT: Adjust this path if your supabase.js is NOT in src/lib/
import { supabase } from '../supabase.js';

// CHANGED: Initialize refs with default/loading values for dynamic data
const eventName = ref('Loading Event...');
const checkedIn = ref(0);
const notCheckedIn = ref(0);
const notAttending = ref(0);
const notCheckedInList = ref([]);
const updatedTime = ref('...'); // CHANGED: Initialize for loading state

// CHANGED: Removed hardcoded static data
// const checkedIn = ref(79)
// const notCheckedIn = ref(22)
// const notAttending = ref(3)
// const notCheckedInList = ref([ /* ... */ ])
// const eventName = ref('Hackathon @ SMU')

// Remaining date formatting helpers are unchanged
function getDaySuffix(day) {
  if (day > 3 && day < 21) return 'th';
  switch (day % 10) {
    case 1:
      return 'st';
    case 2:
      return 'nd';
    case 3:
      return 'rd';
    default:
      return 'th';
  }
}

const today = new Date(); // Current date (2025-07-02 as of your context)
const day = today.getDate();
const daySuffix = getDaySuffix(day);
const monthNames = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
];
const month = monthNames[today.getMonth()];
const year = today.getFullYear();



// ADDED: Helper function to format today's date for Supabase query
function getTodayDateFormatted() {
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
  const day = String(today.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`; // Format: YYYY-MM-DD
}

// ADDED: Main asynchronous function to fetch all dashboard data
async function fetchDashboardData() {
  updatedTime.value = 'Fetching...'; // Set loading state for update time

  const todayFormatted = getTodayDateFormatted();

  let currentEventId = null;

  // 1. Fetch Today's Event
  // !!! IMPORTANT: Ensure 'events' is the EXACT case of your table name in Supabase
  // !!! IMPORTANT: Ensure 'name' and 'date' are the EXACT case of your column names
  // !!! IMPORTANT: Ensure your 'date' column in Supabase is of type 'date' or 'timestamp without time zone'
  const { data: eventData, error: eventError } = await supabase
    .from('Events') // !!! VERIFY: Table name case (e.g., 'events' vs 'Events')
    .select('id, name') // Select 'id' (for linking participants) and 'name'
    .eq('date', '2025-07-02') // Filter by today's date
    .maybeSingle(); // Expecting at most one event for today

  if (eventError) {
    console.error('Error fetching today\'s event:', eventError);
    eventName.value = 'Error loading event'; // Indicate error to user
  } else if (eventData) {
    eventName.value = eventData.name;
    currentEventId = eventData.id;
    console.log("Today's Event Data:", eventData); // ADDED: Debugging log
  } else {
    // No event found for today
    eventName.value = 'No Event Scheduled Today';
    // Reset participant data if no event found
    checkedIn.value = 0;
    notCheckedIn.value = 0;
    notAttending.value = 0;
    notCheckedInList.value = [];
    updatedTime.value = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    return; // Exit function early as no event means no participants to fetch
  }

  // 2. Fetch Participants for the current event (only if an event was found)
  if (currentEventId) {
    // !!! IMPORTANT: Ensure 'participants' is the EXACT case of your table name in Supabase
    // !!! IMPORTANT: Ensure 'event_id', 'name', 'email', 'status' are the EXACT case of your column names
    const { data: participantsData, error: participantsError } = await supabase
      .from('Event_attendees') // !!! VERIFY: Table name case (e.g., 'participants' vs 'Participants')
      .select('event_id, name, user_email, status') // Select necessary participant columns including 'id'
      .eq('event_id', currentEventId); // Filter by the found event's ID

    console.log(participantsData)

    if (participantsError) {
      console.error('Error fetching participants:', participantsError);
      // Reset counts/list on error
      checkedIn.value = 0;
      notCheckedIn.value = 0;
      notAttending.value = 0;
      notCheckedInList.value = [];
    } else {
      // Initialize counts and list
      let checkedInCount = 0;
      let notCheckedInCount = 0;
      let notAttendingCount = 0;
      const tempNotCheckedInList = [];

      // Loop through participants to categorize them
      participantsData.forEach((p) => {
        // !!! IMPORTANT: Adjust these status strings to EXACTLY match your 'status' values in Supabase
        if (p.status === 'Checked In') { // Example status
          checkedInCount++;
        } else if (p.status === 'Registered') { // Example status for those not yet arrived
          notCheckedInCount++;
          tempNotCheckedInList.push(p);
        } else if (p.status === 'Not Attending') { // Example status
          notAttendingCount++;
        }
        // Add more status conditions if you have other categories
      });

      // Update reactive refs
      checkedIn.value = checkedInCount;
      notCheckedIn.value = notCheckedInCount;
      notAttending.value = notAttendingCount;
      notCheckedInList.value = tempNotCheckedInList;
      console.log("Participants Data:", participantsData); // ADDED: Debugging log
    }
  }

  // Update last updated time after all fetches are complete
  updatedTime.value = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// CHANGED: Refresh function now calls the new data fetching function
const refresh = () => {
  fetchDashboardData();
};

// ADDED: Call fetchDashboardData when the component is mounted
onMounted(() => {
  fetchDashboardData();
});
</script>

<style scoped>
/* Your existing styles are unchanged */
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