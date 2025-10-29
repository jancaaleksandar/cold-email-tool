'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { X, Upload, FileText, Loader2 } from 'lucide-react'
import { uploadCSV } from '@/lib/api'

interface UploadModalProps {
  onClose: () => void
  onSuccess: () => void
}

export default function UploadModal({ onClose, onSuccess }: UploadModalProps) {
  const [uploading, setUploading] = useState(false)
  const [file, setFile] = useState<File | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0])
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
    },
    maxFiles: 1,
  })

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    try {
      await uploadCSV(file)
      onSuccess()
    } catch (error) {
      console.error('Upload failed:', error)
      alert('Failed to upload CSV')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Upload Leads</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6">
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragActive
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <input {...getInputProps()} />
            <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
            {file ? (
              <div className="flex items-center justify-center space-x-2">
                <FileText className="w-5 h-5 text-primary-600" />
                <span className="font-medium text-gray-900">{file.name}</span>
              </div>
            ) : (
              <>
                <p className="text-gray-700 font-medium mb-1">
                  Drop your CSV file here, or click to browse
                </p>
                <p className="text-sm text-gray-500">
                  CSV files only
                </p>
              </>
            )}
          </div>

          <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800 font-medium mb-2">
              CSV Format Requirements:
            </p>
            <ul className="text-xs text-blue-700 space-y-1">
              <li>• first_name, last_name, company, title</li>
              <li>• website, linkedin_url, email, phone</li>
              <li>• At least one column required</li>
            </ul>
          </div>
        </div>

        <div className="flex items-center justify-end space-x-3 p-6 border-t border-gray-200">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-700 hover:text-gray-900 font-medium"
            disabled={uploading}
          >
            Cancel
          </button>
          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {uploading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Uploading...</span>
              </>
            ) : (
              <>
                <Upload className="w-4 h-4" />
                <span>Upload</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  )
}

