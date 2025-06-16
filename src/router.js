import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import AttendanceDashboard from './views/AttendanceDashboard.vue'
import SignUp from './views/Signup.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/dashboard', component: AttendanceDashboard },
  { path: '/signup', component: SignUp}
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})