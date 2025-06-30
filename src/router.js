import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './stores/auth'
import Login from './views/Login.vue'
import AttendanceDashboard from './views/AttendanceDashboard.vue'
import SignUp from './views/Signup.vue'
import CheckIn from './views/CheckIn.vue'
import UpcomingEvents from './views/UpcomingEvents.vue'
import PostEventAnalytics1 from './views/PostEventAnalytics1.vue'

const routes = [
  // --- Public Routes ---
  {
    path: '/',
    name: 'login', // It's best practice to name your routes
    component: Login
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUp
  },

  // --- Protected Routes ---
  {
    path: '/dashboard',
    name: 'dashboard',
    component: AttendanceDashboard,
    meta: {
      requiresAuth: true // Mark this route as requiring authentication
    }
  },
  {
    path: '/checkin',
    name: 'checkin',
    component: CheckIn,
    meta: {
      requiresAuth: true // Mark this route as requiring authentication
    }
  },
  {
    path: '/upcomingevents',
    name: 'upcomingevents',
    component: UpcomingEvents,
    meta: {
      requiresAuth: true // Mark this route as requiring authentication
    }
  },
  {
    path: '/posteventanalytics',
    name: 'posteventanalytics',
    component: PostEventAnalytics1,
    meta: {
      requiresAuth: true // Mark this route as requiring authentication
    }
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})


// --- Navigation Guard ---
// This runs before each navigation.
router.beforeEach(async (to, from, next) => {
  // Get the auth store
  const authStore = useAuthStore()

  // This is the key part for persistence:
  // We check if the user's state is loaded. If not, we try to fetch it.
  // This handles the case where a user is already logged in and refreshes the page.
  if (!authStore.isLoggedIn) {
    // Await the checkUser function from your Pinia store
    await authStore.checkUser()
  }

  // Check if the route requires authentication
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  // If the route requires auth and the user is not logged in, redirect to the login page.
  if (requiresAuth && !authStore.isLoggedIn) {
    next({ name: 'login' }); // Redirect to the login page
  } else {
    // Otherwise, allow the navigation to proceed.
    next();
  }
});

// IMPORTANT: Vue Router v4 exports the instance, not the constructor.
// Your original code `export const router = ...` is correct for v4.
// If you are using Vue 2 / Router v3, you would export a new instance.
export default router;