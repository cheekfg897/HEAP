<template>
  <div class="page-center">
    <div class="login-container">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" v-model="email" @input="clearError('email')" placeholder="Enter your email" required>
          <div class="error-message" v-if="errors.email">{{ errors.email }}</div>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" v-model="password" @input="clearError('password')" placeholder="Enter your password" required>
          <div class="error-message" v-if="errors.password">{{ errors.password }}</div>
        </div>

        <div class="forgot-password">
          <a href="#" @click.prevent="handleForgotPassword">Forgot Password?</a>
        </div>

        <button type="submit" :disabled="loading">Login</button>
        <div class="error-message" v-if="authError">{{ authError }}</div>
        <div class="success-message" v-if="authSuccess">{{ authSuccess }}</div>


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
import { supabase } from '@/supabase' // Adjust path as needed based on your project structure

const router = useRouter()
const email = ref('') // Changed from 'username' to 'email' for Supabase auth
const password = ref('')
const errors = ref({ email: '', password: '' }) // Changed from 'username' to 'email'
const authError = ref(null) // To display errors from Supabase
const authSuccess = ref(null) // To display success messages
const loading = ref(false) // To disable button during API call

const handleLogin = async () => {
  errors.value = { email: '', password: '' } // Clear form-level validation errors
  authError.value = null // Clear previous Supabase errors
  authSuccess.value = null // Clear previous success messages

  // --- Client-side form validation ---
  if (!email.value) {
    errors.value.email = 'Email is required';
    return; // Stop if email is missing
  }
  if (!password.value) {
    errors.value.password = 'Password is required';
    return; // Stop if password is missing
  }
  if (password.value.length < 6) {
    errors.value.password = 'Password must be at least 6 characters';
    return; // Stop if password is too short
  }

  loading.value = true; // Disable button

  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value,
    });

    if (error) {
      authError.value = error.message;
      console.error('Supabase Login Error:', error);
    } else {
      authSuccess.value = 'Login successful! Redirecting...';
      console.log('User logged in:', data.user);
      // Redirect to dashboard on successful login
      router.push('/dashboard');
    }
  } catch (err) {
    console.error('Unexpected error during login:', err);
    authError.value = 'An unexpected error occurred. Please try again.';
  } finally {
    loading.value = false; // Re-enable button
  }
}

const clearError = (field) => {
  errors.value[field] = ''
  authError.value = null // Clear general auth error when user starts typing again
}

const handleForgotPassword = async () => {
  const emailInput = prompt('Please enter your email address to reset your password:');
  if (emailInput) {
    // Basic email validation
    if (!emailInput.includes('@') || !emailInput.includes('.')) {
      alert('Please enter a valid email address.');
      return;
    }

    try {
      const { error } = await supabase.auth.resetPasswordForEmail(emailInput, {
        redirectTo: `${window.location.origin}/update-password`, // Configure this URL in Supabase Auth settings
      });

      if (error) {
        alert(`Error: ${error.message}`);
        console.error('Password reset error:', error);
      } else {
        alert('Password reset email sent! Please check your inbox.');
      }
    } catch (err) {
      console.error('Unexpected error during password reset:', err);
      alert('An unexpected error occurred during password reset. Please try again.');
    }
  }
}


const handleCompanyLogin = () => {
  // This part remains as it is, as it's not directly related to Supabase email/password auth
  const method = prompt('Auth method?')
  if (method) alert(`Using ${method}`)
}
</script>

<style scoped>
/* Your existing styles */
.page-center {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
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
button:disabled {
    background-color: #a0c3f7; /* Lighter blue when disabled */
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
.success-message {
    color: #4CAF50; /* Green for success */
    font-size: 0.9rem;
    margin-top: 0.25rem;
}
</style>