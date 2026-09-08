import { useQuery } from '@tanstack/react-query'
import { seedApi, rulesApi, tasksApi } from './api'

export function useSeedCategories() {
  return useQuery({
    queryKey: ['seedCategories'],
    queryFn: async () => {
      const { data } = await seedApi.listCategories()
      return data.categories
    },
  })
}

export function useListSeeds(category: string | null) {
  return useQuery({
    queryKey: ['seeds', category],
    queryFn: async () => {
      if (!category) return []
      const { data } = await seedApi.listSeeds(category)
      return data.seeds
    },
    enabled: !!category,
  })
}

export function useSeedStatistics() {
  return useQuery({
    queryKey: ['seedStatistics'],
    queryFn: async () => {
      const { data } = await seedApi.getStatistics()
      return data
    },
  })
}

export function useRulePresets() {
  return useQuery({
    queryKey: ['rulePresets'],
    queryFn: async () => {
      const { data } = await rulesApi.listPresets()
      return data.presets
    },
  })
}

export function useTaskList() {
  return useQuery({
    queryKey: ['tasks'],
    queryFn: async () => {
      const { data } = await tasksApi.listTasks()
      return data.tasks
    },
  })
}

export function useTask(taskId: string | null) {
  return useQuery({
    queryKey: ['task', taskId],
    queryFn: async () => {
      if (!taskId) return null
      const { data } = await tasksApi.getTask(taskId)
      return data
    },
    enabled: !!taskId,
  })
}
