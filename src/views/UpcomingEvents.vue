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
            <th>Participants</th> <!-- New column for participant count -->
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
            <td>{{ event.participant_count || 0 }}</td> <!-- Display participant count -->
          </tr>
          <tr v-if="filteredEvents.length === 0">
            <td colspan="4" style="text-align:center; color: #999;">No events found.</td>
          </tr>
        </tbody>
      </table>

      <!-- Message/Notification Box -->
      <div v-if="message" :class="['message-box', messageType]">
        {{ message }}
      </div>

      <div v-if="selectedEvent" class="participant-section">
        <h2>Participants for "{{ selectedEvent.name }}"</h2>

        <!-- Add Participant Form -->
        <div class="add-participant-form">
          <h3>Add New Participant</h3>
          <input
            type="text"
            v-model="newParticipantName"
            placeholder="Participant Name"
            class="form-input"
          />
          <input
            type="email"
            v-model="newParticipantEmail"
            placeholder="Participant Email"
            class="form-input"
          />
          <!-- Status will be 'Registered' by default as per backend logic for new registrations -->
          <button @click="addParticipant" class="add-button">Add Participant & Send QR</button>
        </div>

        <!-- Participants Table -->
        <table class="participants-table" v-if="participants.length">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="participant in participants" :key="participant.user_email">
              <td>{{ participant.name }}</td>
              <td>{{ participant.user_email }}</td>
              <td>{{ participant.status }}</td>
              <td>
                <button @click="showDeleteConfirm(participant)" class="delete-button">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-else>No participants found for this event.</p>
      </div>

      <!-- Delete Confirmation Modal -->
      <div v-if="showConfirmModal" class="modal-overlay">
        <div class="modal-content">
          <h3>Confirm Deletion</h3>
          <p>Are you sure you want to delete participant <strong>{{ participantToDelete.name }} ({{ participantToDelete.user_email }})</strong> from this event?</p>
          <div class="modal-actions">
            <button @click="deleteParticipantConfirmed" class="confirm-delete-button">Yes, Delete</button>
            <button @click="cancelDelete" class="cancel-button">Cancel</button>
          </div>
        </div>
      </div>

    </div>
  </Sidebar>
</template>

<script setup type="module">
import { ref, computed, onMounted, watch } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { supabase } from '../supabase.js' // Assuming supabase client is initialized here

// Reactive variables for events and participants
const events = ref([])
const selectedEvent = ref(null)
const participants = ref([])
const searchTerm = ref('')

// Reactive variables for new participant form
const newParticipantName = ref('')
const newParticipantEmail = ref('')
// newParticipantStatus is no longer directly set by user, backend will set to 'Registered'
// const newParticipantStatus = ref('Registered') // Default to 'Registered'

// Reactive variables for messages and confirmation modal
const message = ref('')
const messageType = ref('') // 'success' or 'error'
const showConfirmModal = ref(false)
const participantToDelete = ref(null)

// Computed property for filtering events based on search term
const filteredEvents = computed(() => {
  if (!searchTerm.value) return events.value
  const lower = searchTerm.value.toLowerCase()
  return events.value.filter(ev =>
    ev.name.toLowerCase().includes(lower) ||
    ev.location.toLowerCase().includes(lower)
  )
})

// Function to fetch events from Supabase and their participant counts
async function fetchEvents() {
  const { data: eventsData, error: eventsError } = await supabase
    .from('Events')
    .select('id, name, date, location') // Ensure 'location' is selected
    .gt('date', new Date().toISOString().slice(0, 10)) // Filter for upcoming events
    .order('date', { ascending: true });

  if (eventsError) {
    console.error('Error fetching events:', eventsError);
    showMessage('Error fetching events.', 'error');
  } else {
    // Fetch participant count for each event
    const eventsWithCounts = await Promise.all(eventsData.map(async (event) => {
      const { count, error: countError } = await supabase
        .from('Event_attendees')
        .select('count', { head: true, count: 'exact' })
        .eq('event_id', event.id);

      if (countError) {
        console.error(`Error fetching participant count for event ${event.id}:`, countError);
        return { ...event, participant_count: 0 }; // Default to 0 on error
      }
      return { ...event, participant_count: count };
    }));

    events.value = eventsWithCounts;
    console.log('Fetched events data with counts:', eventsWithCounts);
  }
}

