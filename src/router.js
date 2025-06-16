import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import AttendanceDashboard from './views/AttendanceDashboard.vue'
import SignUp from './views/Signup.vue'
import CheckIn from './views/CheckIn.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/dashboard', component: AttendanceDashboard },
  { path: '/signup', component: SignUp},
  { path: '/checkin', component: CheckIn}
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})