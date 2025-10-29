'use client'

import { useEffect, useState } from 'react'
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  flexRender,
  ColumnDef,
} from '@tanstack/react-table'
import { Sparkles, Loader2, RefreshCw, Trash2 } from 'lucide-react'
import { fetchLeads, enrichLeads, deleteLead } from '@/lib/api'

interface Lead {
  id: number
  first_name: string | null
  last_name: string | null
  company: string | null
  title: string | null
  website: string | null
  linkedin_url: string | null
  email: string | null
  phone: string | null
  enrichment_status: string
  enriched_data: any
  created_at: string
  updated_at: string
}

interface LeadsTableProps {
  refreshTrigger: number
}

export default function LeadsTable({ refreshTrigger }: LeadsTableProps) {
  const [leads, setLeads] = useState<Lead[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedRows, setSelectedRows] = useState<Record<string, boolean>>({})
  const [enriching, setEnriching] = useState(false)

  const loadLeads = async () => {
    try {
      setLoading(true)
      const data = await fetchLeads()
      setLeads(data)
    } catch (error) {
      console.error('Failed to load leads:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadLeads()
  }, [refreshTrigger])

  const handleEnrichSelected = async () => {
    const selectedIds = Object.keys(selectedRows)
      .filter(id => selectedRows[id])
      .map(id => parseInt(id))

    if (selectedIds.length === 0) {
      alert('Please select leads to enrich')
      return
    }

    setEnriching(true)
    try {
      await enrichLeads(selectedIds, ['apollo', 'email', 'ai'])
      alert('Enrichment started! This may take a few minutes.')
      setSelectedRows({})
      loadLeads()
    } catch (error) {
      console.error('Enrichment failed:', error)
      alert('Failed to start enrichment')
    } finally {
      setEnriching(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this lead?')) {
      try {
        await deleteLead(id)
        loadLeads()
      } catch (error) {
        console.error('Delete failed:', error)
        alert('Failed to delete lead')
      }
    }
  }

  const columns: ColumnDef<Lead>[] = [
    {
      id: 'select',
      header: ({ table }) => (
        <input
          type="checkbox"
          checked={table.getIsAllRowsSelected()}
          onChange={table.getToggleAllRowsSelectedHandler()}
          className="w-4 h-4 text-primary-600 rounded"
        />
      ),
      cell: ({ row }) => (
        <input
          type="checkbox"
          checked={selectedRows[row.original.id]}
          onChange={(e) => {
            setSelectedRows(prev => ({
              ...prev,
              [row.original.id]: e.target.checked
            }))
          }}
          className="w-4 h-4 text-primary-600 rounded"
        />
      ),
    },
    {
      accessorKey: 'first_name',
      header: 'First Name',
      cell: ({ row }) => (
        <div className="font-medium text-gray-900">
          {row.original.first_name || '-'}
        </div>
      ),
    },
    {
      accessorKey: 'last_name',
      header: 'Last Name',
      cell: ({ row }) => (
        <div className="font-medium text-gray-900">
          {row.original.last_name || '-'}
        </div>
      ),
    },
    {
      accessorKey: 'email',
      header: 'Email',
      cell: ({ row }) => (
        <div className="text-gray-600">
          {row.original.email || '-'}
        </div>
      ),
    },
    {
      accessorKey: 'title',
      header: 'Title',
      cell: ({ row }) => (
        <div className="text-gray-600">
          {row.original.title || '-'}
        </div>
      ),
    },
    {
      accessorKey: 'company',
      header: 'Company',
      cell: ({ row }) => (
        <div className="font-medium text-gray-900">
          {row.original.company || '-'}
        </div>
      ),
    },
    {
      accessorKey: 'enrichment_status',
      header: 'Status',
      cell: ({ row }) => {
        const status = row.original.enrichment_status
        const colors = {
          pending: 'bg-gray-100 text-gray-700',
          processing: 'bg-blue-100 text-blue-700',
          completed: 'bg-green-100 text-green-700',
          failed: 'bg-red-100 text-red-700',
        }
        return (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status as keyof typeof colors] || colors.pending}`}>
            {status}
          </span>
        )
      },
    },
    {
      id: 'actions',
      header: 'Actions',
      cell: ({ row }) => (
        <div className="flex space-x-2">
          <button
            onClick={() => handleDelete(row.original.id)}
            className="text-red-600 hover:text-red-800"
            title="Delete"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      ),
    },
  ]

  const table = useReactTable({
    data: leads,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  })

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-4 border-b border-gray-200 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h2 className="text-lg font-semibold text-gray-900">
            Leads ({leads.length})
          </h2>
          <button
            onClick={loadLeads}
            className="text-gray-600 hover:text-gray-900"
            title="Refresh"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
        
        <button
          onClick={handleEnrichSelected}
          disabled={enriching || Object.values(selectedRows).filter(Boolean).length === 0}
          className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {enriching ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Sparkles className="w-4 h-4" />
          )}
          <span>Enrich Selected</span>
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            {table.getHeaderGroups().map(headerGroup => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map(header => (
                  <th
                    key={header.id}
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {table.getRowModel().rows.map(row => (
              <tr key={row.id} className="hover:bg-gray-50">
                {row.getVisibleCells().map(cell => (
                  <td key={cell.id} className="px-6 py-4 whitespace-nowrap text-sm">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {leads.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No leads yet. Upload a CSV to get started!</p>
        </div>
      )}

      <div className="p-4 border-t border-gray-200 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <button
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
            className="px-3 py-1 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <button
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
            className="px-3 py-1 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
        <span className="text-sm text-gray-700">
          Page {table.getState().pagination.pageIndex + 1} of{' '}
          {table.getPageCount()}
        </span>
      </div>
    </div>
  )
}

