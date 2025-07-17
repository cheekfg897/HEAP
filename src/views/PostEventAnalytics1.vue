<template>
  <Sidebar>
    <div style="padding: 20px; font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto;">
      <h1 style="color: #333; margin-bottom: 20px;">📊 Past Events Analytics</h1>

      <!-- Loading Indicator -->
      <div v-if="isLoading" style="text-align: center; padding: 20px; color: #007bff;">
        Loading analytics data...
      </div>
      <div v-if="error" style="text-align: center; padding: 20px; color: #dc3545;">
        Error: {{ error }}
      </div>

      <!-- Search Section -->
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

      <!-- Action Buttons -->
      <div style="margin: 1rem 0; display: flex; gap: 10px; flex-wrap: wrap;">
        <button @click="saveCSV" style="padding: 8px 12px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; background: #f8f9fa; display: flex; align-items: center; gap: 5px;">
          💾 Save CSV
        </button>
        <button @click="showAll" style="padding: 8px 12px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; background: #f8f9fa; display: flex; align-items: center; gap: 5px;">
          👁️ Show All
        </button>
      </div>

      <!-- Data Table -->
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
              <th style="padding: 12px; border-bottom: 2px solid #ddd; text-align: left;">Attendees</th>
              <th style="padding: 12px; border-bottom: 2px solid #ddd; text-align: left;">Engagement</th>
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
              <td style="padding: 12px; color: #666;">{{ event.attendees || 'N/A' }}</td>
              <td style="padding: 12px; color: #666;">{{ event.engagement || 'N/A' }}</td>
              <td style="padding: 12px;">
                <a href="#" @click.prevent="viewAnalytics(event)" style="color: #007bff; text-decoration: none; font-weight: 500;">
                  View Here
                </a>
              </td>
            </tr>
            <tr v-if="filteredEvents.length === 0 && !isLoading">
              <td colspan="6" style="text-align: center; color: #666; padding: 40px; font-style: italic;">
                No events found matching your search
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Records Counter -->
      <p style="margin-top: 15px; color: #666; font-size: 14px;">
        Records {{ startRecord }} to {{ endRecord }} of {{ totalRecords }}
        <span v-if="selectedEvents.length > 0" style="margin-left: 20px; color: #007bff;">
          ({{ selectedEvents.length }} selected)
        </span>
      </p>

      <!-- Analytics Modal -->
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
import { ref, computed, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { createClient } from '@supabase/supabase-js'

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
const events = ref([]) // Initialize as empty, data will be fetched
const isLoading = ref(true) // Loading state
const error = ref(null) // Error state

// Function to fetch and process event analytics
const fetchEventsAnalytics = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    // Get current date in YYYY-MM-DD format for comparison
    const currentDate = new Date().toISOString().split('T')[0];

    // 1. Fetch past events from the 'Events' table
    const { data: eventsData, error: eventsError } = await supabase
      .from('Events') // Replace with your actual Events table name
      .select('id, name, date')
      .lt('date', currentDate); // Filter for events whose date is in the past

    if (eventsError) {
      throw new Error(`Error fetching events: ${eventsError.message}`);
    }

    const processedEvents = [];

    // 2. For each past event, fetch attendee data and calculate analytics
    for (const event of eventsData) {
      const { data: attendeesData, error: attendeesError } = await supabase
        .from('Event_attendees') // Replace with your actual Event_attendees table name
        .select('status') // Select the 'status' column
        .eq('event_id', event.id); // Filter by the current event's ID

      if (attendeesError) {
        console.error(`Error fetching attendees for event ${event.id}: ${attendeesError.message}`);
        // Continue to next event even if there's an error for this one
        processedEvents.push({
          id: event.id,
          name: event.name,
          date: event.date,
          attendees: 'N/A',
          engagement: 'N/A',
        });
        continue;
      }

      const totalAttendees = attendeesData.length;
      // Count how many attendees have a 'status' of "Checked In"
      const checkedIns = attendeesData.filter(attendee => attendee.status === 'Checked In').length;

      let engagementPercentage = 'N/A';
      if (totalAttendees > 0) {
        engagementPercentage = ((checkedIns / totalAttendees) * 100).toFixed(2) + '%';
      }

      processedEvents.push({
        id: event.id,
        name: event.name,
        date: event.date,
        attendees: checkedIns, // Number of checked-in attendees
        engagement: engagementPercentage,
      });
    }

    events.value = processedEvents;
  } catch (err) {
    console.error('An unexpected error occurred during data fetch:', err);
    error.value = err.message;
  } finally {
    isLoading.value = false;
  }
};

// Fetch data when the component is mounted
onMounted(() => {
  fetchEventsAnalytics();
});

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
  // The computed property `filteredEvents` will automatically react to searchQuery changes.
  // No explicit re-fetch from Supabase is needed here unless you want server-side searching.
}

const clearSearch = () => {
  searchQuery.value = ''
  selectedEvents.value = []
  // The computed property `filteredEvents` will automatically react.
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
  // Use a custom modal or UI element instead of `alert()` for better user experience.
  // For now, keeping the alert as per original code.
  alert('Filter functionality can be expanded here!')
}

const showAll = () => {
  searchQuery.value = ''
  selectedEvents.value = []
  // This will reset the search filter, and the computed `filteredEvents` will show all.
}

const viewAnalytics = (event) => {
  selectedEvent.value = event
  showAnalyticsModal.value = true
}

const closeAnalytics = () => {
  showAnalyticsModal.value = false
  selectedEvent.value = null
}
</script>

<style scoped>
/*
  You can add or modify styles here if needed.
  The provided template uses inline styles, which are generally not recommended
  for larger projects. For better maintainability, consider moving styles
  to this <style scoped> block or an external CSS file.
*/
</style>
