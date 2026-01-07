/**
 * File upload component with drag-and-drop support
 */
import { useState, useRef, ChangeEvent, DragEvent } from 'react';
import api from '../services/api';

interface FileUploadProps {
  onUpload: (sessionId: string, metadata: any) => void;
  onError?: (error: string) => void;
}

const FileUpload = ({ onUpload, onError }: FileUploadProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): boolean => {
    const validTypes = [
      'text/csv',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ];
    const validExtensions = ['.csv', '.xlsx', '.xls'];

    const hasValidType = validTypes.includes(file.type);
    const hasValidExtension = validExtensions.some((ext) => file.name.toLowerCase().endsWith(ext));

    return hasValidType || hasValidExtension;
  };

  const handleUpload = async (file: File) => {
    if (!validateFile(file)) {
      const errorMsg = 'Invalid file type. Please upload a CSV or Excel file.';
      setError(errorMsg);
      onError?.(errorMsg);
      return;
    }

    setError(null);
    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post('/api/v1/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const { session_id, metadata } = response.data;
      onUpload(session_id, metadata);
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Upload failed. Please try again.';
      setError(errorMsg);
      onError?.(errorMsg);
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleUpload(file);
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      handleUpload(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="file-upload-container">
      <div
        className={`upload-zone ${isDragging ? 'dragging' : ''} ${isUploading ? 'uploading' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
        role="button"
        tabIndex={0}
        aria-label="Upload file"
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={handleFileChange}
          style={{ display: 'none' }}
          aria-label="Upload file input"
        />

        {isUploading ? (
          <div className="upload-status">
            <p>Uploading...</p>
          </div>
        ) : (
          <div className="upload-prompt">
            <p>Drag & drop your CSV or Excel file here</p>
            <p className="or-text">or</p>
            <button type="button" className="browse-button">
              Browse Files
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="error-message" role="alert">
          {error}
        </div>
      )}

      <style>{`
        .file-upload-container {
          width: 100%;
          max-width: 600px;
          margin: 2rem auto;
        }

        .upload-zone {
          border: 2px dashed #cbd5e0;
          border-radius: 8px;
          padding: 3rem 2rem;
          text-align: center;
          cursor: pointer;
          transition: all 0.3s ease;
          background-color: #f7fafc;
        }

        .upload-zone:hover,
        .upload-zone.dragging {
          border-color: #4299e1;
          background-color: #ebf8ff;
        }

        .upload-zone.uploading {
          cursor: not-allowed;
          opacity: 0.6;
        }

        .upload-prompt p {
          margin: 0.5rem 0;
          color: #4a5568;
        }

        .or-text {
          margin: 1rem 0;
          color: #a0aec0;
          font-size: 0.9rem;
        }

        .browse-button {
          padding: 0.75rem 2rem;
          background-color: #4299e1;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 1rem;
          transition: background-color 0.2s;
        }

        .browse-button:hover {
          background-color: #3182ce;
        }

        .upload-status p {
          color: #4299e1;
          font-weight: 500;
        }

        .error-message {
          margin-top: 1rem;
          padding: 0.75rem;
          background-color: #fed7d7;
          color: #c53030;
          border-radius: 4px;
          text-align: center;
        }
      `}</style>
    </div>
  );
};

export default FileUpload;