// Function to fetch participants for a specific event_id from Supabase
async function fetchParticipants(eventId) {
  const { data, error } = await supabase
    .from('Event_attendees')
    .select('name, user_email, status')
    .eq('event_id', eventId);

  if (error) {
    console.error('Error fetching participants:', error);
    showMessage('Error fetching participants.', 'error');
    return [];
  } else {
    return data;
  }
}

// Function to select an event and fetch its participants
async function selectEvent(event) {
  if (selectedEvent.value && selectedEvent.value.id === event.id) {
    selectedEvent.value = null;
    participants.value = [];
  } else {
    selectedEvent.value = event;
    participants.value = await fetchParticipants(event.id) || [];
  }
  // Clear any previous messages when a new event is selected
  clearMessage();
  // Reset new participant form fields
  newParticipantName.value = '';
  newParticipantEmail.value = '';
}

// Function to format date strings
function formatDate(dateStr) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString(undefined, options)
}

// Function to add a new participant and trigger QR code generation/email sending via backend
async function addParticipant() {
  if (!selectedEvent.value) {
    showMessage('Please select an event first.', 'error');
    return;
  }
  if (!newParticipantName.value || !newParticipantEmail.value) {
    showMessage('Participant Name and Email are required.', 'error');
    return;
  }

  // Call the Flask backend to handle participant registration, QR generation, and email sending
  try {
    const response = await fetch('http://localhost:5000/send_email_python', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        attendeeName: newParticipantName.value,
        attendeeEmail: newParticipantEmail.value,
        eventName: selectedEvent.value.name, // Assuming event_name is used as event_id in backend
        eventDate: selectedEvent.value.date,
        eventLocation: selectedEvent.value.location,
      }),
    });

    const result = await response.json();

    if (response.ok) {
      showMessage(`Participant added and QR email sent: ${result.message}`, 'success');
      // Clear form fields
      newParticipantName.value = '';
      newParticipantEmail.value = '';
      // Refresh participants list for the current event
      participants.value = await fetchParticipants(selectedEvent.value.id) || [];
      // Also refresh events to update participant count
      await fetchEvents();
    } else {
      showMessage(`Error adding participant: ${result.message}`, 'error');
      console.error('Backend error:', result.message);
    }
  } catch (e) {
    console.error('Network or unexpected error calling backend:', e);
    showMessage(`Failed to connect to backend or unexpected error: ${e.message}`, 'error');
  }
}

// Function to show the delete confirmation modal
function showDeleteConfirm(participant) {
  participantToDelete.value = participant;
  showConfirmModal.value = true;
}

// Function to confirm and delete the participant
async function deleteParticipantConfirmed() {
  if (!selectedEvent.value || !participantToDelete.value) {
    showMessage('No event or participant selected for deletion.', 'error');
    return;
  }

  const { error } = await supabase
    .from('Event_attendees')
    .delete()
    .eq('event_id', selectedEvent.value.id)
    .eq('user_email', participantToDelete.value.user_email); // Use user_email as identifier

  if (error) {
    console.error('Error deleting participant:', error);
    showMessage(`Error deleting participant: ${error.message}`, 'error');
  } else {
    showMessage('Participant deleted successfully!', 'success');
    // Refresh participants list for the current event
    participants.value = await fetchParticipants(selectedEvent.value.id) || [];
    // Also refresh events to update participant count
    await fetchEvents();
  }
  // Close the modal regardless of success or failure
  cancelDelete();
}

// Function to cancel the delete operation
function cancelDelete() {
  showConfirmModal.value = false;
  participantToDelete.value = null;
}

// Function to display messages
function showMessage(msg, type) {
  message.value = msg;
  messageType.value = type;
  setTimeout(() => {
    clearMessage();
  }, 5000); // Message disappears after 5 seconds
}

// Function to clear messages
function clearMessage() {
  message.value = '';
  messageType.value = '';
}

// Fetch events from Supabase when the component is mounted
onMounted(() => {
  fetchEvents();
});
</script>

<style scoped>
.upcoming-events-page {
  max-width: 800px;
  margin: 2rem auto;
  font-family: 'Inter', sans-serif; /* Using Inter font */
  padding: 1rem;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

h1 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 2.2rem;
  font-weight: 700;
}

