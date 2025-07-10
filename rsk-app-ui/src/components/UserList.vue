<template>
  <div class="user-list">
    <h1>User List</h1>
    <ul v-if="users.length > 0">
      <li v-for="user in users" :key="user.id">
        <strong>{{ user.name }}</strong> — {{ user.email }}
      </li>
    </ul>
    <p v-else>No users found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const users = ref([])

onMounted(() => {
  // Mock data — replace with API call later
  users.value = [
    { id: 1, name: 'John Doe', email: 'john@example.com' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
    { id: 3, name: 'Alice Johnson', email: 'alice@example.com' }
  ]
})
</script>

<style scoped>
.user-list {
  max-width: 600px;
  margin: 2rem auto;
  font-family: Arial, sans-serif;
}
.user-list h1 {
  text-align: center;
  margin-bottom: 1rem;
}
.user-list ul {
  list-style: none;
  padding: 0;
}
.user-list li {
  background: #f4f4f4;
  margin-bottom: 0.5rem;
  padding: 0.75rem;
  border-radius: 5px;
}
</style>