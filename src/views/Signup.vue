<template>
  <div class="page-center">
  <div class="signup-container">
    <h2>Create Free Account</h2>

    <form @submit.prevent="handleSignup">
      <div class="form-group">
        <label for="username">Username</label>
        <input 
          type="text" 
          id="username" 
          v-model="username" 
          @input="clearError('username')"
          placeholder="Choose a username">
        <div class="error-message" v-if="errors.username">
          {{ errors.username }}
        </div>
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input 
          type="email" 
          id="email" 
          v-model="email" 
          @input="clearError('email')"
          placeholder="Your email address">
        <div class="error-message" v-if="errors.email">
          {{ errors.email }}
        </div>
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input 
          type="password" 
          id="password" 
          v-model="password" 
          @input="clearError('password')"
          placeholder="Create a password">
        <div class="error-message" v-if="errors.password">
          {{ errors.password }}
        </div>
      </div>

      <button type="submit">Create Account</button>
    </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const username = ref('')
const email = ref('')
const password = ref('')
const errors = ref({ username: '', email: '', password: '' })

const validEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)

const clearError = (field) => {
  errors.value[field] = ''
}

const handleSignup = () => {
  errors.value = { username: '', email: '', password: '' }
  let isValid = true

  if (!username.value) {
    errors.value.username = 'Username is required'
    isValid = false
  } else if (username.value.length < 4) {
    errors.value.username = 'Username must be at least 4 characters'
    isValid = false
  }

  if (!email.value) {
    errors.value.email = 'Email is required'
    isValid = false
  } else if (!validEmail(email.value)) {
    errors.value.email = 'Please enter a valid email'
    isValid = false
  }

  if (!password.value) {
    errors.value.password = 'Password is required'
    isValid = false
  } else if (password.value.length < 8) {
    errors.value.password = 'Password must be at least 8 characters'
    isValid = false
  }

  if (isValid) {
    console.log('Signing up:', {
      username: username.value,
      email: email.value,
      password: password.value
    })
    setTimeout(() => {
      alert('Account created successfully! (This is a demo)')
    }, 500)
  }
}
</script>

<style scoped>
body {
  font-family: 'Arial', sans-serif;
  background-color: #f8f9fa;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}
.signup-container {
  background-color: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 350px;
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
    height: 100vh;
    background-color: #f5f5f5;
}

</style>
