<template>
  <div class="login-page-container">
    <!-- Left side - Image -->
    <div class="image-side">
      <img src="../assets/Events.svg" alt="University Campus" class="background-image" />
    </div>

    <!-- Right side - Login Form -->
    <div class="form-side">
      <div class="login-container">
        <h2>Login</h2>

        <!-- General error message for login failures -->
        <div v-if="loginError" class="error-message general-error">{{ loginError }}</div>
        
        <form @submit.prevent="handleLogin">
          <!-- UPDATED: Changed from username to email -->
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="Enter your email"
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Enter your password"
            />
          </div>

          <div class="forgot-password">
            <a href="#" @click.prevent="handleForgotPassword">Forgot Password?</a>
          </div>

          <!-- UPDATED: Button is disabled while loading -->
          <button type="submit" :disabled="loading">
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>

          <div class="company-link">
            <!-- You might want to link this to a signup page -->
            <router-link to="/signup">Don't have an account? Sign Up</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth' // 1. Import your auth store

// 2. Instantiate the store
const authStore = useAuthStore()

// 3. UPDATED: Use 'email' instead of 'username'
const email = ref('')
const password = ref('')
const loading = ref(false)
const loginError = ref(null) // To hold errors from Supabase

// 4. UPDATED: The handleLogin function now uses the store
const handleLogin = async () => {
  // Reset previous errors
  loginError.value = null
  loading.value = true

  try {
    // Call the login action from your Pinia store
    await authStore.login(email.value, password.value)
    
    // The store will handle the redirect on success, so you don't need to do anything here.
    
  } catch (error) {
    // If the store action throws an error, display it
    loginError.value = error.message || "An unexpected error occurred."
    
  } finally {
    // Ensure loading is set to false even if there's an error
    loading.value = false
  }
}

const handleForgotPassword = () => {
  alert('You would implement a password reset flow here, likely using supabase.auth.resetPasswordForEmail()')
}
</script>

<style scoped>
/* Your existing styles are great and don't need to change */
/* I've added one small style for the general error message */
.general-error {
  background-color: #f8d7da;
  color: #721c24;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  text-align: center;
}

/* --- Main Layout Styles --- */
.login-page-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

.image-side {
  width: 60%;
}

.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.form-side {
  width: 40%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  padding: 1rem; 
  box-sizing: border-box;
}

/* --- Login Form Specific Styles --- */
.login-container {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 350px;
}

h2 {
    text-align: center;
    color: #333;
    margin-bottom: 1.5rem;
}

.form-group {
    margin-bottom: 1rem;
}
label {
    display: block;
    margin-bottom: 0.5rem;
    color: #555;
}
input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}
button {
    width: 100%;
    padding: 0.75rem;
    background-color: #4285f4;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    margin-top: 1rem;
    transition: background-color 0.2s;
}
button:hover:not(:disabled) {
    background-color: #3367d6;
}
button:disabled {
    background-color: #9ec2f8;
    cursor: not-allowed;
}
.forgot-password {
    text-align: right;
    margin-top: 0.5rem;
}
.forgot-password a {
    color: #4285f4;
    text-decoration: none;
    font-size: 0.9rem;
}
.company-link {
    text-align: center;
    margin-top: 1rem;
    font-size: 0.9rem;
}
.company-link a {
    color: #4285f4;
    text-decoration: none;
}
.error-message {
    color: #d32f2f;
    font-size: 0.9rem;
    margin-top: 0.25rem;
}
</style>