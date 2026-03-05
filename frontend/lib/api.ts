export type Carousel = {
  id: string
  title: string
  status: string
  lang?: string
  slides_count?: number
}

export type Slide = {
  id: string
  order: number
  title?: string
  body?: string
  footer?: string
}

export type Generation = {
  id: string
  carousel_id: string
  status: string
  error?: string | null
}

export type ExportJob = {
  id: string
  carousel_id: string
  status: string
  zip_asset_key?: string | null
  download_url?: string | null
  error?: string | null
}

export function useApi() {
  const config = useRuntimeConfig()
  const base = (config.public.apiBase as string) || "http://localhost:8000"

  async function apiGet<T>(path: string): Promise<T> {
    return await $fetch<T>(`${base}${path}`)
  }

  async function apiPost<T>(path: string, body: unknown): Promise<T> {
    return await $fetch<T>(`${base}${path}`, { method: "POST", body })
  }

  async function apiPatch<T>(path: string, body: unknown): Promise<T> {
    return await $fetch<T>(`${base}${path}`, { method: "PATCH", body })
  }

  return { apiGet, apiPost, apiPatch }
}
