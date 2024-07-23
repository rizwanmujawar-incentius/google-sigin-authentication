<template>
<h1>hey</h1>
<button @click="userdetails">click me</button>
<p>{{name}}</p>
 <p v-if="user != ''">
    <a href="/api/logout">logout</a>
  </p>
  <p v-else>
    Please Login
  </p>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'MainPage',
  data(){
    return {
      user:{}
    }
  },
   methods:{
  async userdetails(){
    let user_data = this.$axios.post('/api/userdetails').then(function(response){
      return response;
    })
    this.user = await user_data;
   
  }
 }
}
);
</script>