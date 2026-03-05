<script setup lang="ts">
import type {
  Carousel,
  Slide,
  Generation,
  ExportJob,
} from "~/lib/api"
import { useApi } from "~/lib/api"

const route = useRoute()
const id = route.params.id as string
const genId = route.query.gen as string | undefined

const { apiGet, apiPatch, apiPost } = useApi()

const carousel = ref<Carousel | null>(null)
const slides = ref<Slide[]>([])
const active = ref(0)

const gen = ref<Generation | null>(null)
const exp = ref<ExportJob | null>(null)

const loading = ref(false)
const saving = ref(false)

async function loadAll() {
  loading.value = true
  try {
    carousel.value = await apiGet<Carousel>(`/carousels/${id}`)
    slides.value = await apiGet<Slide[]>(`/carousels/${id}/slides`)
  } finally {
    loading.value = false
  }
}

async function pollGeneration(gid: string) {
  for (let i = 0; i < 60; i++) {
    const g = await apiGet<Generation>(`/generations/${gid}`)
    gen.value = g
    if (g.status === "done" || g.status === "failed") break
    await new Promise((r) => setTimeout(r, 1000))
  }
  await loadAll()
}

async function saveSlide() {
  const s = slides.value[active.value]
  if (!s) return
  saving.value = true
  try {
    const updated = await apiPatch<Slide>(
      `/carousels/${id}/slides/${s.id}`,
      {
        title: s.title,
        body: s.body,
        footer: s.footer,
      }
    )
    slides.value[active.value] = updated
  } finally {
    saving.value = false
  }
}

async function startExport() {
  const result = await apiPost<ExportJob>("/exports", { carousel_id: id })
  exp.value = result
  const eid = result.id
  for (let i = 0; i < 90; i++) {
    const e = await apiGet<ExportJob>(`/exports/${eid}`)
    exp.value = e
    if (e.status === "done" || e.status === "failed") break
    await new Promise((r) => setTimeout(r, 1000))
  }
}

onMounted(async () => {
  await loadAll()
  if (genId) await pollGeneration(genId)
})
</script>

<template>
  <div style="max-width: 1100px; margin: 0 auto; padding: 16px">
    <div
      style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
      "
    >
      <div>
        <h1 style="margin: 0">Editor</h1>
        <div style="font-size: 12px; opacity: 0.7">
          {{ carousel?.title }} · status: {{ carousel?.status }}
        </div>
      </div>

      <div style="display: flex; gap: 10px; align-items: center">
        <button
          type="button"
          :disabled="!slides.length"
          @click="startExport"
        >
          Export
        </button>
        <NuxtLink to="/">Back</NuxtLink>
      </div>
    </div>

    <div
      v-if="gen && gen.status !== 'done'"
      style="margin-top: 10px"
    >
      Generation: {{ gen.status }}
      <span v-if="gen.error" style="color: #b91c1c">{{ gen.error }}</span>
    </div>

    <div v-if="exp" style="margin-top: 10px">
      Export: {{ exp.status }}
      <span v-if="exp.error" style="color: #b91c1c">{{ exp.error }}</span>
      <a
        v-if="exp.status === 'done' && exp.download_url"
        :href="exp.download_url"
        target="_blank"
        rel="noopener noreferrer"
        style="margin-left: 10px"
      >
        Download ZIP
      </a>
    </div>

    <div
      style="
        display: grid;
        grid-template-columns: 260px 1fr;
        gap: 16px;
        margin-top: 16px;
      "
    >
      <div
        style="
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          padding: 12px;
        "
      >
        <div style="font-weight: 700; margin-bottom: 10px">Slides</div>
        <div v-if="loading">Loading...</div>
        <div
          v-else
          style="display: flex; flex-direction: column; gap: 8px"
        >
          <button
            v-for="(s, idx) in slides"
            :key="s.id"
            type="button"
            :style="{
              textAlign: 'left',
              padding: '10px',
              borderRadius: '10px',
              border: '1px solid #e5e7eb',
              background: idx === active ? '#eef2ff' : 'white',
            }"
            @click="active = idx"
          >
            {{ s.order }}. {{ s.title || "(no title)" }}
          </button>
        </div>
      </div>

      <div
        style="
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          padding: 12px;
        "
      >
        <div v-if="!slides.length">No slides yet.</div>

        <div v-else style="display: grid; gap: 10px">
          <div style="font-size: 12px; opacity: 0.7">
            Editing slide {{ slides[active].order }}
          </div>

          <label>
            Title
            <input v-model="slides[active].title" style="width: 100%" />
          </label>

          <label>
            Body
            <textarea
              v-model="slides[active].body"
              rows="10"
              style="width: 100%"
            />
          </label>

          <label>
            Footer
            <input v-model="slides[active].footer" style="width: 100%" />
          </label>

          <button
            type="button"
            :disabled="saving"
            @click="saveSlide"
          >
            {{ saving ? "Saving..." : "Save" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
