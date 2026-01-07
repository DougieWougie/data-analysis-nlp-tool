/**
 * Custom hook for managing dataset state and operations
 */
import { useState, useCallback } from 'react';
import api from '../services/api';

interface Column {
  name: string;
  data_type: string;
  missing_count: number;
}

interface DatasetMetadata {
  row_count: number;
  column_count: number;
  columns: Column[];
  preview: Record<string, any>[];
}

interface CleaningOperation {
  type: string;
  params: Record<string, any>;
}

export const useDataset = () => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<DatasetMetadata | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refreshDataset = useCallback(async (sid: string) => {
    try {
      setLoading(true);
      setError(null);

      const response = await api.get(`/api/v1/dataset/${sid}`);
      setMetadata(response.data);
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to fetch dataset';
      setError(errorMsg);
      console.error('Error refreshing dataset:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const applyCleaningOperations = useCallback(
    async (operations: CleaningOperation[]) => {
      if (!sessionId) {
        throw new Error('No active session');
      }

      try {
        setLoading(true);
        setError(null);

        const response = await api.post(`/api/v1/dataset/${sessionId}/clean`, operations);
        setMetadata(response.data);

        return response.data;
      } catch (err: any) {
        const errorMsg = err.response?.data?.detail || 'Failed to clean dataset';
        setError(errorMsg);
        console.error('Error cleaning dataset:', err);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [sessionId]
  );

  const dropColumn = useCallback(
    async (columnName: string) => {
      const operations: CleaningOperation[] = [
        {
          type: 'DROP_COLUMNS',
          params: { columns: [columnName] },
        },
      ];

      return applyCleaningOperations(operations);
    },
    [applyCleaningOperations]
  );

  const renameColumn = useCallback(
    async (oldName: string, newName: string) => {
      const operations: CleaningOperation[] = [
        {
          type: 'RENAME_COLUMN',
          params: { old_name: oldName, new_name: newName },
        },
      ];

      return applyCleaningOperations(operations);
    },
    [applyCleaningOperations]
  );

  const fillNA = useCallback(
    async (column: string, strategy: string, value?: any) => {
      const params: Record<string, any> = { column, strategy };
      if (value !== undefined) {
        params.value = value;
      }

      const operations: CleaningOperation[] = [
        {
          type: 'FILL_NA',
          params,
        },
      ];

      return applyCleaningOperations(operations);
    },
    [applyCleaningOperations]
  );

  const dropNA = useCallback(
    async (columns?: string[]) => {
      const params: Record<string, any> = {};
      if (columns && columns.length > 0) {
        params.columns = columns;
      }

      const operations: CleaningOperation[] = [
        {
          type: 'DROP_NA',
          params,
        },
      ];

      return applyCleaningOperations(operations);
    },
    [applyCleaningOperations]
  );

  const castType = useCallback(
    async (column: string, dtype: string) => {
      const operations: CleaningOperation[] = [
        {
          type: 'CAST_TYPE',
          params: { column, dtype },
        },
      ];

      return applyCleaningOperations(operations);
    },
    [applyCleaningOperations]
  );

  return {
    sessionId,
    setSessionId,
    metadata,
    setMetadata,
    loading,
    error,
    refreshDataset,
    applyCleaningOperations,
    dropColumn,
    renameColumn,
    fillNA,
    dropNA,
    castType,
  };
};
