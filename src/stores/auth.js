import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { supabase } from '../supabase'
import { router } from '../router'     // Your Vue router instance

// The first argument to defineStore is a unique ID for the store
export const useAuthStore = defineStore('auth', () => {

    // --- STATE ---
    // The user object from Supabase. null if not logged in.
    const user = ref(null)

    // --- GETTERS ---
    // A computed property to easily check if the user is logged in.
    // The `!!` converts a value (object or null) to a boolean (true or false).
    const isLoggedIn = computed(() => !!user.value)

    // --- ACTIONS ---

    /**
     * Handles the user login process.
     * @param {string} email - The user's email.
     * @param {string} password - The user's password.
     */
    async function login(email, password) {
        const { data, error } = await supabase.auth.signInWithPassword({
            email: email,
            password: password,
        })

        if (error) {
            // If Supabase returns an error, throw it to be caught by the component
            throw error
        }

        // If login is successful, update the user state
        user.value = data.user
        
        // Redirect the user to the dashboard after successful login
        router.push({ name: 'dashboard' })
    }

    /**
     * Handles the user registration process.
     * @param {string} email - The new user's email.
     * @param {string} password - The new user's password.
     */
    async function signUp(email, password) {
        const { data, error } = await supabase.auth.signUp({
            email: email,
            password: password,
        })
        
        if (error) {
            throw error
        }
        
        // Optionally, you can return the user data or handle it as needed
        return data.user
    }

    /**
     * Handles the user logout process.
     */
    async function logout() {
        const { error } = await supabase.auth.signOut()

        if (error) {
            throw error
        }

        // Reset the user state to null
        user.value = null
        
        // Redirect the user to the login page after logout
        router.push({ name: 'login' })
    }

    /**
     * Checks for an active session with Supabase on app startup.
     * This is crucial for session persistence.
     */
    async function checkUser() {
        const { data } = await supabase.auth.getUser()
        user.value = data.user
    }

    // --- RETURN ---
    // Expose the state, getters, and actions to be used in components and the router.
    return {
        user,
        isLoggedIn,
        login,
        signUp,
        logout,
        checkUser,
    }
})