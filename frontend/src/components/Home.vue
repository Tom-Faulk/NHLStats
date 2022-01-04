// Home.vue

<template>
  <div>
    <p>Home page</p>
    <button @click="callDataFunctions">Re-run 'getDataFromBackend'</button>
    <bootstrap-vue-datatable :playerPosts="playerPosts" :goaliePosts="goaliePosts"></bootstrap-vue-datatable>
    
  </div>
</template>

<script>
import axios from 'axios'
import BootstrapVueDatatable from './BootstrapVueDatatable.vue'
export default {
    components: {
        BootstrapVueDatatable
    },

  data () {
    return {
        playerPosts: [
            {

            }
        ],

        goaliePosts: [
            {

            }
        ]
      
    }
  },
  methods: {
    callDataFunctions () {
        this.getPlayerDataFromBackend()
        this.getGoalieDataFromBackend()
    },
    getPlayerDataFromBackend () {
    const path = `http://localhost:5000/api/playerQuery`
    axios.get(path)
    .then(response => {
      this.playerPosts = response.data
    })
    
    .catch(error => {
      console.log(error)
    })
    },
    getGoalieDataFromBackend () {
    const path = `http://localhost:5000/api/goalieQuery`
    axios.get(path)
    .then(response => {
      this.goaliePosts = response.data
    })
    
    .catch(error => {
      console.log(error)
    })
    }
  },
  created () {
    this.callDataFunctions()
  }
}
</script>