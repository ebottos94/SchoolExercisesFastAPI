<template>
  <div class="home">
    <EserciziClassi />
  </div>
</template>

<script>
// @ is an alias to /src
import EserciziClassi from '@/components/EserciziClassi.vue'

export default {
  name: 'HomeView',
  components: {
    EserciziClassi
  }
}
</script>
