<template>
  <div class="page-center">
    <div class="signup-container">
      <h2>Create Free Account</h2>

      <div v-if="message" :class="['message', messageType]">{{ message }}</div>

      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            placeholder="Your email address" />
          <div class="error-message" v-if="errors.email">{{ errors.email }}</div>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="Create a password (min. 8 characters)" />
          <div class="error-message" v-if="errors.password">{{ errors.password }}</div>
        </div>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Creating...' : 'Create Account' }}
        </button>
      </form>

      <div class="login-link">
        <p>Already have an account? <router-link to="/">Log In</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { supabase } from '../supabase'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const selectedCcas = ref([])
const organisations = ref([])

const errors = ref({ email: '', password: '' })
const loading = ref(false)
const message = ref(null)
const messageType = ref('')

// Fetch all CCA organisations on mount
onMounted(async () => {
  const { data, error } = await supabase.from('organisations').select('*')
  if (error) {
    console.error('Failed to load organisations:', error)
    message.value = 'Could not load CCA list.'
    messageType.value = 'error'
  } else {
    organisations.value = data
  }
})

const validEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)

const handleSignup = async () => {
  errors.value = { email: '', password: '' }
  message.value = null
  let isValid = true

  if (!email.value || !validEmail(email.value)) {
    errors.value.email = 'Please enter a valid email'
    isValid = false
  }
  if (!password.value || password.value.length < 8) {
    errors.value.password = 'Password must be at least 8 characters'
    isValid = false
  }
  if (selectedCcas.value.length === 0) {
    messageType.value = 'error'
    message.value = 'Please select at least one CCA.'
    return
  }
  if (!isValid) return

  loading.value = true
  try {
    const { user, error } = await authStore.signUp(email.value, password.value)
    if (error) throw error

    // After account creation, insert CCA links to Admin_Organisations
    const inserts = selectedCcas.value.map((cca) => ({
      admin_email: email.value,
      organisation_id: cca.id
    }))

    const { error: insertError } = await supabase.from('Admin_Organisations').insert(inserts)
    if (insertError) throw insertError

    messageType.value = 'success'
    message.value = "Account created successfully! Please check your email to confirm your account."

    setTimeout(() => {
      router.push({ path: '/' })
    }, 3000)

  } catch (error) {
    messageType.value = 'error'
    message.value = error.message || 'An unexpected error occurred during signup.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page-center {
  display: flex;
  justify-content: center;
  padding: 4rem 2rem;
}

.signup-container {
  width: 100%;
  max-width: 420px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.signup-container h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: 600;
}

input {
  width: 100%;
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

.error-message {
  color: red;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  background: #2c7be5;
  color: #fff;
  font-size: 1.1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background: #1a5fcc;
}

.message {
  margin-bottom: 1rem;
  padding: 0.75rem;
  border-radius: 6px;
  text-align: center;
}
.message.success {
  background: #e0f7e9;
  color: #0a8740;
}
.message.error {
  background: #ffe4e1;
  color: #c0392b;
}

.login-link {
  margin-top: 1rem;
  text-align: center;
}
</style>
