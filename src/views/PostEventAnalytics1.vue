<template>
  <Sidebar>
    <div style="padding: 20px; font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto;">
      <h1 style="color: #333; margin-bottom: 20px;">📊 Past Events Analytics</h1>

      <div style="margin: 1rem 0; display: flex; gap: 5px; align-items: center;">
        <input
          type="text"
          placeholder="Quick Search"
          v-model="searchQuery"
          @keyup.enter="handleSearch"
          style="padding: 8px; border: 1px solid #ccc; border-radius: 4px; flex: 1; max-width: 300px;"
        />
        <button @click="handleSearch" style="padding: 8px 12px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; background: #f8f9fa;">
          🔍
        </button>
        <button @click="clearSearch" style="padding: 8px 12px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; background: #f8f9fa;">
          ❌
        </button>
      </div>

      <div style="margin: 1rem 0; display: flex; gap: 10px; flex-wrap: wrap;">
        <button @click="saveCSV" style="padding: 8px 12px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; background: #f8f9fa; display: flex; align-items: center; gap: 5px;">
          💾 Save CSV
        </button>
        <button @click="toggleFilter" style="padding: 8px 12px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; background: #f8f9fa; display: flex; align-items: center; gap: 5px;">
          🔽 Filter
        </button>
        <button @click="showAll" style="padding: 8px 12px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; background: #f8f9fa; display: flex; align-items: center; gap: 5px;">
          👁️ Show All
        </button>
      </div>

      <div style="overflow-x: auto; border: 1px solid #ddd; border-radius: 4px;">
        <table style="width: 100%; border-collapse: collapse; background: white;">
          <thead>
            <tr style="background-color: #f5f5f5;">
              <th style="padding: 12px; border-bottom: 2px solid #ddd; width: 50px; text-align: center;">
                <input
                  type="checkbox"
                  @change="selectAll"
                  :checked="allSelected"
                  style="cursor: pointer;"
                />
              </th>
              <th style="padding: 12px; border-bottom: 2px solid #ddd; text-align: left;">Event Name</th>
              <th style="padding: 12px; border-bottom: 2px solid #ddd; text-align: left;">Date</th>
              <th style="padding: 12px; border-bottom: 2px solid #ddd; text-align: left;">Analytics</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="event in filteredEvents" :key="event.id" style="border-bottom: 1px solid #eee;" @mouseover="$event.target.style.backgroundColor='#f9f9f9'" @mouseout="$event.target.style.backgroundColor='white'">
              <td style="padding: 12px; text-align: center;">
                <input
                  type="checkbox"
                  :value="event.id"
                  v-model="selectedEvents"
                  style="cursor: pointer;"
                />
              </td>
              <td style="padding: 12px; font-weight: 500;">{{ event.name }}</td>
              <td style="padding: 12px; color: #666;">{{ event.date }}</td>
              <td style="padding: 12px;">
                <a href="#" @click.prevent="viewAnalytics(event)" style="color: #007bff; text-decoration: none; font-weight: 500;">
                  View Here
                </a>
              </td>
            </tr>
            <tr v-if="filteredEvents.length === 0">
              <td colspan="4" style="text-align: center; color: #666; padding: 40px; font-style: italic;">
                No events found matching your search
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p style="margin-top: 15px; color: #666; font-size: 14px;">
        Records {{ startRecord }} to {{ endRecord }} of {{ totalRecords }}
        <span v-if="selectedEvents.length > 0" style="margin-left: 20px; color: #007bff;">
          ({{ selectedEvents.length }} selected)
        </span>
      </p>

      <div v-if="showAnalyticsModal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000;" @click="closeAnalytics">
        <div @click.stop style="background: white; padding: 30px; border-radius: 8px; max-width: 500px; width: 90%; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
          <h3 style="margin-top: 0; color: #333; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;">📈 Analytics for {{ selectedEvent?.name }}</h3>
          <div style="margin: 20px 0;">
            <p style="margin: 10px 0;"><strong>Date:</strong> {{ selectedEvent?.date }}</p>
            <p style="margin: 10px 0;"><strong>Attendees:</strong> {{ selectedEvent?.attendees || 'N/A' }}</p>
            <p style="margin: 10px 0;"><strong>Engagement:</strong> {{ selectedEvent?.engagement || 'N/A' }}</p>
            <p style="margin: 10px 0;"><strong>Status:</strong> <span style="color: #28a745; font-weight: bold;">Completed</span></p>
          </div>
          <div style="text-align: right; margin-top: 20px;">
            <button @click="closeAnalytics" style="padding: 10px 20px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; background: #f8f9fa; margin-right: 10px;">
              Close
            </button>
            <button style="padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; background: #007bff; color: white;">
              View Full Report
            </button>
          </div>
        </div>
      </div>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref, computed } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { createClient } from '@supabase/supabase-js' // Import createClient

