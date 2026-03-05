<script setup lang="ts">
import type { Carousel } from "~/lib/api"
import { useApi } from "~/lib/api"

const { apiGet } = useApi()
const carousels = ref<Carousel[]>([])
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    carousels.value = await apiGet<Carousel[]>("/carousels")
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div style="max-width: 960px; margin: 0 auto; padding: 16px">
    <div
      style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
      "
    >
      <h1>My carousels</h1>
      <NuxtLink to="/new">Create</NuxtLink>
    </div>

    <div v-if="loading">Loading...</div>

    <div
      v-else
      style="
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 12px;
      "
    >
      <div
        v-for="c in carousels"
        :key="c.id"
        style="
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          padding: 12px;
        "
      >
        <div style="font-weight: 700">{{ c.title }}</div>
        <div style="font-size: 12px; opacity: 0.7; margin-top: 6px">
          status: {{ c.status }} · {{ c.lang }} · slides: {{ c.slides_count }}
        </div>
        <div style="margin-top: 10px; display: flex; gap: 10px">
          <NuxtLink :to="`/editor/${c.id}`">Open</NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>
