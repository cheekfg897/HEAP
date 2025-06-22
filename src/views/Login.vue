<template>
  <div class="page-center">
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Username</label>
        <input v-model="username" @input="clearError('username')" placeholder="Enter your username">
        <div class="error-message" v-if="errors.username">{{ errors.username }}</div>
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" v-model="password" @input="clearError('password')" placeholder="Enter your password">
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
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const errors = ref({ username: '', password: '' })

const handleLogin = () => {
  errors.value = { username: '', password: '' }

  if (!username.value) errors.value.username = 'Username is required'
  if (!password.value) {
    errors.value.password = 'Password is required'
  } else if (password.value.length < 6) {
    errors.value.password = 'Password must be at least 6 characters'
  }

  if (!errors.value.username && !errors.value.password) {
    alert('Login successful!')
    router.push('/dashboard')
  }
}

const clearError = (field) => {
  errors.value[field] = ''
}

const handleForgotPassword = () => alert('Forgot password logic here')

const handleCompanyLogin = () => {
  const method = prompt('Auth method?')
  if (method) alert(`Using ${method}`)
}
</script>

<style scoped>
/* Use the styles from your login.html */
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            width: 300px;
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
        .page-center {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #f5f5f5;
        }

</style>
