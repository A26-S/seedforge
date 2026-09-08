import axios from 'axios'
import { Seed, Rule, Task } from '../types'

const API_BASE = '/api'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
})

// Seed API
export const seedApi = {
  listCategories: () => api.get('/seeds/categories'),
  listSeeds: (category: string) => api.get(`/seeds/list/${category}`),
  searchSeeds: (q: string, category?: string) =>
    api.get('/seeds/search', { params: { q, category } }),
  addSeed: (value: string, category: string, tags?: string[]) =>
    api.post('/seeds/add', { value, category, tags }),
  importSeeds: (category: string, file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/seeds/import?category=${category}`, formData)
  },
  getStatistics: () => api.get('/seeds/statistics'),
}

// Rules API
export const rulesApi = {
  listPresets: () => api.get('/rules/presets'),
  getPreset: (name: string) => api.get(`/rules/presets/${name}`),
  preview: (seeds: string[], rules: any) => api.post('/rules/preview', { seeds, rules }),
  validate: (rule: any) => api.post('/rules/validate', rule),
}

// Tasks API
export const tasksApi = {
  createTask: (name: string, seedIds: string[], ruleIds: string[], config: any) =>
    api.post('/tasks/create', { name, seed_ids: seedIds, rule_ids: ruleIds, config }),
  getTask: (taskId: string) => api.get(`/tasks/${taskId}`),
  startTask: (taskId: string) => api.post(`/tasks/${taskId}/start`),
  pauseTask: (taskId: string) => api.post(`/tasks/${taskId}/pause`),
  resumeTask: (taskId: string) => api.post(`/tasks/${taskId}/resume`),
  cancelTask: (taskId: string) => api.post(`/tasks/${taskId}/cancel`),
  listTasks: () => api.get('/tasks/history'),
  compareTasks: (taskId1: string, taskId2: string) =>
    api.post('/tasks/compare', { task_id1: taskId1, task_id2: taskId2 }),
}

// Export API
export const exportApi = {
  exportTxt: (passwords: string[], filename?: string) =>
    api.post('/export/txt', { passwords, filename }),
  exportCsv: (passwords: string[], filename?: string) =>
    api.post('/export/csv', { passwords, filename }),
  exportJson: (passwords: string[], filename?: string) =>
    api.post('/export/json', { passwords, filename }),
}

// Analysis API
export const analysisApi = {
  analyzeEntropy: (passwords: string[]) =>
    api.post('/analysis/entropy', { passwords }),
  analyzeDistribution: (passwords: string[]) =>
    api.post('/analysis/distribution', { passwords }),
}

export default api
