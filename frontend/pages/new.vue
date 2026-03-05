<script setup lang="ts">
import type { Generation } from "~/lib/api"
import { useApi } from "~/lib/api"

const { apiPost } = useApi()
const title = ref("Test")
const lang = ref<"ru" | "en">("ru")
const slidesCount = ref(8)
const text = ref(
  "Напиши пост про пользу планирования и дисциплины."
)
const styleHint = ref("Короткие фразы, деловой стиль.")

const creating = ref(false)
const error = ref<string | null>(null)

async function createAndGenerate() {
  creating.value = true
  error.value = null
  try {
    const carousel = await apiPost<{ id: string }>("/carousels", {
      title: title.value,
      source_type: "text",
      source_payload: { text: text.value },
      lang: lang.value,
      slides_count: slidesCount.value,
      style_hint: styleHint.value,
    })

    const gen = await apiPost<Generation>("/generations", {
      carousel_id: carousel.id,
    })
    await navigateTo(`/editor/${carousel.id}?gen=${gen.id}`)
  } catch (e: unknown) {
    const err = e as { data?: { detail?: string }; message?: string }
    error.value =
      err?.data?.detail || err?.message || "Failed"
  } finally {
    creating.value = false
  }
}
</script>

<template>
  <div style="max-width: 720px; margin: 0 auto; padding: 16px">
    <h1>Create carousel</h1>

    <div style="display: grid; gap: 10px">
      <label>Title <input v-model="title" style="width: 100%" /></label>

      <label>
        Language
        <select v-model="lang">
          <option value="ru">RU</option>
          <option value="en">EN</option>
        </select>
      </label>

      <label>
        Slides count
        <input v-model.number="slidesCount" type="number" min="6" max="10" />
      </label>

      <label>
        Style hint
        <textarea v-model="styleHint" rows="3" style="width: 100%"></textarea>
      </label>

      <label>
        Source text
        <textarea v-model="text" rows="8" style="width: 100%"></textarea>
      </label>

      <button type="button" :disabled="creating" @click="createAndGenerate">
        {{ creating ? "Working..." : "Create & Generate" }}
      </button>

      <div v-if="error" style="color: #b91c1c">{{ error }}</div>
    </div>
  </div>
</template>
