<template>
  <div class="page-center">
    <div class="signup-container">
      <h2>Create Free Account</h2>

      <!-- General error/success message display -->
      <div v-if="message" :class="['message', messageType]">{{ message }}</div>

      <form @submit.prevent="handleSignup">
        <!-- Client-side validation errors still work as before -->
      
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            placeholder="Your email address">
          <div class="error-message" v-if="errors.email">{{ errors.email }}</div>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="Create a password (min. 8 characters)">
          <div class="error-message" v-if="errors.password">{{ errors.password }}</div>
        </div>

        <!-- UPDATED: Button is disabled during loading -->
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth' // 1. Import store

// 2. Instantiate store and router
const authStore = useAuthStore()
const router = useRouter()

// --- State for the component ---

const email = ref('')
const password = ref('')

// For client-side validation errors
const errors = ref({ email: '', password: '' })
// For API loading state and server messages
const loading = ref(false)
const message = ref(null) // Can be used for success or error messages from the server
const messageType = ref('') // 'success' or 'error'

// --- Functions ---
const validEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)

// 3. UPDATED: handleSignup is now async and uses the store
const handleSignup = async () => {
  // --- A. Client-side validation (good practice to keep this) ---
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
  if (!isValid) return // Stop if client-side validation fails

  // --- B. API call to Supabase via Pinia store ---
  loading.value = true
  try {
    // Call the signUp action from the store, passing the username as metadata
    await authStore.signUp(email.value, password.value)
    
    // Set a success message
    messageType.value = 'success'
    message.value = "Account created successfully! Please check your email to confirm your account before logging in."

    // Redirect to login page after a short delay
    setTimeout(() => {
      router.push({ path: '/' }) // Redirect to login page
    }, 4000)

  } catch (error) {
    // Display errors from the server (e.g., "User already registered")
    messageType.value = 'error'
    message.value = error.message || 'An unexpected error occurred during signup.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Your excellent styles are kept, with minor additions */

.message {
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 1rem;
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

.login-link {
    margin-top: 1.5rem;
    font-size: 0.9rem;
}
.login-link a {
    color: #4285f4;
    font-weight: 500;
    text-decoration: none;
}

button:disabled {
  background-color: #9ec2f8;
  cursor: not-allowed;
}

/* --- Unchanged Styles --- */
.signup-container {
  background-color: white;
  padding: 2rem 2.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}
h2 {
  color: #333;
  margin-bottom: 1.5rem;
}
.form-group {
  margin-bottom: 1.2rem;
  text-align: left;
}
label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}
input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box;
  font-size: 1rem;
}
input:focus {
  border-color: #4285f4;
  outline: none;
  box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2);
}
button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  margin-top: 0.5rem;
  transition: background-color 0.3s;
}
button:hover {
  background-color: #3367d6;
}
.error-message {
  color: #d32f2f;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}
.page-center {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 1rem;
}
</style>