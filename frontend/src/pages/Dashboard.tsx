import React from 'react'
import { FiTrendingUp, FiDatabase, FiClock, FiCheckCircle } from 'react-icons/fi'
import { useSeedStatistics, useTaskList } from '../hooks/useQueries'

const Dashboard: React.FC = () => {
  const { data: stats } = useSeedStatistics()
  const { data: tasks } = useTaskList()

  const StatCard: React.FC<{ icon: React.ReactNode; label: string; value: string | number }> = ({
    icon,
    label,
    value,
  }) => (
    <div className="card p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-sm">{label}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
        </div>
        <div className="text-4xl text-blue-600 opacity-20">{icon}</div>
      </div>
    </div>
  )

  return (
    <div className="space-y-8">
      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={<FiDatabase />}
          label="Total Seeds"
          value={stats?.total || 0}
        />
        <StatCard
          icon={<FiTrendingUp />}
          label="Recent Tasks"
          value={tasks?.length || 0}
        />
        <StatCard
          icon={<FiCheckCircle />}
          label="Completed"
          value={tasks?.filter((t: any) => t.status === 'completed').length || 0}
        />
        <StatCard
          icon={<FiClock />}
          label="In Progress"
          value={tasks?.filter((t: any) => t.status === 'running').length || 0}
        />
      </div>

      {/* Recent Tasks */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Tasks</h3>
        {tasks && tasks.length > 0 ? (
          <div className="space-y-3">
            {tasks.slice(0, 5).map((task: any) => (
              <div key={task.id} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <div>
                  <p className="font-medium">{task.name}</p>
                  <p className="text-sm text-gray-600">{task.status}</p>
                </div>
                <div className="text-right">
                  <p className="font-medium">{task.results.generated}</p>
                  <p className="text-sm text-gray-600">passwords</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-600">No tasks yet</p>
        )}
      </div>
    </div>
  )
}

export default Dashboard
