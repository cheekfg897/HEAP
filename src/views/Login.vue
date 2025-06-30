<template>
  <!-- Main container for the page -->
  <div class="login-page-container">

    <!-- Left side - Image (now takes up 3/4 of the width) -->
    <div class="image-side">
      <img
        src="../assets/Events.svg"
        alt="University Campus"
        class="background-image"
      />
      <!-- The gradient overlay has been removed -->
    </div>

    <!-- Right side - Login Form (now takes up 1/4 of the width) -->
    <div class="form-side">
      <div class="login-container">
        <h2>Login</h2>
        
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="username">Username</label>
            <input
              id="username"
              v-model="username"
              @input="clearError('username')"
              type="text"
              placeholder="Enter your username"
            />
            <div class="error-message" v-if="errors.username">{{ errors.username }}</div>
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              v-model="password"
              @input="clearError('password')"
              type="password"
              placeholder="Enter your password"
            />
            <div class="error-message" v-if="errors.password">{{ errors.password }}</div>
          </div>

          <div class="forgot-password">
            <a href="#" @click.prevent="handleForgotPassword">Forgot Password?</a>
          </div>

          <button type="submit">Login</button>

          <div class="company-link">
            <a href="#" @click.prevent="handleCompanyLogin">For a company? [CCA]?</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
// The script logic remains unchanged
import { ref } from 'vue'

const username = ref('')
const password = ref('')
const errors = ref({ username: '', password: '' })

const handleLogin = () => {
  errors.value = { username: '', password: '' }
  if (!username.value) {
    errors.value.username = 'Username is required'
  }
  if (!password.value) {
    errors.value.password = 'Password must be required'
  } else if (password.value.length < 6) {
    errors.value.password = 'Password must be at least 6 characters'
  }
  if (!errors.value.username && !errors.value.password) {
    alert('Login successful!')
  }
}

const clearError = (field) => {
  errors.value[field] = ''
}

const handleForgotPassword = () => {
  alert('Forgot password functionality')
}

const handleCompanyLogin = () => {
  const method = prompt('Auth method?')
  if (method) {
    alert(`Using ${method}`)
  }
}
</script>

<style scoped>
/* --- Main Layout Styles --- */
.login-page-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

.image-side {
  /* CHANGED: Set width to 3/4 (75%) of the container */
  width: 60%;
}

.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* REMOVED: The .image-overlay style block is gone */

.form-side {
  /* CHANGED: Set width to 1/4 (25%) of the container */
  width: 40%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  /* Add some padding for better spacing on smaller screens */
  padding: 1rem; 
  box-sizing: border-box;
}


/* --- Login Form Specific Styles (Unchanged) --- */
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

/* ... all other form styles remain the same ... */

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
}
button:hover {
    background-color: #3367d6;
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