// Initialize Supabase using environment variables
// IMPORTANT: Ensure your .env file has VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY
// Example .env content:
// VITE_SUPABASE_URL="https://your-project-ref.supabase.co"
// VITE_SUPABASE_ANON_KEY="your-anon-public-key"
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY
const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Reactive data
const searchQuery = ref('')
const selectedEvents = ref([])
const showAnalyticsModal = ref(false)
const selectedEvent = ref(null)

// Sample events data
// TODO: Replace this with data fetched from Supabase once the connection is verified.
const events = ref([
  { id: 1, name: 'SMU Flag Off', date: '2024-06-01', attendees: 150, engagement: '85%' },
  { id: 2, name: 'Annual Conference 2024', date: '2024-05-15', attendees: 300, engagement: '92%' },
  { id: 3, name: 'Tech Workshop Series', date: '2024-04-20', attendees: 75, engagement: '78%' },
  { id: 4, name: 'Student Orientation', date: '2024-03-10', attendees: 200, engagement: '88%' },
  { id: 5, name: 'Career Fair 2024', date: '2024-02-28', attendees: 450, engagement: '94%' },
  { id: 6, name: 'Alumni Networking Night', date: '2024-01-15', attendees: 120, engagement: '82%' }
])

// Computed properties
const filteredEvents = computed(() => {
  if (!searchQuery.value.trim()) return events.value
  const query = searchQuery.value.toLowerCase()
  return events.value.filter(event =>
    event.name.toLowerCase().includes(query) || event.date.includes(query)
  )
})

const allSelected = computed(() =>
  filteredEvents.value.length > 0 &&
  selectedEvents.value.length === filteredEvents.value.length
)

const totalRecords = computed(() => filteredEvents.value.length)
const startRecord = computed(() => totalRecords.value > 0 ? 1 : 0)
const endRecord = computed(() => totalRecords.value)

// Methods
const handleSearch = () => {
  console.log('Searching for:', searchQuery.value)
  // In a real application, you'd trigger a data fetch from Supabase here
  // based on the search query.
}

const clearSearch = () => {
  searchQuery.value = ''
  selectedEvents.value = []
  // In a real application, you might re-fetch all data from Supabase here.
}

const selectAll = (event) => {
  selectedEvents.value = event.target.checked
    ? filteredEvents.value.map(e => e.id)
    : []
}

const saveCSV = () => {
  const csvContent = [
    ['Event Name', 'Date', 'Attendees', 'Engagement'],
    ...filteredEvents.value.map(e => [
      e.name,
      e.date,
      e.attendees || 'N/A',
      e.engagement || 'N/A'
    ])
  ].map(row => row.join(',')).join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'events-analytics.csv'
  a.click()
  URL.revokeObjectURL(url)
}

const toggleFilter = () => {
  alert('Filter functionality can be expanded here!')
  // This is where you would implement more advanced filtering,
  // potentially interacting with Supabase to filter data.
}

const showAll = () => {
  searchQuery.value = ''
  selectedEvents.value = []
  // If data is fetched from Supabase, this would trigger a re-fetch without filters.
}

const viewAnalytics = (event) => {
  selectedEvent.value = event
  showAnalyticsModal.value = true
}

const closeAnalytics = () => {
  showAnalyticsModal.value = false
  selectedEvent.value = null
}

// You can now use the 'supabase' client to interact with your Supabase database.
// For example, to fetch data when the component is mounted:
/*
import { onMounted } from 'vue'

onMounted(async () => {
  try {
    const { data, error } = await supabase
      .from('your_events_table_name') // Replace with your actual table name
      .select('*')

    if (error) {
      console.error('Error fetching events:', error.message)
    } else {
      events.value = data // Update your reactive 'events' data with fetched data
    }
  } catch (err) {
    console.error('An unexpected error occurred:', err)
  }
})
*/
</script>

<style scoped>
/* You can add or modify styles here if needed. */
/* The provided template uses inline styles, but for larger projects,
   it's better to use <style scoped> or external CSS files. */
</style>