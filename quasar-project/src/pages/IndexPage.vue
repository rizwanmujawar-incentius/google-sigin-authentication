<template>
  <q-page class="flex flex-center column">
    <div v-if="Object.keys(user_details).length != 0">
      <div class="q-pa-md q-gutter-sm">
        <q-banner rounded class="bg-purple-8 text-white">

          The names is : {{ user_details.name }}
          <br>
          The email is : {{ user_details.email }}

          <template v-slot:action>
            <q-btn flat color="white" @click="logout" label="logout" />
          </template>
        </q-banner>
      </div>
    </div>
    <div v-else>
      <q-card class="my-card">
        <q-card-section>
          <div class="text-h6">Login</div>
        </q-card-section>
        <q-separator />
        <q-card-actions vertical>
          <GoogleLogin :callback="callback" />
        </q-card-actions>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue';
import { decodeCredential, googleLogout } from 'vue3-google-login'


export default defineComponent({
  name: 'IndexPage',
  data() {
    return {
      user: null,
      user_details: {},
      callback: async (response, user) => {
        var obj = {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json; charset=UTF-8',
          },
        };
        console.log(response)
        this.user = await response
        this.user_details = await this.$axios.post('/api/userdetails', this.user, obj).then(function (response) {
          return response.data
        })
          .catch(function (response) {
            console.log("error")
          })
      }
    }
  },
  async created() {
    let url = await this.$axios.get('/api/check-user').then(function (response) {
      console.log("heyy")
      console.log(response.data)
      console.log("heyy2")
      return response
    })
      .catch(function (response) {
        console.log("error")
      })
  },
  methods: {
    async logout() {
      this.user_details = {}
      let logout_user = await this.$axios.get('/api/logout').then(function (response) {
        return response
      })
        .catch(function (response) {
          console.log("error")
        })
    },
    async login() {
      var obj = {
        method: ' GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
        },
      };
      let url = await this.$axios.get('/api/google-login').then(function (response) {
        console.log(response.data)
        window.location.assign(response.data)
        return response
      })
        .catch(function (response) {
          console.log("error")
        })
      console.log("url")
      console.log(url)
    }
  }
});
</script>