h2 {
  color: #34495e;
  margin-top: 2.5rem;
  margin-bottom: 1rem;
  font-size: 1.8rem;
  font-weight: 600;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 0.5rem;
}

h3 {
  color: #34495e;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-size: 1.5rem;
  font-weight: 500;
}

.search-input,
.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  margin-bottom: 1rem;
  font-size: 1rem;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  box-sizing: border-box;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.search-input:focus,
.form-input:focus {
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
  outline: none;
}

.events-table,
.participants-table {
  width: 100%;
  border-collapse: separate; /* Use separate for rounded corners on cells */
  border-spacing: 0; /* Remove space between cells */
  margin-top: 1.5rem;
  border-radius: 10px;
  overflow: hidden; /* Ensures rounded corners apply to content */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.events-table th,
.events-table td,
.participants-table th,
.participants-table td {
  padding: 1rem 1.2rem;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.events-table th,
.participants-table th {
  background-color: #ecf0f1;
  color: #2c3e50;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.9rem;
}

/* Specific rounded corners for table headers */
.events-table thead tr th:first-child,
.participants-table thead tr th:first-child {
  border-top-left-radius: 10px;
}
.events-table thead tr th:last-child,
.participants-table thead tr th:last-child {
  border-top-right-radius: 10px;
}

.events-table tbody tr:last-child td,
.participants-table tbody tr:last-child td {
  border-bottom: none; /* No border for the last row */
}

.events-table tr.selected {
  background-color: #e8f5fd; /* Lighter blue for selected row */
  font-weight: 500;
}

.events-table tr:hover {
  background-color: #f8fcff; /* Very light blue on hover */
  cursor: pointer;
}

.participant-section {
  margin-top: 2.5rem;
  background-color: #f9fbfd;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.add-participant-form {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
}

.add-button, .delete-button, .confirm-delete-button, .cancel-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.add-button {
  background-color: #28a745; /* Green */
  color: white;
  margin-top: 1rem;
  width: 100%;
}

.add-button:hover {
  background-color: #218838;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.delete-button {
  background-color: #dc3545; /* Red */
  color: white;
  padding: 0.5rem 1rem; /* Smaller padding for table button */
  font-size: 0.9rem;
}

.delete-button:hover {
  background-color: #c82333;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Message Box Styling */
.message-box {
  padding: 0.8rem 1.2rem;
  margin-top: 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  text-align: center;
  opacity: 1;
  transition: opacity 0.5s ease-in-out;
}

.message-box.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message-box.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

/* Modal Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
  text-align: center;
  max-width: 450px;
  width: 90%;
  animation: fadeIn 0.3s ease-out;
}

.modal-content h3 {
  margin-top: 0;
  color: #2c3e50;
  font-size: 1.8rem;
}

.modal-content p {
  margin-bottom: 2rem;
  color: #555;
  line-height: 1.6;
  font-size: 1.1rem;
}

.modal-actions button {
  margin: 0 0.75rem;
  padding: 0.8rem 1.8rem;
  font-size: 1rem;
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
}

.confirm-delete-button {
  background-color: #dc3545;
  color: white;
}

.confirm-delete-button:hover {
  background-color: #c82333;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.cancel-button {
  background-color: #6c757d; /* Grey */
  color: white;
}

.cancel-button:hover {
  background-color: #5a6268;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .upcoming-events-page {
    margin: 1rem auto;
    padding: 0.75rem;
  }

  h1 {
    font-size: 1.8rem;
  }

  h2 {
    font-size: 1.5rem;
  }

  h3 {
    font-size: 1.3rem;
  }

  .events-table th,
  .events-table td,
  .participants-table th,
  .participants-table td {
    padding: 0.75rem 0.8rem;
    font-size: 0.9rem;
  }

  .add-button, .delete-button, .confirm-delete-button, .cancel-button {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }

  .modal-content {
    padding: 1.5rem;
  }

  .modal-actions button {
    margin: 0.5rem 0.5rem;
  }
}

@media (max-width: 480px) {
  .events-table, .participants-table {
    font-size: 0.85rem;
  }

  .search-input, .form-input {
    padding: 0.6rem 0.8rem;
    font-size: 0.9rem;
  }

  .add-button {
    padding: 0.6rem 1rem;
  }
}
</style>
