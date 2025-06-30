import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'
import { createPinia } from 'pinia'

const app = createApp(App)

app.use(router) // <-- Problem: Router is used here
app.use(createPinia()) // <-- Pinia is used too late

app.mount('#app')
