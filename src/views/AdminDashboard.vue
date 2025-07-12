<template>
  <Sidebar>
    <div class="admin-dashboard">
      <h1 class="dashboard-title">My CCAs</h1>

      <div v-if="loading" class="loading">Loading CCAs...</div>
      <div v-else-if="ccas.length === 0" class="empty">You are not linked to any CCAs.</div>

      <div v-else class="cca-grid">
        <div v-for="cca in ccas" :key="cca.id" class="cca-card">
          <h2>{{ cca.Organisation_name }}</h2>
          <p><strong>CCA ID:</strong> {{ cca.id }}</p>
          <button @click="goToAddEvent(cca)">Add Event</button>
        </div>
      </div>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../supabase.js'
import Sidebar from '../components/Sidebar.vue'

const router = useRouter()
const loading = ref(true)
const ccas = ref([])

const fetchAdminCcas = async () => {
  loading.value = true

  // Step 1: Get current user
  const {
    data: { user },
    error: userError,
  } = await supabase.auth.getUser()

  if (userError || !user) {
    console.error('Unable to fetch user', userError)
    loading.value = false
    return
  }

  // Step 2: Fetch linked CCAs from admin_organisation
  const { data, error } = await supabase
  .from('Admin_Organisations')
  .select(`
    id,
    organisation_id,
    organisations:organisation_id (id, Organisation_name)
  `)
  .eq('admin_email', user.email)

  if (error) {
    console.error('Error fetching admin CCAs:', error)
    loading.value = false
    return
  }

  // Step 3: Extract and store CCAs
  ccas.value = data.map((item) => item.organisations)
  loading.value = false
}

// Navigate to Add Event page
const goToAddEvent = (cca) => {
  router.push({
    name: 'AddEvent',
    query: {
      org_id: cca.id,
      org_name: cca.Organisation_name,
    },
  })
}

// Run on component mount
onMounted(() => {
  fetchAdminCcas()
})
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
  font-family: sans-serif;
}

.dashboard-title {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.loading,
.empty {
  font-size: 1.2rem;
  color: #888;
  margin-top: 1rem;
}

.cca-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}

.cca-card {
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  text-align: center;
}

.cca-card h2 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.cca-card button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #2c7be5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cca-card button:hover {
  background: #1a5fcc;
}
</style>

