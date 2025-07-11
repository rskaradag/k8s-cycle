<template>
  <div class="user-list">
    <h1>User List</h1>
    <ul v-if="users.length > 0">
      <li v-for="user in users" :key="user.id">
        <strong>{{ user.username }}</strong> — {{ user.email }}
      </li>
    </ul>
    <p v-else>Loading or no users found...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const users = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/users')
    users.value = response.data
  } catch (error) {
    console.error('Error fetching users:', error)
  }
})
</script>