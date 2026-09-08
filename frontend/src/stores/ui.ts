import { create } from 'zustand'
import { UUID } from '../types'

export interface UiStore {
  sidebarOpen: boolean
  currentPage: string
  selectedSeeds: UUID[]
  selectedRules: UUID[]
  toggleSidebar: () => void
  setCurrentPage: (page: string) => void
  setSelectedSeeds: (seeds: UUID[]) => void
  setSelectedRules: (rules: UUID[]) => void
}

export const useUiStore = create<UiStore>((set) => ({
  sidebarOpen: true,
  currentPage: 'dashboard',
  selectedSeeds: [],
  selectedRules: [],
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setCurrentPage: (page: string) => set({ currentPage: page }),
  setSelectedSeeds: (seeds: UUID[]) => set({ selectedSeeds: seeds }),
  setSelectedRules: (rules: UUID[]) => set({ selectedRules: rules }),
}))
