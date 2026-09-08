import { create } from 'zustand'
import { Seed, Rule, Task } from '../types'

export interface GeneratorStore {
  seeds: Seed[]
  rules: Rule[]
  currentTask: Task | null
  previewData: string[]
  estimatedCount: number
  setSeed: (seeds: Seed[]) => void
  setRules: (rules: Rule[]) => void
  setCurrentTask: (task: Task | null) => void
  setPreviewData: (data: string[]) => void
  setEstimatedCount: (count: number) => void
}

export const useGeneratorStore = create<GeneratorStore>((set) => ({
  seeds: [],
  rules: [],
  currentTask: null,
  previewData: [],
  estimatedCount: 0,
  setSeed: (seeds: Seed[]) => set({ seeds }),
  setRules: (rules: Rule[]) => set({ rules }),
  setCurrentTask: (task: Task | null) => set({ currentTask: task }),
  setPreviewData: (data: string[]) => set({ previewData: data }),
  setEstimatedCount: (count: number) => set({ estimatedCount: count }),
}))
