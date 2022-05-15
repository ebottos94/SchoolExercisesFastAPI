import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import { createApp} from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';

createApp(App).use(router).mount('#app')

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000/';  // the FastAPI backend

//Vue.config.productionTip = false;