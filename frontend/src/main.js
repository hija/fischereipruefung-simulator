import { createApp } from 'vue'
import axios from 'axios'
import App from './App.vue'


import 'bootstrap/dist/css/bootstrap.css'

const app = createApp(App).mount('#app')
app.config.globalProperties.axios=axios